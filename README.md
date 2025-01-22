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

0. [PDF Text to Review](review_generation/0_pdf_text_review.py): Given a PDF of a paper, convert it
   to text and generate a review using a single prompt.
1. [PDF Text to Review, Step-by-Step](review_generation/1_pdf_text_step_review.py): Same as above, but using prescribed steps that ask specific questions (see `review_generation/1_pdf_text_step_review.py` for details).
2. [O1 Review](review_generation/2_pdf_text_o1_review.py): Same as 0, but using the O1 model.
