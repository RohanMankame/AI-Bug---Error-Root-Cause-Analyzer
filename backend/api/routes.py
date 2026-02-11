from flask import Blueprint, request, jsonify
from core.ai_analyzer import AIAnalyzer
from typing import Tuple
import json

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






@api_bp.route('/reevaluate', methods=['POST'])
def reevaluate():
    """
    Re-evaluate the error analysis with user feedback.
    Expects:
    {
        "error_input": "...",
        "metadata": {...},
        "analysis": {...},
        "user_message": "..."
    }
    Returns the same structure as /api/analyze.
    """
    try:
        data = request.get_json()
        error_input = data.get("error_input")
        metadata = data.get("metadata")
        analysis = data.get("analysis")
        user_message = data.get("user_message")

        if not error_input or not metadata or not analysis or not user_message:
            return jsonify({"error": "Missing required fields"}), 400

        # Build the conversation for the LLM
        messages = [
            {"role": "system", "content": (
                "You are an expert senior software engineer and debugging assistant. "
                "Given the original error, previous analysis, metadata, and the user's new feedback, "
                "provide a revised or deeper explanation, new recommendations, or address the user's concerns. "
                "Respond in this JSON format: "
                "{\"root_cause\": ..., \"recommendations\": [...], \"preventive_suggestions\": [...] }"
            )},
            {"role": "user", "content": f"Original error:\n{error_input}\n\nMetadata:\n{json.dumps(metadata, indent=2)}\n\nPrevious analysis:\n{json.dumps(analysis, indent=2)}"},
            {"role": "user", "content": f"User feedback: {user_message}"}
        ]

        from core.ai_analyzer import AIAnalyzer
        analyzer = AIAnalyzer()
        response = analyzer.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=analyzer.config.MAX_ANALYSIS_TOKENS,
        )
        content = response.choices[0].message.content or ""

        # Try to parse the LLM's response as JSON for the analysis section
        try:
            analysis_new = json.loads(content)
        except Exception:
            analysis_new = {
                "root_cause": content[:500],
                "recommendations": [],
                "preventive_suggestions": []
            }

        return jsonify({
            "error_input": error_input,
            "metadata": metadata,
            "analysis": analysis_new
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500