import re
from typing import Tuple, Optional

class LanguageDetector:
    """Detect programming language from error input"""
    
    LANGUAGE_PATTERNS = {
        'python': [
            r'Traceback \(most recent call last\)',
            r'^\s*File ".*", line \d+',
            r'(?:Error|Exception):\s',
            r'import error|from.*import',
            r'IndentationError|SyntaxError|AttributeError|TypeError|ValueError',
        ],
        'javascript': [
            r'at\s+\w+\s+\(',
            r'TypeError:.*is not a function',
            r'SyntaxError:',
            r'ReferenceError:',
            r'JSON\.parse|console\.log|require\(|import\s+{',
        ],
        'java': [
            r'Exception in thread',
            r'at\s+[\w.]+\([\w.]+\.java:\d+\)',
            r'(NullPointerException|IndexOutOfBoundsException|ClassNotFoundException)',
            r'public class|private void|throws',
        ],
        'csharp': [
            r'at\s+\w+\.[\w.]+\(.*\.cs:\d+\)',
            r'(NullReferenceException|IndexOutOfRangeException)',
            r'using\s+System|public class|private void',
        ],
        'golang': [
            r'panic:',
            r'goroutine\s+\d+',
            r'fatal error:',
            r'func\s+\w+\(|defer\s+',
        ],
        'php': [
            r'Fatal error:|Parse error:|Warning:',
            r'Stack trace:|#\d+\s+[\w.]+\(\)',
            r'\$\w+|<?php|echo|function',
        ],
        'ruby': [
            r'(Traceback|.*\.rb:\d+:in)',
            r'raise\s+|def\s+\w+|class\s+\w+',
            r'(NoMethodError|ArgumentError|SyntaxError)',
        ],
        'sql': [
            r'SQL Error|SQL syntax|ORA-\d+',
            r'(SELECT|INSERT|UPDATE|DELETE)\s+',
            r'(MySQLError|PostgreSQLError)',
        ],
    }
    
    @staticmethod
    def detect_language(error_input: str) -> Tuple[str, float]:
        """
        Detect programming language from error input
        
        Args:
            error_input: The error message or stack trace
            
        Returns:
            Tuple of (language, confidence_score)
        """
        if not error_input or len(error_input.strip()) == 0:
            return 'unknown', 0.0
        
        scores = {}
        
        for language, patterns in LanguageDetector.LANGUAGE_PATTERNS.items():
            matches = 0
            for pattern in patterns:
                if re.search(pattern, error_input, re.IGNORECASE | re.MULTILINE):
                    matches += 1
            scores[language] = matches / len(patterns)
        
        # Find best match
        best_language = max(scores, key=scores.get)
        best_score = scores[best_language]
        
        if best_score == 0:
            return 'unknown', 0.0
        
        return best_language, min(best_score, 1.0)
    
    @staticmethod
    def detect_platform(error_input: str) -> Optional[str]:
        """Detect platform/framework from error"""
        platforms = {
            'django': r'django|DjangoRuntimeError',
            'fastapi': r'fastapi|FastAPI',
            'flask': r'flask|Werkzeug',
            'spring': r'Spring|SpringBootException',
            'dotnet': r'\.NET|AspNet',
            'nodejs': r'npm|Node\.js|express',
            'react': r'React|ReactDOM|JSX',
            'angular': r'Angular|ng-',
            'docker': r'Docker|container|image',
            'kubernetes': r'kubectl|pod|deployment',
        }
        
        for platform, pattern in platforms.items():
            if re.search(pattern, error_input, re.IGNORECASE):
                return platform
        
        return None