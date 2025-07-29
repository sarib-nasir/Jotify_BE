from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import numpy

app = FastAPI()

# Allow frontend to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Limit in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask_llm(request: Request):
    data = await request.json()
    # question = data.get("question", "")
    task = "get the capital of france?"
    llm_response = requests.post(
        "http://localhost:8000/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "nvidia/Llama-3_3-Nemotron-Super-49B-v1_5",
            "messages": [
                {
                    "role": "user",
                    "content": task
                }
            ]
        }
    )

    # Extract the LLM's response
    response_json = llm_response.json()
    answer = response_json["choices"][0]["message"]["content"]

    return {"answer": answer}
if __name__ == '__main__':
    ('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
