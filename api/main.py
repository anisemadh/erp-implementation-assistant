"""
FastAPI Backend for ERP Implementation Assistant
Wraps the ERPAgent for HTTP access from H5 widget
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import sys
import os
from pathlib import Path
import json
import asyncio

# Add src to path
src_path = str(Path(__file__).parent.parent / "src")
sys.path.insert(0, src_path)

from agent import ERPAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="ERP Implementation Assistant API",
    description="AI-powered M3 implementation guidance with RAG",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - Configure for your M3 domain in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to your M3/ION domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent (singleton)
agent = None

def get_agent():
    """Get or create agent instance"""
    global agent
    if agent is None:
        agent = ERPAgent()
    return agent


# Request/Response Models
class UserContext(BaseModel):
    """M3 user context from H5 widget"""
    company: Optional[str] = Field(None, description="M3 Company (CONO)")
    division: Optional[str] = Field(None, description="M3 Division (DIVI)")
    user_id: Optional[str] = Field(None, description="M3 User ID (USID)")
    language: Optional[str] = Field(None, description="Language code")


class QueryRequest(BaseModel):
    """Request body for query endpoint"""
    query: str = Field(..., description="User's question", min_length=1)
    user_context: Optional[UserContext] = Field(None, description="M3 user context")
    conversation_history: Optional[List[Dict]] = Field(None, description="Previous messages")


class QueryResponse(BaseModel):
    """Response body for query endpoint"""
    answer: str = Field(..., description="AI-generated response")
    query_type: str = Field(..., description="Classified query type")
    modules: List[str] = Field(..., description="Relevant M3 modules")
    sources: List[str] = Field(default_factory=list, description="Source documents")
    response_time: float = Field(..., description="Response time in seconds")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str


class MetadataResponse(BaseModel):
    """API metadata response"""
    version: str
    capabilities: Dict
    model: str
    knowledge_base: Dict


# Health & Info Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return HealthResponse(
        status="healthy",
        service="ERP Implementation Assistant API",
        version="1.0.0"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check"""
    return HealthResponse(
        status="healthy",
        service="ERP Implementation Assistant API",
        version="1.0.0"
    )


@app.get("/api/metadata", response_model=MetadataResponse)
async def get_metadata():
    """Get API metadata and capabilities"""
    return MetadataResponse(
        version="1.0.0",
        capabilities={
            "query_types": ["configuration", "troubleshooting", "best_practices", "general"],
            "modules": ["OIS", "PPS", "MMS", "CRS", "MWS", "ARS", "APS", "GLS"],
            "streaming": True,
            "conversation_memory": False  # Will add later
        },
        model="gpt-4o-mini",
        knowledge_base={
            "documents": 4,
            "chunks": 6360,
            "last_updated": "2024-10-28"
        }
    )


# Main Query Endpoint
@app.post("/api/query", response_model=QueryResponse)
async def query_assistant(request: QueryRequest):
    """
    Process a query and return AI-generated response
    
    This is the main endpoint called by the H5 widget
    """
    import time
    start_time = time.time()
    
    try:
        agent = get_agent()
        
        # Get response from agent
        response, messages = agent.run(
            request.query,
            conversation_history=request.conversation_history
        )
        
        # Classify query type
        query_type = agent.classify_query_type(request.query)
        
        # Detect relevant modules
        modules = agent.detect_relevant_modules(request.query)
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Extract sources (simplified - could be enhanced)
        sources = ["M3 Documentation"]  # TODO: Extract actual source docs
        
        return QueryResponse(
            answer=response,
            query_type=query_type,
            modules=modules if modules else ["General"],
            sources=sources,
            response_time=response_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


# Streaming Endpoint (for future use)
@app.post("/api/query/stream")
async def query_assistant_stream(request: QueryRequest):
    """
    Streaming version of query endpoint
    Returns Server-Sent Events (SSE) for real-time response
    """
    async def generate():
        try:
            agent = get_agent()
            
            # Start with metadata
            yield f"data: {json.dumps({'type': 'start', 'query': request.query})}\n\n"
            
            # Get response (non-streaming for now - can enhance later)
            response, messages = agent.run(request.query)
            
            # Stream response in chunks
            chunk_size = 50
            for i in range(0, len(response), chunk_size):
                chunk = response[i:i+chunk_size]
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
                await asyncio.sleep(0.05)  # Small delay for smooth streaming
            
            # Send completion
            query_type = agent.classify_query_type(request.query)
            modules = agent.detect_relevant_modules(request.query)
            
            yield f"data: {json.dumps({
                'type': 'done',
                'query_type': query_type,
                'modules': modules
            })}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler"""
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler"""
    return {
        "error": "Internal server error",
        "detail": str(exc),
        "status_code": 500
    }


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    
    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║  ERP Implementation Assistant API                         ║
    ║                                                           ║
    ║  Starting server...                                       ║
    ║  API Docs: http://localhost:{port}/docs                       ║
    ║  Health:   http://localhost:{port}/health                     ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
