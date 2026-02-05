import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .chatbot import get_bot_reply
from .sessions import router as sessions_router
from supabase import create_client

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Supabase connection
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.include_router(sessions_router, prefix="/sessions")

# Request/Response models
class ChatRequest(BaseModel):
    conversation: list

class ChatResponse(BaseModel):
    reply: str

class CreateUserRequest(BaseModel):
    id: str
    name: str
    email: str
    role: str = "patient"  # Default to patient

class LoginRequest(BaseModel):
    name: str
    password: str

class LoginResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str

@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    """
    Authenticate a user (doctor or patient) by name and password.
    Returns user info if credentials are valid.
    """
    try:
        # Query users table by name and password
        response = supabase.table("users").select("*").eq("name", request.name).eq("password", request.password).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=401, detail="Invalid name or password")
        
        user = response.data[0]
        return LoginResponse(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            role=user["role"]
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

# Request/Response models
class ChatRequest(BaseModel):
    conversation: list

class ChatResponse(BaseModel):
    reply: str

class CreateUserRequest(BaseModel):
    id: str
    name: str
    email: str
    password: str
    role: str = "patient"  # Default to patient

class RegisterPatientRequest(BaseModel):
    name: str
    email: str
    password: str

@app.post("/users")
def create_user(request: CreateUserRequest):
    """Create a new user (patient or doctor)"""
    try:
        response = supabase.table("users").insert({
            "id": request.id,
            "name": request.name,
            "email": request.email,
            "password": request.password,
            "role": request.role
        }).execute()
        
        return {"message": "User created", "user": response.data[0] if response.data else None}
    except Exception as e:
        return {"error": str(e)}

@app.post("/register-patient")
def register_patient(request: RegisterPatientRequest):
    """Register a new patient (called by doctor)"""
    import uuid
    try:
        patient_id = str(uuid.uuid4())
        response = supabase.table("users").insert({
            "id": patient_id,
            "name": request.name,
            "email": request.email,
            "password": request.password,
            "role": "patient"
        }).execute()
        
        if response.data:
            return {
                "message": "Patient registered successfully",
                "patient_id": patient_id,
                "patient_name": request.name,
                "patient_email": request.email
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to register patient")
    except Exception as e:
        print(f"Register patient error: {e}")
        raise HTTPException(status_code=500, detail=f"Registration error: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    reply = get_bot_reply(request.conversation)
    return {"reply": reply}

# Mount static files
# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
