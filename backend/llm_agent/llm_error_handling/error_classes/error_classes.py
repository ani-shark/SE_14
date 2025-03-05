class LLMErrorTypes:
    API_ERROR = 'api_error'
    HALLUCINATION = 'hallucination' 
    ROLE_SWITCH = 'role_switch'
    TIMEOUT = 'timeout'
    VALIDATION = 'validation'
    CONTEXT_OVERFLOW = 'context_overflow'

class LLMError(Exception):
    """Base class for LLM-related errors"""
    def __init__(self, error_type, message, details=None):
        self.error_type = error_type
        self.message = message
        self.details = details
        super().__init__(self.message)

class HallucinationError(LLMError):
    """When LLM generates factually incorrect content"""
    pass

class RoleSwitchError(LLMError):
    """When LLM assumes incorrect persona/role""" 
    pass