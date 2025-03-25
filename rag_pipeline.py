import os
import re
from llm_error_handling.retry_mechanism.retry_handler import retry
import ollama
from vector_db import retrieve_chunks

class RAGPipeline:
    def __init__(self):
        self.system_prompt = """ You are a course transcript guide. Your ONLY task is to direct students to the correct week/lecture for topics using the format: 'See [Week X, Lecture Y.Y]'. Rules:

1. ALWAYS reference the CSV structure (subject/title/course/week/lecture)
2. NEVER provide explanations or answers
3. If the topic isn't covered, respond: 'Not in materials'"""

    @retry(max_retries=3, initial_delay=1)
    def query(self, collection, prompt: str) -> dict:
        try:
            context_chunks = retrieve_chunks(collection, prompt)
            context = "\n\n".join(context_chunks)
            response = ollama.chat(
                model="deepseek-r1:14b",
                messages=[{
                    "role": "system",
                    "content": f"{self.system_prompt}\n\nCourse Materials:\n{context}"
                }, {
                    "role": "user",
                    "content": prompt
                }]
            )
            return {
                "success": True,
                "response": response['message']['content'],
                "context_chunks": context_chunks
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "context_chunks": []
            }

def setup_rag_pipeline():
    return RAGPipeline()

def query_rag_pipeline(pipeline, collection, query):
    result = pipeline.query(collection, query)
    if result['success']:
        response = re.sub(r'<think>.*?</think>', '', result['response'], flags=re.DOTALL)
        response = response.strip()
        return response
    else:
        return f"Error: {result['error']}"

if __name__ == "__main__":
    # Initialize components
    from data_ingestion import process_transcript, chunk_transcript
    from vector_db import setup_chroma_db, add_documents_to_collection

    # Process data
    file_path = 'data/PDSA_Transcripts.csv'
    transcripts = process_transcript(file_path)
    chunks = chunk_transcript(transcripts)
    
    # Setup vector DB
    collection = setup_chroma_db()
    add_documents_to_collection(collection, chunks)

    # Initialize pipeline
    pipeline = RAGPipeline(collection)

    # Test query
    test_query = "Where can I find information on string matching?"
    result = pipeline.query(test_query)
    
    print(f"Query: {test_query}")
    print(f"Success: {result['success']}")
    if result['success']:
        print("Response:")
        print(result['response'][:1000] + "...")
    else:
        print(f"Error: {result['error']}")