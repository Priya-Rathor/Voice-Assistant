from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from config import GOOGLE_API_KEY, MODEL_NAME, TEMPERATURE
import uvicorn

app = FastAPI(title="Voice AI Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
generation_config = {
    "temperature": TEMPERATURE,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
}

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config=generation_config,
)

# Store chat sessions (in production, use Redis or database)
chat_sessions = {}

# Request/Response Models
class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"

class QueryResponse(BaseModel):
    response: str
    session_id: str

class ResetRequest(BaseModel):
    session_id: str = "default"

class HealthResponse(BaseModel):
    status: str
    message: str

# Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Voice AI Assistant API is running"
    }

@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process user query and return AI response"""
    try:
        # Get or create chat session
        if request.session_id not in chat_sessions:
            chat_sessions[request.session_id] = model.start_chat(history=[])
        
        chat = chat_sessions[request.session_id]
        
        # System message for context
        system_message = """You are a helpful voice assistant. 
Guidelines:
- Give complete, natural responses
- Keep answers conversational but thorough
- Always finish your sentences completely
- Speak in a friendly, clear manner"""
        
        # Send message with system context
        full_prompt = f"{system_message}\n\nUser: {request.query}\nAssistant:"
        
        response = chat.send_message(full_prompt)
        assistant_response = response.text
        
        return {
            "response": assistant_response,
            "session_id": request.session_id
        }
        
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@app.post("/api/reset")
async def reset_conversation(request: ResetRequest):
    """Reset conversation history"""
    try:
        if request.session_id in chat_sessions:
            chat_sessions[request.session_id] = model.start_chat(history=[])
        
        return {
            "status": "success",
            "message": "Conversation history cleared",
            "session_id": request.session_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error resetting conversation: {str(e)}"
        )

@app.get("/api/status")
async def get_status():
    """Get API status and active sessions"""
    return {
        "status": "active",
        "active_sessions": len(chat_sessions),
        "model": MODEL_NAME
    }

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting Voice AI Assistant API Server")
    print("=" * 60)
    print(f"Model: {MODEL_NAME}")
    print(f"Temperature: {TEMPERATURE}")
    print("Server: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(app, host="127.0.0.1", port=8000)