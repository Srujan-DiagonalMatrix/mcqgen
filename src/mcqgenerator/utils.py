import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith('.pdf'):
        try:
            pdf_reader=PyPDF2.PdfReader(file)
            text=""

            for page in pdf_reader.pages:
                text+=page.extract_text()
            
            return text

        except Exception as e:
            raise Exception(f"Error reading PDF file: {e}")
        
    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')

    else:
        raise Exception("Unsupported file format, PDF and TXT files are supported")

def get_table_data(quiz_str):
    if not quiz_str or not isinstance(quiz_str, str):
        raise ValueError("Input quiz_str is empty or not a string.")
    
    try:
        # Attempt to parse JSON
        quiz_dict = json.loads(quiz_str)
        return quiz_dict
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
