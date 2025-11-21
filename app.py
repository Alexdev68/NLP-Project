import os
import re
from flask import Flask, render_template, request, flash, redirect, url_for
from groq import Groq

app = Flask(__name__)
app.secret_key = "dev-secret-for-local"


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
def build_prompt(pre):
    return (
        f"Original question: {pre['original']}\n"
        f"Processed question: {pre['processed']}\n\n"
        "Answer concisely. If clarification is needed, ask a single clarifying question.\n\n"
        "Answer:\n"
    )


# -----------------------------------------
# Grok API call
# -----------------------------------------
def call_grok(prompt: str, model="grok-2-latest"):
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        raise RuntimeError("XAI_API_KEY environment variable is missing.")

    client = Groq(api_key=os.getenv("XAI_API_KEY"))


    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",  "content": prompt}
        ]
    )

    return response


# -----------------------------------------
# Flask Routes
# -----------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        model = request.form.get("model", "grok-2-latest")

        if not question:
            flash("Please enter a question.", "warning")
            return redirect(url_for("index"))

        pre = preprocess_question(question)
        prompt = build_prompt(pre)

        try:
            raw = call_grok(prompt, model=model)
            answer = raw.choices[0].message["content"]
        except Exception as e:
            flash(f"Error calling Grok: {e}", "danger")
            raw = {}
            answer = None

        return render_template("index.html",
                               original=pre["original"],
                               processed=pre["processed"],
                               tokens=pre["tokens"],
                               answer=answer,
                               llm_raw=raw,
                               model=model)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
