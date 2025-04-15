from pinecone.grpc import PineconeGRPC as Pinecone
from typing import List, Dict, Any
from semchunk import chunkerify
from openai import OpenAI
import tiktoken
import secrets
import string
import json
import re



class Chunker:
    def __init__(self,input_json_path = r'Liquid.json', output_chunks_path = r'E:\Projects and codes\PDF_Manager\scripts\chunks.json'):
        self.used_ids = set()
        self.input_json_path = input_json_path
        self.output_chunks_path = output_chunks_path

    def generate_unique_id(self, prefix='doc_', length=6):
        while True:
            characters = string.ascii_lowercase + string.digits
            random_part = ''.join(secrets.choice(characters) for _ in range(length))
            new_id = f"{prefix}{random_part}"
            
            if new_id not in self.used_ids:
                self.used_ids.add(new_id)
                return new_id
            
    def process_document_chunks(self,documents: List[Dict[Any, Any]], chunk_size: int = 300):
        tokenizer = tiktoken.get_encoding('cl100k_base')
        chunker = chunkerify(tokenizer, chunk_size=chunk_size)
        
        processed_chunks = []
        
        for doc in documents:
            filename = doc.get('File name', 'unknown')
            # meta = doc.get('meta_info', {})  # Default to empty dict
            
            # Process text chunks
            if doc.get('text'):
                text_chunks = chunker(doc['text'], overlap=0.1)
                processed_chunks.extend([
                    {   'id' : self.generate_unique_id(),
                        'type': 'text',
                        'content': chunk,
                        'source': filename  # Create new dict with added filename
                    } for chunk in text_chunks
                ])
        
        return processed_chunks

    def SemanticChunker(self):
        
        # Load documents
        with open(self.input_json_path, 'r', encoding='utf-8') as f:
            documents = json.load(f)
        
        # Process chunks
        processed_chunks = self.process_document_chunks(documents)

        with open(self.output_chunks_path, 'w', encoding='utf-8') as f:
            json.dump(processed_chunks, f, ensure_ascii=False, indent=4)
        
        print(f"Processed {len(documents)} documents")
        print(f"Created {len(processed_chunks)} chunks")



# Example Usage
# if __name__ == "__main__":
#     pdf_manager = AnswerQuery(
#         embedding_api_key="sk-None-E8mR7aEJJUOXcpsDZsMKT3BlbkFJ3vHG99vv7CHkrCTh4iEU",
#         embedding_model="text-embedding-3-small",
#         pinecone_api_key="pcsk_3wzzr3_8c2WiBgY3Fsd8eGGnktQW98ayKLwbHrvCrL488LSLGH7gZcHuaXEveSpLwwqi83",
#         pinecone_index_name="pdf-manager",
#         gpt_model="gpt-3.5-turbo",
#         gpt_api_key="sk-None-E8mR7aEJJUOXcpsDZsMKT3BlbkFJ3vHG99vv7CHkrCTh4iEU",
#         content_file_path=r"E:\\Projects and codes\\PDF_Manager\\scripts\\chunks.json"
#     )

#     query = "What was the primary purpose of this Data Labeling project?"
#     response = pdf_manager.run_query(query)
#     print(response)