# LLMs in Reviewing

This project is a collection of code and data to experiment with different ways in which language
models can be used in the reviewing process.
The experiments are organized into three main categories:
1. **Review Generation**: Given a paper, generate a review.
2. **Review Quality Assessment**: Given a review, assess its quality.
3. **Discussion Facilitation**: Given a paper, a set of reviews, author responses, and (optionally)
   previous discussion threads, summarize the consensus among reviewers, the points of disagreement,
   and either make a recommendation for acceptance or rejection or suggest points to be discussed to
   reach a consensus.
   
## Requirements

All requirements are listed in `requirements.txt`. To install them, run:
```bash
pip install -r requirements.txt
```

## Review Generation

### 0. PDF Review Generation

This is a baseline approach to review generation. It converts the PDF of a paper into text and
queries the LLM for a review with a single prompt.   
Sample usage:
```bash
python review_generation/0_pdf_text_review.py data/iclr_2024/KS8mIvetg2/9019_Proving_Test_Set_Contamin.pdf
```