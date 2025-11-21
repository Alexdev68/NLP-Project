# LLM Q&A System (Grok Version)

## Files include:

-   LLM_QA_CLI.py
-   app.py
-   templates/index.html
-   static/style.css
-   requirements.txt

## Setup

### 1. Install requirements

pip install -r requirements.txt

### 2. Set environment variable

export XAI_API_KEY="your_grok_api_key"

### 3. Run CLI

python LLM_QA_CLI.py -q "What is computer architecture?"

### 4. Run Flask Web App

flask run\
Open: http://127.0.0.1:5000

## Deployment (Render)

-   Build command: pip install -r requirements.txt
-   Start command: gunicorn app:app
-   Add environment variable: XAI_API_KEY

## Model Used

Grok-2 (xAI LLM)
