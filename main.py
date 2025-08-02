import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
# import openai
import os

app = FastAPI()

# Allow frontend to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/ask_llm")
async def ask_llm(request: Request):
    data = await request.json()
    # question = "what is the capitol of pakistan"
    chatGPT = False
    if chatGPT:
        return "feature under development"
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",  # You can use "gpt-4" if you have access
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant."},
        #         {"role": "user", "content": question}
        #     ],
        #     max_tokens=200,
        #     temperature=0.7
        # )
        #
        # answer = response["choices"][0]["message"]["content"].strip()
        # return {"answer": answer}
    else:
        ollama_response = requests.post(
            "http://localhost:11434/api/generate",
            headers={"Content-Type": "application/json"},
            json={
                "model": "mistral",
                "prompt": data["data"]+" "+ data["prompt"],
                "stream": False
            }
        )

        if ollama_response.status_code != 200:
            return {"error": "Failed to get response from LLM", "details": ollama_response.text}

        response_json = ollama_response.json()
        answer = response_json.get("response", "").strip()

        return answer

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



# @app.post("/ask")
# async def ask_llm(request: Request):
#     data = await request.json()
#     question = data.get("question", "What is the capital of France?")
#
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
