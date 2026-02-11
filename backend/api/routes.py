from flask import Blueprint, request, jsonify
from core.ai_analyzer import AIAnalyzer
from typing import Tuple

api_bp = Blueprint('api', __name__, url_prefix='/api')
analyzer = AIAnalyzer()



@api_bp.route('/analyze', methods=['POST'])
def analyze_error() -> Tuple[dict, int]:
    """
    Main endpoint for error analysis
    
    Request body:
    {
        "error_input": "error message or stack trace"
    }
    
    Returns:
    {
        "metadata": {...},
        "analysis": {...}
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'error_input' not in data:
            return jsonify({'error': 'Missing error_input field'}), 400
        
        error_input = data['error_input'].strip()
        
        if not error_input:
            return jsonify({'error': 'error_input cannot be empty'}), 400
        
        if len(error_input) > 10000:
            return jsonify({'error': 'error_input too large (max 10000 chars)'}), 400
        
        result = analyzer.analyze_error(error_input)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@api_bp.route('/health', methods=['GET'])
def health_check() -> Tuple[dict, int]:
    """Status check endpoint"""
    return jsonify({'status': 'Working :D'}), 200




@api_bp.route('/supported-languages', methods=['GET'])
def supported_languages() -> Tuple[dict, int]:
    """Get list of supported languages"""
    languages = list(analyzer.language_detector.LANGUAGE_PATTERNS.keys())
    return jsonify({'languages': languages}), 200