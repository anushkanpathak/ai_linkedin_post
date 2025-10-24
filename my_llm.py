import subprocess
import google.generativeai as genai
GOOGLE_API_KEY = 
OLLAMA_MODEL = "llama3.2"
genai.configure(api_key=GOOGLE_API_KEY)
GOOGLE_MODEL = "models/gemini-2.5-flash"

def call_google(prompt: str) -> str:
    """Generate response using Google Gemini API."""
    try:
        model = genai.GenerativeModel(GOOGLE_MODEL)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[Google API Error] {e}")
        return None

def call_ollama(prompt: str) -> str:
    """Fallback: Generate response using Ollama locally."""
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.decode("utf-8").strip()
    except Exception as e:
        print(f"[Ollama Error] {e}")
        return "Error: Unable to get response from both Google API and Ollama."

def call_llm(prompt: str) -> str:
    """Main function: Try Google API first, fallback to Ollama."""
    response = call_google(prompt)
    if response:
        return response
    else:
        print("⚠️ Google API failed, switching to Ollama...")
        return call_ollama(prompt)
