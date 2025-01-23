import argparse
import openai
import PyPDF2
import os
import sys

sys.path.append(os.getcwd())
from util.util import extract_text_from_pdf, get_openai_api_key

def compute_usage_cost(model_type, prompt_tokens, completion_tokens):
    if model_type == "o1":
        return prompt_tokens * 15/1e6 + completion_tokens * 60/1e6
    elif model_type == "gpt-4o":
        return prompt_tokens * 2.5/1e6 + completion_tokens * 60/1e6

def generate_review(openai_api_key, text):
    current_file_path = os.path.abspath(__file__)
    review_prompt_path = os.path.join(os.path.dirname(current_file_path), "review_prompt.txt")
    review_prompt = open(review_prompt_path, "r").read().strip()

    openai.api_key = openai_api_key

    print("Generating a review of the paper...")
    review_response = openai.ChatCompletion.create(
        model="o1",
        messages=[
            {"role": "system", "content": "You are an expert reviewer for AI conference papers."},
            {"role": "user", "content": f"Read the following paper, in preparation to review it:\n{text}"},
            {"role": "user", "content": f"{review_prompt}"}
        ]
    )
    review = review_response['choices'][0]['message']['content']
    print("Usage:")
    print(review_response['usage'])
    prompt_tokens = review_response['usage']['prompt_tokens']
    completion_tokens = review_response['usage']['completion_tokens']
    print(f"Cost: ${compute_usage_cost('o1', prompt_tokens, completion_tokens):.2f}")

    return review

def main():
    # Required argument: paper PDF path.
    if len(sys.argv) < 2:
        print("Usage: python 2_pdf_text_o1_review.py <path_to_pdf>")
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

    review_file_path = os.path.join(pdf_dir, "2_review.txt")

    with open(review_file_path, "w") as review_file:
        review_file.write(review)

    print(f"Review has been saved to {review_file_path}")

if __name__ == "__main__":
    main()
