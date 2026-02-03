import os
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ ONLY VALID MODEL
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

def call_llm(prompt: str) -> str:
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 1024
        }
    )
    return response.text
