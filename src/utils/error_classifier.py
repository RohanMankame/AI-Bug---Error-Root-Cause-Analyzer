import re
from enum import Enum
from typing import Optional

class ErrorSeverity(Enum):
    """
    Error severity levels
    """
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ErrorType(Enum):
    """
    Error type categories
    """
    SYNTAX = "syntax_error"
    RUNTIME = "runtime_error"
    LOGIC = "logic_error"
    DEPENDENCY = "dependency_error"
    CONFIGURATION = "configuration_error"
    NETWORK = "network_error"
    AUTHENTICATION = "authentication_error"
    DATABASE = "database_error"
    MEMORY = "memory_error"
    PERFORMANCE = "performance_error"
    UNKNOWN = "unknown_error"



class ErrorClassifier:
    """
    Classify errors by type and severity
    """
    
    SEVERITY_PATTERNS = {
        ErrorSeverity.CRITICAL: [
            r'fatal error|crash|outofmemory|segmentation fault',
            r'deadlock|infinite loop|stack overflow',
            r'system shutdown|kernel panic',
        ],

        ErrorSeverity.HIGH: [
            r'exception|error|failed|failure',
            r'access denied|permission|unauthorized',
            r'connection (refused|reset|closed|timeout)',
        ],

        ErrorSeverity.MEDIUM: [
            r'warning|deprecated|deprecated',
            r'null pointer|undefined|none',
            r'type mismatch|incompatible',
        ],

        ErrorSeverity.LOW: [
            r'notice|info|debug',
            r'minor|cosmetic|ui issue',
        ],
    }
    



    ERROR_TYPE_PATTERNS = {
        ErrorType.SYNTAX: [
            r'SyntaxError|ParseError|compile error',
            r'unexpected token|invalid syntax|unmatched',
        ],

        ErrorType.RUNTIME: [
            r'RuntimeError|Exception|Error at runtime',
            r'AttributeError|TypeError|NameError',
        ],

        ErrorType.DEPENDENCY: [
            r'ModuleNotFoundError|ImportError|cannot find module',
            r'no such file|dependency not found|missing library',
        ],

        ErrorType.CONFIGURATION: [
            r'configuration error|config not found',
            r'invalid config|missing configuration',
        ],

        ErrorType.NETWORK: [
            r'connection (failed|refused|timeout)',
            r'network unreachable|host unreachable|no route',
        ],

        ErrorType.AUTHENTICATION: [
            r'authentication failed|invalid (credentials|token)',
            r'unauthorized|forbidden|access denied',
        ],

        ErrorType.DATABASE: [
            r'database error|SQL error|query failed',
            r'(connection refused|timeout) at database',
        ],

        ErrorType.MEMORY: [
            r'out of memory|memory exhausted|heap space',
            r'stack overflow|too much recursion',
        ],
    }
    
    @staticmethod
    def classify_severity(error_input: str) -> ErrorSeverity:
        """
        Classify error severity
        """
        for severity, patterns in ErrorClassifier.SEVERITY_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, error_input, re.IGNORECASE):
                    return severity
        
        # Default to medium if error is present
        if re.search(r'error|exception|failed', error_input, re.IGNORECASE):
            return ErrorSeverity.MEDIUM
        
        return ErrorSeverity.LOW
    
    @staticmethod
    def classify_error_type(error_input: str) -> ErrorType:
        """
        Classify error type
        """
        for error_type, patterns in ErrorClassifier.ERROR_TYPE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, error_input, re.IGNORECASE):
                    return error_type
        
        return ErrorType.UNKNOWN
    
    @staticmethod
    def extract_error_message(error_input: str) -> str:
        """
        Extract the main error message
        """
        lines = error_input.split('\n')
        
        # Look for typical error patterns
        for line in lines:
            if re.search(r'(Error|Exception|Fatal):', line):
                return line.strip()
        
        # Return last non-empty line as fallback
        for line in reversed(lines):
            if line.strip():
                return line.strip()
        
        return "Unknown error"