import requests
import os
from dotenv import load_dotenv
load_dotenv()


url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    "HTTP-Referer": "http://localhost:8000",  # or your actual dev URL
    "Content-Type": "application/json"
}

data = {
    "model": "openai/gpt-3.5-turbo",  # or another model from OpenRouter
    "messages": [
        {"role": "user", "content": "Hello, who are you?"}
    ]
}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.json())
