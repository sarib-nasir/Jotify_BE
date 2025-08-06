import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
from together import Together
from dotenv import load_dotenv
# import openai
import os

from pydantic import BaseModel

app = FastAPI()
load_dotenv()
api_key = os.environ.get("TOGETHER_API_KEY")
# Allow frontend to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/ask_llm")
async def ask_llm(request: Request):
    apiResponse = ApiResponse()
    data = await request.json()
    # question = "what is the capitol of pakistan"
    chatGPT = False
    deepSeek = True
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
    elif deepSeek:
        api_key = os.environ.get("TOGETHER_API_KEY")
        if not api_key:
            raise RuntimeError("TOGETHER_API_KEY is not set!")
        client = Together(api_key=api_key)

        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",
            messages=[
                {"role": "user", "content": data["data"]+" "+ data["prompt"]}
            ],
            stream=True
        )
        answer = response.choices[0].message.content
        apiResponse.data = answer
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

        apiResponse.data = answer
    apiResponse.statusCode = "200"
    return apiResponse

from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class ApiResponse:
    statusCode: str = "11"
    message: str = "No data found"
    data: Optional[Any] = None
    Token: Optional[str] = None
    typeId: Optional[str] = None
    NetworkStatus: int = 0

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)