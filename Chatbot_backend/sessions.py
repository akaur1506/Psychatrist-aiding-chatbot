from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables from .env file in the same directory as this script
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

router = APIRouter()

# Request models
class StartSessionRequest(BaseModel):
    patient_id: str

class EndSessionRequest(BaseModel):
    session_id: str

class PingSessionRequest(BaseModel):
    session_id: str

# Supabase connection
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@router.post("/start")
def start_session(request: StartSessionRequest):
    """
    Start a new session for a patient.
    Closes any existing active session.
    """
    patient_id = request.patient_id

    # 1. Close any active session (if any)
    try:
        supabase.table("sessions") \
            .update({"ended_at": datetime.utcnow().isoformat()}) \
            .eq("patient_id", patient_id) \
            .is_("ended_at", "null") \
            .execute()
    except Exception as e:
        print(f"Error closing previous session: {e}")
    except Exception as e:
        print(f"Error closing previous session: {e}")

    # 2. Create new session
    try:
        # include last_seen for heartbeat-based liveness
        now_iso = datetime.utcnow().isoformat()
        response = supabase.table("sessions").insert({
            "patient_id": patient_id,
            "started_at": now_iso,
            "last_seen": now_iso
        }).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to start session")

        return {
            "session_id": response.data[0]["id"],
            "started_at": response.data[0]["started_at"]
        }
    except Exception as e:
        print(f"Error in start_session: {e}")
        raise HTTPException(status_code=500, detail=f"Session error: {str(e)}")


@router.post("/end")
def end_session(request: EndSessionRequest):
    """
    End an active session.
    """
    session_id = request.session_id

    try:
        response = supabase.table("sessions") \
            .update({"ended_at": datetime.utcnow().isoformat(), "last_seen": datetime.utcnow().isoformat()}) \
            .eq("id", session_id) \
            .is_("ended_at", "null") \
            .execute()

        if response.count == 0:
            raise HTTPException(status_code=404, detail="Session not found or already ended")

        return {"status": "session ended"}
    except Exception as e:
        print(f"Error ending session: {e}")
        raise HTTPException(status_code=500, detail=f"Session end error: {str(e)}")


@router.post("/ping")
def ping_session(request: PingSessionRequest):
    """Update session heartbeat (last_seen)."""
    session_id = request.session_id
    try:
        now_iso = datetime.utcnow().isoformat()
        response = supabase.table("sessions") \
            .update({"last_seen": now_iso}) \
            .eq("id", session_id) \
            .execute()

        if response.count == 0:
            raise HTTPException(status_code=404, detail="Session not found")

        return {"status": "ping received", "last_seen": now_iso}
    except Exception as e:
        print(f"Error pinging session: {e}")
        raise HTTPException(status_code=500, detail=f"Ping error: {str(e)}")
