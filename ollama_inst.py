import ollama
 
 
def Ollama_action(prompt: str, max_tokens: int = 500) -> str:
    """
    Send a prompt to your local Ollama model and return the text response.
 
    Requirements:
      - Ollama installed: https://ollama.com
      - Model pulled  : ollama pull llama3
      - Server running: ollama serve
    """
    try:
        response = ollama.chat(
            model="llama3",                        # swap to "mistral" or "phi3" freely
            messages=[{"role": "user", "content": prompt}],
            options={"num_predict": max_tokens}
        )
        return response["message"]["content"]
    except Exception as e:
        return f"⚠️ Ollama error: {str(e)}\n\nMake sure `ollama serve` is running and the model is pulled."