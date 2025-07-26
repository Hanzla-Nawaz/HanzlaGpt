from pydantic import BaseModel

class QueryRequest(BaseModel):
    user_id: str
    session_id: str
    query: str

class QueryResponse(BaseModel):
    response: str