"""
LLM_QA_CLI.py — Grok (xAI) version
Simple CLI that:
 - accepts a natural-language question
 - preprocesses it (lowercase, punctuation removal, tokenization)
 - constructs a prompt
 - sends it to Grok (xAI API)
 - prints the answer

Set environment variable:
export XAI_API_KEY="your_grok_api_key"
"""

import os
import re
import sys
import argparse
from groq import Groq


# -----------------------------------------
# Preprocessing
# -----------------------------------------
def preprocess_question(question: str) -> dict:
    original = question.strip()
    lowered = original.lower()
    processed = re.sub(r"[^\w\s]", "", lowered)
    processed = re.sub(r"\s+", " ", processed).strip()
    tokens = processed.split(" ") if processed else []
    return {"original": original, "processed": processed, "tokens": tokens}


# -----------------------------------------
# Build prompt
# -----------------------------------------
def build_prompt(pre: dict) -> str:
    return (
        f"Original question: {pre['original']}\n"
        f"Processed version: {pre['processed']}\n\n"
        "Answer concisely and clearly. If more information is needed, ask one short clarification.\n\n"
        "Answer:\n"
    )


# -----------------------------------------
# Grok API call
# -----------------------------------------
def call_grok(prompt: str, model: str = "grok-2-latest") -> str:
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        raise RuntimeError("XAI_API_KEY is not set in environment variables.")

    client = Groq(api_key=os.getenv("XAI_API_KEY"))


    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful, concise assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message["content"]


# -----------------------------------------
# CLI entry point
# -----------------------------------------
def main():
    parser = argparse.ArgumentParser(description="LLM Q&A CLI — Grok version")
    parser.add_argument("-q", "--question", type=str, help="Question text")
    parser.add_argument("-m", "--model", type=str, default="grok-2-latest", help="Grok model")
    args = parser.parse_args()

    if args.question:
        question = args.question
    else:
        print("Enter your question:")
        question = sys.stdin.readline().strip()

    if not question:
        print("No question provided.")
        return

    pre = preprocess_question(question)
    prompt = build_prompt(pre)

    print("\n--- Processed Question ---")
    print(pre["processed"])

    print("\nCalling Grok…")
    try:
        answer = call_grok(prompt, model=args.model)
    except Exception as e:
        print("Error:", e)
        return

    print("\n--- Grok Answer ---")
    print(answer)


if __name__ == "__main__":
    main()
