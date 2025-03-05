import time
import functools
from ..error_classes.error_classes import LLMError, LLMErrorTypes

def retry(max_retries=3, initial_delay=1, backoff_factor=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay
            
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except LLMError as e:
                    if e.error_type not in [LLMErrorTypes.API_ERROR, LLMErrorTypes.TIMEOUT]:
                        raise
                    
                    retries += 1
                    if retries >= max_retries:
                        raise LLMError(
                            error_type=LLMErrorTypes.API_ERROR,
                            message=f"Max retries ({max_retries}) exceeded",
                            details={
                                "original_error": str(e),
                                "retry_attempts": retries
                            }
                        ) from e
                    
                    time.sleep(delay)
                    delay *= backoff_factor
                    
        return wrapper
    return decorator
