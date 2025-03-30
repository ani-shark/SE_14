from flask import Flask, request, jsonify
from rag_pipeline import setup_rag_pipeline, query_rag_pipeline
from vector_db import setup_chroma_db, add_documents_to_collection, get_subject_collection
from data_ingestion import process_transcript, chunk_transcript
from flask_cors import CORS


app = Flask(__name__)

CORS(app, origins=["http://localhost:5000"])

# Initialize LLM
llm = setup_rag_pipeline()

@app.route('/query', methods=['POST'])
def query_transcripts():
    data = request.json
    query = data.get('query')
    subject = data.get('subject')

    if not query or not subject:
        return jsonify({'error': 'Missing query or subject'}), 400

    collection = get_subject_collection(subject)
    response = query_rag_pipeline(llm, collection, query)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(host = '127.0.0.1', port=3000, debug=True)