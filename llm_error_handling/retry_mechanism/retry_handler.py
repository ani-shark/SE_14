# SE_14_rag_pipeline/llm_error_handling/retry_mechanism/retry_handler.py
from functools import wraps
import time
import random

def retry(max_retries=3, initial_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    sleep_time = delay + random.uniform(0, 1)
                    time.sleep(sleep_time)
                    delay *= 2
            return func(*args, **kwargs)
        return wrapper
    return decorator