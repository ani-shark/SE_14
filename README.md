# SE_14
Software Engineering group project 

## Backend Set up


### Navigate to the backend directory
# Flask App Setup Guide

## Prerequisites
Ensure you have the following installed on your system:
- Python (version 3.x recommended)
- pip (Python package manager)
- virtualenv (optional but recommended for dependency management)

## Backend

### Setting up the backend
```
# Navigate to the backend directory
cd backend

# Initialize a Python virtual environment (recommended for dependency isolation)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies from requirements.txt using pip
pip install -r requirements.txt
```

### Running the application
```
# Set up the Flask application environment
# Windows
set FLASK_APP=app.py
# macOS/Linux
export FLASK_APP=app.py

# Start the Flask application
flask run
```


