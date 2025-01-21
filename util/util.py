import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def get_openai_api_key():
    # First check if the API key is in the .openai_api_key file
    api_key_file = ".openai_api_key"
    if os.path.exists(api_key_file):
        with open(api_key_file, "r") as file:
            key = file.read().strip()
            print(f"Using OpenAI API key from {api_key_file}")
            return key

    # If not found, check for an environment variable named OPENAI_API_KEY
    if "OPENAI_API_KEY" in os.environ:
        print("Using OpenAI API key from environment variable OPENAI_API_KEY")
        return os.environ["OPENAI_API_KEY"]
    
    # If still not found, prompt the user to enter the API key
    return input("Enter your OpenAI API key: ")