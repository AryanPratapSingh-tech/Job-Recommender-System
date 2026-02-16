from langchain_ollama import OllamaLLM

def Ollama_action(prompt):
  llm = OllamaLLM(model="gemma:2b")
  response = llm.invoke(prompt)
  return response