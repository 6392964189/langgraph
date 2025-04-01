# Step1: Setup Pydantic Model (Schema Validation)
from pydantic import BaseModel
from typing import List

class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

# Step2: Setup AI Agent from Frontend Request
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

# Only allow Groq models (No OpenAI)
ALLOWED_MODEL_NAMES = ["llama-3.3-70b-versatile"]

app = FastAPI(title="LangGraph AI Agent (Groq + Tavily)")

@app.post("/chat")
def chat_endpoint(request: RequestState): 
    """
    API Endpoint to interact with the Chatbot using Groq (LLM) and Tavily (Search).
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name. Kindly select a valid Groq model."}
    
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    system_prompt = request.system_prompt

    # Get AI response (Groq + Tavily)
    response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt)
    return response

# Step3: Run API Server (Swagger UI available at http://127.0.0.1:9999/docs)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)

