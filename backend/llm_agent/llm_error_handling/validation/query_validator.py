import re
from ..error_classes.error_classes import (
    LLMError,
    LLMErrorTypes
)

class QueryValidator:
    def __init__(self, course_context: str):
        self.course_context = course_context
        self.injection_patterns = [
            r"(?:act as|pretend to be|you are now) (?:a student|teacher|admin)",
            r"ignore (previous|instructions)"
        ]

    def validate_query(self, query: str):
        self._check_injection(query)
        self._check_relevance(query)

    def _check_injection(self, query: str):
        for pattern in self.injection_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                raise LLMError(
                    error_type=LLMErrorTypes.VALIDATION,
                    message="Potential prompt injection detected",
                    details={
                        "pattern": pattern,
                        "input": query,
                        "course": self.course_context
                    }
                )

    def _check_relevance(self, query: str):
        # Simple relevance check - can be enhanced later
        query_terms = set(query.lower().split())
        course_terms = set(self.course_context.lower().split())
        
        if len(query_terms & course_terms) / len(query_terms) < 0.3:
            raise LLMError(
                error_type=LLMErrorTypes.VALIDATION,
                message="Query out of course scope",
                details={
                    "course": self.course_context,
                    "query": query,
                    "shared_terms": list(query_terms & course_terms)
                }
            )