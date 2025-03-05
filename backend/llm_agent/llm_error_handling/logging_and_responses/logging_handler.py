import logging
import json
import uuid
from datetime import datetime
from ..error_classes.error_classes import LLMError

class StructuredLogger:
    def __init__(self, log_file="llm_errors.log"):
        self.logger = logging.getLogger("LLM_Logger")
        self.logger.setLevel(logging.ERROR)
        
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        
    def log_error(self, error: LLMError, context: dict):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "error_id": str(uuid.uuid4()),
            "error_type": error.error_type,
            "message": error.message,
            "details": error.details,
            "context": context,
            "stack_trace": self._get_stack_trace()
        }
        
        self.logger.error(json.dumps(log_entry))
    
    def _get_stack_trace(self):
        # Implement proper stack trace collection
        return "Stack trace placeholder"

def error_response(error: LLMError) -> dict:
    return {
        "error": {
            "type": error.error_type,
            "message": error.message,
            "error_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat()
        },
        "success": False
    }