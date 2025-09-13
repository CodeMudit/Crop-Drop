from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile

class ChatRequest(BaseModel):
    prompt: str

class VoiceChatRequest(BaseModel):
    audio: UploadFile  # Audio file (e.g., WAV/MP3)
    lang: Optional[str] = None  # Optional hint; STT auto-detects