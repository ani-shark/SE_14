import chromadb
from data_ingestion import process_transcript, chunk_transcript

client = chromadb.Client()

def setup_chroma_db(subject):
    return client.create_collection(f"transcripts_{subject}")

def add_documents_to_collection(collection, chunked_transcripts):
    for i, chunk in enumerate(chunked_transcripts):
        collection.add(
            documents=[chunk],
            metadatas=[{"source": f"chunk_{i}"}],
            ids=[f"id_{i}"]
        )

def retrieve_chunks(collection, query, k=5):
    results = collection.query(
        query_texts=[query],
        n_results=k
    )
    return results['documents'][0]

def get_subject_collection(subject):
    collection_name = f"transcripts_{subject}"
    collections = client.list_collections()
    if not collections or collection_name not in collections:
        process_and_store_subject(subject)
    return client.get_collection(collection_name)

def process_and_store_subject(subject):
    file_path = f'data/{subject}_Transcripts.csv'
    transcripts = process_transcript(file_path)
    chunks = chunk_transcript(transcripts)
    collection_name = f"transcripts_{subject}"
    if collection_name not in client.list_collections():
        collection = client.create_collection(collection_name)
    else:
        collection = client.get_collection(collection_name)
    add_documents_to_collection(collection, chunks)

if __name__ == "__main__":
    # Test the functions
    from data_ingestion import process_transcript, chunk_transcript

    file_path = 'data/PDSA_Transcripts.csv'
    transcripts = process_transcript(file_path)
    chunked_transcripts = chunk_transcript(transcripts)

    collection = setup_chroma_db()
    add_documents_to_collection(collection, chunked_transcripts)

    test_query = "What is string matching?"
    retrieved_chunks = retrieve_chunks(collection, test_query)

    print(f"Retrieved {len(retrieved_chunks)} chunks for query: '{test_query}'")
    print(f"First retrieved chunk: {retrieved_chunks[0][:100]}...")