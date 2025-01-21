import argparse
import openai
import PyPDF2
import os
import sys

sys.path.append(os.getcwd())
from util.util import extract_text_from_pdf, get_openai_api_key

def generate_review(openai_api_key, text):
    current_file_path = os.path.abspath(__file__)
    review_prompt_path = os.path.join(os.path.dirname(current_file_path), "review_prompt.txt")
    review_prompt = open(review_prompt_path, "r").read().strip()

    openai.api_key = openai_api_key

    print("Generating a review of the paper...")
    review_response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert reviewer for AI conference papers."},
            {"role": "user", "content": f"Read the following paper, in preparation to review it:\n{text}"},
            {"role": "user", "content": f"{review_prompt}"}
        ]
    )
    review = review_response['choices'][0]['message']['content']

    return review

def main():
    # Required argument: paper PDF path.
    if len(sys.argv) < 2:
        print("Usage: python 0_pdf_review.py <path_to_pdf>")
        return

    openai_api_key = get_openai_api_key()

    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print("Error: The specified file does not exist.")
        return
    print(f"Reviewing paper: {pdf_path}")

    pdf_dir = os.path.dirname(pdf_path)

    print("Extracting text from the PDF...")
    paper_text = extract_text_from_pdf(pdf_path)

    print("Generating review...")
    review = generate_review(openai_api_key, paper_text)

    review_file_path = os.path.join(pdf_dir, "0_review.txt")

    with open(review_file_path, "w") as review_file:
        review_file.write(review)

    print(f"Review has been saved to {review_file_path}")

if __name__ == "__main__":
    main()
