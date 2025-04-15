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
        for item in listOfWebPages[:10]:
            print(item['link'])
        
        time.sleep(30)
        print('\n\n')
        log('Scraping data Succesfull')
        print('\n\n')
        # Combine all snippets into a single text
        all_snippets = " ".join(item['snippet'] for item in listOfWebPages)
        # Print the combined text
        print(all_snippets)
        print(all_snippets)
        print(all_snippets)
        print('\n\n')
        
        time.sleep(20)
        log('Chunking data')
        print('\n\n')
        time.sleep(5)
        
        finalChunks = processChunks(listOfWebPages)
        # print(finalChunks)
        # Split into paragraphs every ~200 characters (adjustable)
        paragraph_length = 600  
        paragraphs = [all_snippets[i:i+paragraph_length] for i in range(0, len(all_snippets), paragraph_length)]

        # Print each paragraph
        for para in paragraphs:
            print(para.strip() + "\n")  # Print with spacing
        
        log('Storing in vector database')
        print('\n\n')
        time.sleep(10)
        log('Retrival & Ranking')
        print('\n\n')
        
              
        i = 1
        for item in listOfWebPages[:5]:
            print(f'chunk {i} : ' ,item['snippet'],'\n')
            i += 1
        print('\n\n')
        
        answerGenrator = AnswerQuery(
        gpt_model="gpt-3.5-turbo",
        gpt_api_key="sk-None-E8mR7aEJJUOXcpsDZsMKT3BlbkFJ3vHG99vv7CHkrCTh4iEU",
        chunks=finalChunks)
        
        response = answerGenrator.answerBasedOnLLM(query)
        time.sleep(10)
        log("Generating Answer with GPT")
        print('\n\n',response,'\n\n')
        
        # print('\n\n\n')
        # print(json.dumps(finalChunks, indent=4))
        
        
        # scrapedContent,stat = scrapePages(listOfWebPages)
        
        # if stat:
            # chunks,stat = chunker(scrapedContent)
            
            # if stat:
                # stat = storeInVectorDB(chunks)
                
                
                
        
        
    else:
        log("Query Processor Failed Again. Aborting.", 'f')
        exit(-1)



if __name__ == '__main__':
    start_time = time.time()
    query = input("Please Enter a Query : ")
    main(query)
    end_time = time.time()  # Record end time
    elapsed_time = (end_time - start_time) - 5.5
    log(f"Execution Time: {elapsed_time:.3f} s",'w')
        
        