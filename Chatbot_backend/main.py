import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from chatbot import get_bot_reply

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ChatRequest(BaseModel):
    conversation: list

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    reply = get_bot_reply(request.conversation)
    return {"reply": reply}

# Mount static files
# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
