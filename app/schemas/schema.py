from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    provider: Optional[str] = None  # e.g., openai, groq, together, hf
    stream: bool = False
    
    @validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError('Query cannot be empty or whitespace only')
        return v.strip()

class QueryResponse(BaseModel):
    response: str = Field(..., description="AI assistant's response")
    intent: Optional[str] = Field(None, description="Detected intent of the query")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score of the response")
    response_time_ms: Optional[int] = Field(None, description="Response time in milliseconds")
    sources: Optional[List[Any]] = Field(None, description="Sources used for the response")
    provider: Optional[str] = Field(None, description="Active provider used to generate the response")

class ChatHistoryResponse(BaseModel):
    messages: List[Dict[str, Any]] = Field(..., description="Chat history messages")
    total_count: int = Field(..., description="Total number of messages")
    session_id: str = Field(..., description="Session identifier")

class HealthCheckResponse(BaseModel):
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")
    components: Dict[str, str] = Field(..., description="Component statuses")
    providers: Dict[str, Any] = Field(..., description="Provider statuses")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")

class SignupRequest(BaseModel):
    email: str
    password: str

class SignupResponse(BaseModel):
    message: str

class EmailVerificationRequest(BaseModel):
    token: str

class EmailVerificationResponse(BaseModel):
    message: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    message: str = "Login successful"