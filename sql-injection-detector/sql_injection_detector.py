import re
from datetime import datetime

class SQLInjectionDetector:
    def __init__(self):
        self.patterns = [
            r"(\b(SELECT|UNION|INSERT|UPDATE|DELETE|DROP|EXEC)\b)",
            r"(--|#|/\*|\*/|;--)",
            r"(\b(OR|AND)\b\s+\d+=\d+)",
            r"(\b(CHAR|CONCAT|BENCHMARK)\()",
            r"(WAITFOR\s+DELAY\s+'[^']+')"
        ]
        
    def analyze_parameters(self, params: dict) -> bool:
        for key, value in params.items():
            if isinstance(value, str) and self._contains_sqli(value):
                return True
        return False

    def _contains_sqli(self, input_str: str) -> bool:
        return any(re.search(pattern, input_str, re.IGNORECASE) 
                   for pattern in self.patterns)

class ThreatLogger:
    def __init__(self, log_file='sql_injection.log'):
        self.log_file = log_file
        
    def log_attempt(self, request_data):
        entry = (
            f"[{datetime.now()}] Potential SQL Injection Detected\n"
            f"Request Data: {request_data}\n"
            "----------------------------------------------------\n"
        )
        with open(self.log_file, 'a') as f:
            f.write(entry)