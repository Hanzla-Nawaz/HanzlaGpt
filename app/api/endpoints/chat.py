from fastapi import APIRouter, HTTPException
from app.schemas.schema import QueryRequest, QueryResponse
from app.core.config import settings
from app.core.database import create_tables, log_chat
from app.core.vectorstore import create_vector_store
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, LLMChain
from langchain.output_parsers import PydanticOutputParser
from app.templates.prompts import (
    INTENT_ROUTING_PROMPT, RAG_PROMPT, CAREER_PROMPT,
    AI_PROMPT, CYBER_PROMPT, PERSONAL_PROMPT
)

chat_router = APIRouter()

# Setup
create_tables()
lll = ChatOpenAI(model=settings.OPENAI_MODEL_NAME, openai_api_key=settings.OPENAI_API_KEY or "YOUR_DEFAULT_API_KEY", temperature=0.1)
vector_store = create_vector_store()

# Chains
if vector_store is not None:
    rag_chain = RetrievalQA.from_chain_type(llm=lll, retriever=vector_store.as_retriever(), chain_type="stuff",
                                            chain_type_kwargs={"prompt": RAG_PROMPT})
else:
    # Handle the case where vector_store is None, e.g., by creating a default chain or raising an exception
    raise ValueError("Vector store could not be initialized.")

parser = PydanticOutputParser(pydantic_object=QueryResponse)
career_chain = LLMChain(llm=lll, prompt=CAREER_PROMPT, output_parser=parser)
ai_chain = LLMChain(llm=lll, prompt=AI_PROMPT, output_parser=parser)
cyber_chain = LLMChain(llm=lll, prompt=CYBER_PROMPT, output_parser=parser)
personal_chain = LLMChain(llm=lll, prompt=PERSONAL_PROMPT, output_parser=parser)
intent_chain = LLMChain(llm=lll, prompt=INTENT_ROUTING_PROMPT)

@chat_router.post("/query", response_model=QueryResponse)
async def query_chat(request: QueryRequest):
    try:
        # Intent detection
        intent_json = intent_chain.run(question=request.query)
        intent = intent_json.get("intent", "general_rag")
        # Route
        if intent == "career_guidance":
            answer = career_chain.run(question=request.query)
        elif intent == "ai_advice":
            answer = ai_chain.run(question=request.query)
        elif intent == "cybersecurity_advice":
            answer = cyber_chain.run(question=request.query)
        elif intent == "personal_info":
            answer = personal_chain.run(question=request.query)
        else:
            answer = rag_chain.run(request.query)
        # Logging
        log_chat(request.user_id, request.session_id, request.query, answer)
        return QueryResponse(response=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))