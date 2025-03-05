from flask import Blueprint, request, jsonify
from llm_agent.Simple_wrapper import query_deepseek

llm_bp = Blueprint('llm', __name__)

@llm_bp.route('/ask', methods=['POST'])
def ask_llm():
    """
    API for querying the LLM agent.
    Note: This is a dummy integration and is not fully operational yet.
    """
    data = request.json
    if not data or 'prompt' not in data or 'course' not in data:
        return jsonify({"error": "Invalid request. 'prompt' and 'course' are required."}), 400

    # Dummy response for now
    return jsonify({"response": "LLM endpoint working"})  # Dummy response

