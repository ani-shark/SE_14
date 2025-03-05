import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_error_handling.error_classes.error_classes import LLMError
from llm_error_handling.validation.query_validator import QueryValidator
from llm_error_handling.retry_mechanism.retry_handler import retry
from llm_error_handling.logging_and_responses.logging_handler import (
    StructuredLogger,
    error_response
)
from llm_error_handling.pdf_processor import process_course_materials
import ollama

logger = StructuredLogger()

@retry(max_retries=3, initial_delay=1)
def query_deepseek(prompt: str, course_name: str) -> dict:
    try:
        print(f"Loading course: {course_name}")
        course_context = process_course_materials(course_name)
        print(f"Loaded {len(course_context)//1024} KB of course materials")
        
        validator = QueryValidator(course_context)
        validator.validate_query(prompt)
        
        response = ollama.chat(
            model="deepseek-r1:14b",
            messages=[{
                "role": "system",
                "content": f"""You are a course assistant. Strictly use:
                {course_context[:30000]}... [truncated]
                Cite sources as [Filename#Page]. Say 'Not covered' if unsure."""
            }, {
                "role": "user",
                "content": prompt
            }]
        )
        
        return {
            "success": True,
            "response": response['message']['content'],
            "sources": [
                f"course_materials/{course_name.lower()}/{f}"
                for f in os.listdir(
                    os.path.join("course_materials", course_name.lower())
                )
                if f.endswith(".pdf")
            ]
        }
        
    except LLMError as e:
        logger.log_error(e, {"course": course_name})
        return error_response(e)
        
    except Exception as e:
        generic_error = LLMError(
            error_type="system_error",
            message=f"Operation failed: {str(e)}",
            details={
                "course": course_name,
                "working_dir": os.getcwd(),
                "python_version": sys.version
            }
        )
        logger.log_error(generic_error, {"course": course_name})
        return error_response(generic_error)

if __name__ == "__main__":
    """
    result = query_deepseek(
        "Explain p-values in hypothesis testing",
        "Statistics_2"
    )
    """
    result = "Dummy Result"
    print(result)
