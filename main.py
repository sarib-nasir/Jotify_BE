from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Allow frontend to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/ask")
def ask_llm():
    # data = await request.json()
    question = "give me details about the following note: short theoretical notes for REST api integration"

    # Call the Ollama API
    ollama_response = requests.post(
        "http://localhost:11434/api/generate",
        headers={"Content-Type": "application/json"},
        json={
            "model": "mistral",
            "prompt": question,
            "stream": False
        }
    )

    if ollama_response.status_code != 200:
        return {"error": "Failed to get response from LLM", "details": ollama_response.text}

    response_json = ollama_response.json()
    answer = response_json.get("response", "").strip()

    return answer

if __name__ == "__main__":
    data = ask_llm()
    print(data)

#
# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# import requests
#
# app = FastAPI()
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# @app.post("/ask")
# async def ask_llm(request: Request):
#     data = await request.json()
#     question = data.get("question", "What is the capital of France?")
#
#     # Call the Ollama API
#     ollama_response = requests.post(
#         "http://localhost:11434/api/generate",
#         headers={"Content-Type": "application/json"},
#         json={
#             "model": "mistral",
#             "prompt": question,
#             "stream": False
#         }
#     )
#
#     if ollama_response.status_code != 200:
#         return {"error": "Failed to get response from LLM", "details": ollama_response.text}
#
#     response_json = ollama_response.json()
#     answer = response_json.get("response", "").strip()
#
#     return {"answer": answer}
