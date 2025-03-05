from flask import Blueprint, jsonify

llm_bp = Blueprint('llm', __name__)

@llm_bp.route('/llm/query', methods=['POST'])
def placeholder_llm_query():
    """Placeholder endpoint for LLM integration"""
    return jsonify({
        "success": True,
        "response": "This is a placeholder LLM response",
        "sources": ["course_materials/dummy.pdf"]
    }), 200