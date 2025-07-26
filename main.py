from fastapi import FastAPI
from app.api.endpoints.router import api_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="HanzalaGPT",
    description="Personal AI assistant using FastAPI, LangChain, and Pinecone",
    version="1.0.0"
)


oring_origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=oring_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api", tags=["API"])

@app.get("/")
async def root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Welcome to HanzalaGPT API"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9090)
