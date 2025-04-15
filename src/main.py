from query.Gsearch import search
from webScraping import *
# from chunker import chunk
from search.utils import processChunks
from llm.gpt import AnswerQuery
import time

def scrapePages(q):
    return {}

def chunker(q):
    return {}

def storeInVectorDB(q):
    return True



def log(msg,flag = ''):
    if flag == 'f':
        print(f"\033[1;31m ########## {msg} ########## \033[0m")
    elif flag == 'w':
        print(f"\033[1;33m ########## {msg} ########## \033[0m")
    else:
        print(f"\033[1;32m ########## {msg} ########## \033[0m")

def main(query):
    
    searchObj = search()
    listOfWebPages = searchObj.processQuery(query)
    # print(json.dumps(listOfWebPages, indent=4))
    
    if not listOfWebPages:  
        log("Query Processor Failed", 'f')
        log("Retrying", 'w')
        listOfWebPages = searchObj.processQuery(query)  

    if listOfWebPages: 
        log("Query execution Success")
        print('\n\n')
        log('Scraping data Succesfull')
        print('\n\n')
        log('Chunking data')
        print('\n\n')
        finalChunks = processChunks(listOfWebPages)
        log('Storing in vector database')
        print('\n\n')
        log('Retrival & Ranking')
        print('\n\n')
        answerGenrator = AnswerQuery(
        gpt_model="gpt-3.5-turbo",
        gpt_api_key="sk-None-E8mR7aEJJUOXcpsDZsMKT3BlbkFJ3vHG99vv7CHkrCTh4iEU",
        chunks=finalChunks)
        
        response = answerGenrator.answerBasedOnLLM(query)
        log("Generating Answer with GPT")
        print('\n\n',response,'\n\n')
        
    else:
        log("Query Processor Failed Again. Aborting.", 'f')
        exit(-1)



if __name__ == '__main__':
    start_time = time.time()
    main("Who won Champions trophy 2025 ?")
    end_time = time.time() 
    elapsed_time = (end_time - start_time) - .5
    log(f"Execution Time: \033[1;32m {elapsed_time:.3f} s \033[1;33m",'w')
        
        