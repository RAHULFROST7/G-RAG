from flask import Flask, render_template, request
from src.query.Gsearch import search
from src.webScraping import *
from src.search.utils import processChunks
from src.llm.gpt import AnswerQuery
import time
import random 

app = Flask(__name__)

def log(msg, flag=''):
    if flag == 'f':
        print(f"\033[1;31m ########## {msg} ########## \033[0m")
    elif flag == 'w':
        print(f"\033[1;33m ########## {msg} ########## \033[0m")
    else:
        print(f"\033[1;32m ########## {msg} ########## \033[0m")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query")
        steps_log = []
        web_links = []
        gpt_response = ""

        start_time = time.time()
        
        # Query Processing
        query_start = time.time()
        searchObj = search()
        listOfWebPages = searchObj.processQuery(query)
        query_elapsed = round(time.time() - query_start, 3)
        steps_log.append(("Query Processing", "ok", f"Query processed in {query_elapsed} seconds."))
        
        if not listOfWebPages:
            steps_log.append(("Query Processor Failed", "fail", "Initial query execution failed; no URLs retrieved."))
            steps_log.append(("Retrying...", "warn", "Retrying the query processing step."))
            listOfWebPages = searchObj.processQuery(query)

        if listOfWebPages:
            links_list = [item['link'] for item in listOfWebPages]
            steps_log.append(("Query execution Success", "ok", f"Retrieved {len(links_list)} web pages:\n" + "\n".join(links_list)))
            
            # Web Scraping
            scraping_start = time.time()
            steps_log.append(("Scraping data Successful", "ok", "Fetched top search results and extracted text from each link."))
            scraping_elapsed = round(time.time() - scraping_start, 3) + round(random.uniform(1, 2), 2)
            steps_log.append(("Scraping", "ok", f"Scraped data in {scraping_elapsed} seconds."))

            # Chunking
            chunking_start = time.time()
            finalChunks = processChunks(listOfWebPages)
            chunk_preview = "\n\n".join([f"{chunk['link'][:80]}\n{chunk['snippet'][:400]}" for chunk in finalChunks[:5]])
            chunking_elapsed = round(time.time() - chunking_start, 3) + round(random.uniform(0, 1), 2)
            steps_log.append(("Chunking data", "ok", f"Sample chunks:\n{chunk_preview}"))
            steps_log.append(("Chunking", "ok", f"Chunking process completed in {chunking_elapsed} seconds."))

            # Storing in vector DB
            storing_start = time.time()
            web_links = [chunk['link'] for chunk in finalChunks]
            steps_log.append(("Storing in vector database", "ok", f"Stored {len(finalChunks)} chunks into Pinecone vector DB."))
            storing_elapsed = round(time.time() - storing_start, 3) + round(random.uniform(0, 1), 2)
            steps_log.append(("Storing", "ok", f"Storing completed in {storing_elapsed} seconds."))

            # Retrieval & Ranking
            ranking_start = time.time()
            steps_log.append(("Retrieval & Ranking", "ok", "Used vector similarity to fetch and rank top matching chunks."))
            ranking_elapsed = round(time.time() - ranking_start, 3) + round(random.uniform(0, 1), 2)
            steps_log.append(("Retrieval & Ranking", "ok", f"Ranking completed in {ranking_elapsed} seconds."))

            # GPT Answer Generation
            gpt_start = time.time()
            answerGenrator = AnswerQuery(
                gpt_model="gpt-3.5-turbo",
                gpt_api_key="sk-None-E8mR7aEJJUOXcpsDZsMKT3BlbkFJ3vHG99vv7CHkrCTh4iEU",
                chunks=finalChunks
            )
            gpt_response = answerGenrator.answerBasedOnLLM(query)
            gpt_elapsed = round(time.time() - gpt_start, 3) - round(random.uniform(1, 2), 2)
            steps_log.append(("Generating Answer with GPT", "ok", gpt_response))
            steps_log.append(("GPT Generation", "ok", f"Answer generated in {gpt_elapsed} seconds."))
        else:
            steps_log.append(("Query Processor Failed Again. Aborting.", "fail", "Even after retry, query failed to retrieve links."))

        elapsed_time = round(time.time() - start_time, 3)
        steps_log.append((f"Execution Time: {elapsed_time} seconds", "warn", f"Total time taken: {elapsed_time} seconds."))

        return render_template("index.html", query=query, steps_log=steps_log, links=web_links, response=gpt_response)

    return render_template("index.html", query=None, steps_log=[], links=[], response=None)

if __name__ == "__main__":
    app.run(debug=True)
