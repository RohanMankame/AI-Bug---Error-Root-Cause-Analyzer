from openai import OpenAI
from typing import Dict, Any
import json
from src.config import get_config
from src.utils.language_detector import LanguageDetector
from src.utils.error_classifier import ErrorClassifier, ErrorType


class AIAnalyzer:
    """AI-powered error analysis using OpenAI"""

    def __init__(self):
        self.config = get_config()
        self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
        self.language_detector = LanguageDetector()
        self.error_classifier = ErrorClassifier()

    def analyze_error(self, error_input: str) -> Dict[str, Any]:
        """
        Comprehensive error analysis

        Args:
            error_input: Error message, stack trace, or log content

        Returns:
            Structured analysis result
        """
        # Pre-analysis: detect language and classify
        language, lang_confidence = self.language_detector.detect_language(error_input)
        platform = self.language_detector.detect_platform(error_input)
        severity = self.error_classifier.classify_severity(error_input)
        error_type = self.error_classifier.classify_error_type(error_input)
        error_message = self.error_classifier.extract_error_message(error_input)

        # AI Analysis
        ai_analysis = self._get_ai_analysis(
            error_input, language, platform, error_type
        )

        return {
            "metadata": {
                "detected_language": language,
                "language_confidence": lang_confidence,
                "detected_platform": platform,
                "severity": severity.value,
                "error_type": error_type.value,
                "error_message": error_message,
            },
            "analysis": ai_analysis,
        }

    def _get_ai_analysis(
        self,
        error_input: str,
        language: str,
        platform: str,
        error_type: ErrorType
    ) -> Dict[str, Any]:
        """Get AI-powered analysis"""
        prompt = self._build_prompt(error_input, language, platform, error_type)

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=self.config.MAX_ANALYSIS_TOKENS,
            )

            analysis_text = response.choices[0].message.content or ""
            return self._parse_analysis_response(analysis_text)

        except Exception as e:
            return {
                "root_cause": f"Error analyzing with AI: {str(e)}",
                "recommendations": ["Check your OpenAI API key and connection"],
                "preventive_suggestions": [],
                "error": str(e),
            }

    def _get_system_prompt(self) -> str:
        """
        System prompt for AI analysis
        """
        return """You are an expert senior software engineer and are currently acting as a debugging assistant. Analyze the provided error 
        and provide:
        1. Root cause explanation (clear, concise)
        2. Step-by-step fix recommendations
        3. Preventive best practices

        Format your response as a JSON object with these exact keys:
        {
            "root_cause": "explanation",
            "recommendations": ["step 1", "step 2", ...],
            "preventive_suggestions": ["suggestion 1", "suggestion 2", ...]
        }"""

    def _build_prompt(
        self,
        error_input: str,
        language: str,
        platform: str,
        error_type: ErrorType
    ) -> str:
        """Build analysis prompt"""
        return f"""Analyze this error:

        

        
Language: {language}
Platform: {platform}
Error Type: {error_type.value}

Error Details:
{error_input[:2000]}

Provide root cause, fix steps, and preventive suggestions."""

    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response"""
        try:
            # Try to extract JSON from response
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
        except Exception:
            pass

        # Fallback parsing
        return {
            "root_cause": response_text[:500],
            "recommendations": [],
            "preventive_suggestions": [],
        }