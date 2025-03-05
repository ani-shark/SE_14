import PyPDF2
import os

def sanitize_course_name(name: str) -> str:
    """Converts course names to filesystem-safe format"""
    return (
        name.strip()
        .replace(":", "")
        .replace(",", "")
        .replace(" ", "_")
        .replace("-", "")
        .lower()
    )

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            return "\n".join([page.extract_text() for page in reader.pages])
    except Exception as e:
        raise RuntimeError(f"PDF processing failed: {str(e)}")

def process_course_materials(course_name: str) -> str:
    """Processes all PDFs for a course and returns combined text"""
    sanitized_name = sanitize_course_name(course_name)
    
    # Path resolution within project directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)  # Up to SE_14_AI_Agent
    course_dir = os.path.join(project_root, "course_materials", sanitized_name)
    
    # Normalize path for Windows
    course_dir = os.path.normpath(course_dir)
    
    if not os.path.exists(course_dir):
        available = os.listdir(os.path.join(project_root, "course_materials"))
        raise FileNotFoundError(
            f"Course directory '{sanitized_name}' not found. "
            f"Available courses: {available}"
        )
    
    course_content = []
    for filename in sorted(os.listdir(course_dir)):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(course_dir, filename)
            course_content.append(f"[[{filename}]]\n{extract_text_from_pdf(file_path)}")
    
    if not course_content:
        raise ValueError(f"No PDFs found in {course_dir}")
    
    return "\n\n".join(course_content)