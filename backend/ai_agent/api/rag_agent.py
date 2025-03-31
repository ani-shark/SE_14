from flask import Blueprint, jsonify, request
import requests

rag_bp = Blueprint('rag', __name__)

RAG_SERVICE_URL = 'http://localhost:3000'

@rag_bp.route('/query', methods=['POST'])
def query_rag():
    data = request.get_json()
    query = data.get('query')
    subject = data.get('subject')
    if not query or not subject:
        return jsonify(error="query and subject are required"), 400
    try:
        print(f"Querying RAG pipeline with subject: {subject}, query: {query}")
        response = requests.post(f'{RAG_SERVICE_URL}/query', json={'query': query, 'subject': subject})
        response.raise_for_status()
        print(f"RAG pipeline response: {response}")
        result = response.json()
        if 'response' not in result:
            result['response'] = ""
        return jsonify(result), 200
    except requests.RequestException as e:
        return jsonify({'error': f'Error Querying RAG service: {str(e)}'}), 500