import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_text(prompt):
    payload = {
        "model": "llama3.2",  # or another model you've downloaded
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json().get('response')
    else:
        return f"Error: {response.status_code} - {response.text}"
def call_ollama_ai(prompt):
    # send prompt to AI model and return the response
    # example placeholder:
    return "Mock response to: " + prompt
