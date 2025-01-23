import argparse
import openai
import PyPDF2
import os
import sys

sys.path.append(os.getcwd())
from util.util import extract_text_from_pdf, get_openai_api_key

cot_prompts = [
  "What is the problem that the paper aims to address?",
  "What are the claimed limitations in the state of the art that the paper addresses? Are the limitations real?",
  "What is the key novel technical contribution in the paper? Is it really novel?",
  "Is the technical approach sound and clearly described? Are there any errors, unstated assumptions, or missing details?",
  "Does the empirical evaluation include appropriate baselines and comparisons to validate the proposed approach compared to the state of the art?",
  "Does the empirical evaluation report well-established and reasonable metrics?",
  "Are the evaluation benchmarks and datasets appropriately chosen? Are there any better benchmarks or datasets that should have been used?",
  "Do the empirical results really support the claims of the paper?",
  "Now read your own analysis. Identify any logical gaps or unsubstantiated claims and correct them.",
  "If you were the harshest critic of this paper, what would your top concerns be? Provide a short bullet list of critiques."
  "Name relevant SOTA papers or standard results from major AI conferences in the last 2-3 years that may relate to this approach. Evaluate whether the paper’s contributions outperform or differ significantly."
  "Propose additional experiments or ablations that could strengthen the paper’s claims. How would these experiments be designed?"
]


def compute_usage_cost(model_type, prompt_tokens, completion_tokens):
    if model_type == "o1":
        return prompt_tokens * 15/1e6 + completion_tokens * 60/1e6
    elif model_type == "gpt-4o":
        return prompt_tokens * 2.5/1e6 + completion_tokens * 60/1e6

def generate_cot_review(openai_api_key, text):
    openai.api_key = openai_api_key

    prompt_tokens = 0
    completion_tokens = 0
    messages=[
        {"role": "system", "content": "You are an expert reviewer for AI conference papers."},
        {"role": "user", "content": f"Read the following paper, in preparation to review it. Maintain healthy scientific skepticism, don't assume that the claims in the paper are necessarily correct, and check everything carefully:\n{text}"},
    ]
    print("Generating COT responses...")
    for i in range(len(cot_prompts)):
        prompt = cot_prompts[i]
        # Print a breakline for better readability
        print("=" * 80)
        print(f"Step {i}: {cot_prompts[i]}")
        messages.append({"role": "user", "content": f"{prompt}"})
        cot_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages
        )
        prompt_tokens += cot_response['usage']['prompt_tokens']
        completion_tokens += cot_response['usage']['completion_tokens']
        response = cot_response['choices'][0]['message']['content']
        print(response)
        print("=" * 80)
        messages.append({"role": "assistant", "content": f"{response}"})

    return messages, prompt_tokens, completion_tokens

def generate_review(openai_api_key, text):
    current_file_path = os.path.abspath(__file__)
    review_prompt_path = os.path.join(os.path.dirname(current_file_path), "review_prompt.txt")
    review_prompt = open(review_prompt_path, "r").read().strip()

    openai.api_key = openai_api_key
    messages, prompt_tokens, completion_tokens = generate_cot_review(openai_api_key, text)
    messages.append({"role": "user", "content": f"{review_prompt}"})
    print("Generating a review of the paper...")
    review_response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages
    )
    prompt_tokens += review_response['usage']['prompt_tokens']
    completion_tokens += review_response['usage']['completion_tokens']
    review = review_response['choices'][0]['message']['content']
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Completion tokens: {completion_tokens}")
    print(f"Cost: ${compute_usage_cost('gpt-4o', prompt_tokens, completion_tokens):.2f}")

    return review, messages

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
    review, messages = generate_review(openai_api_key, paper_text)

    review_file_path = os.path.join(pdf_dir, "1_review.txt")
    cot_file_path = os.path.join(pdf_dir, "1_steps.txt")
    
    with open(review_file_path, "w") as review_file:
        review_file.write(review)

    with open(cot_file_path, "w") as cot_file:
        for message in messages:
            cot_file.write(f"{message['role']}: {message['content']}\n")

    print(f"Review has been saved to {review_file_path}")
    print(f"COT responses have been saved to {cot_file_path}")

if __name__ == "__main__":
    main()
