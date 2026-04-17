import os
import requests
from utils.config import get_settings
settings = get_settings()

class LLMService:
    def __init__(self, model):
        self.api_key = settings.LLM_API_KEY
        self.base_url = settings.LLM_BASE_URL
        self.model = model

    def generate(self, prompt: str):
        response = requests.post(
            self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a medical assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2
            }
        )

        return response.json()["choices"][0]["message"]["content"]