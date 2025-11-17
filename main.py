from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from datetime import datetime
import time
from monitoring.experiment import experiment_tracker
import yaml
# Import agent logic
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agent.logic import process_query
from agent.memory import memory

# Import monitoring
from monitoring.metrics import (
    track_tool_usage, 
    track_error, 
    update_active_users,
    request_count,
    request_latency,
    generate_latest,
    CONTENT_TYPE_LATEST
)

# Create FastAPI app
app = FastAPI(
    title="Tool-Using AI Agent",
    description="An intelligent agent that uses multiple tools to answer questions",
    version="1.0.0"
)

# Request/Response models
class QueryRequest(BaseModel):
    query: str
    user_id: str = "default_user"

class QueryResponse(BaseModel):
    query: str
    tool_used: str
    result: dict
    timestamp: str
    processing_time: float

# Global stats
stats = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0
}

@app.get("/")
def root():
    """
    Welcome endpoint
    """
    return {
        "message": "Welcome to Tool-Using AI Agent API",
        "docs": "/docs",
        "endpoints": {
            "ask": "/ask",
            "history": "/history/{user_id}",
            "stats": "/stats",
            "health": "/health",
            "metrics": "/metrics"
        }
    }

@app.post("/ask", response_model=QueryResponse)
def ask_agent(request: QueryRequest):
    """
    Ask the agent a question.
    The agent will automatically choose the right tool.
    """
    start_time = time.time()
    
    try:
        # Track request
        request_count.labels(endpoint="/ask", method="POST").inc()
        
        # Update stats
        stats["total_requests"] += 1
        
        # Process the query
        result = process_query(request.query)
        
        # Track tool usage
        tool_name = result['tool_used']
        success = result['result'].get('success', False)
        track_tool_usage(tool_name, success)
        
        # Track latency
        processing_time = time.time() - start_time
        request_latency.labels(endpoint="/ask", tool=tool_name).observe(processing_time)
        
        # Log to MLflow
        experiment_tracker.log_request(tool_name, success, processing_time)
        
        # Store in memory
        memory.add_interaction(
            user_id=request.user_id,
            query=request.query,
            response=result
        )
        
        # Update active users count
        update_active_users(len(memory.conversations))
        
        # Check if successful
        if success:
            stats["successful_requests"] += 1
        else:
            stats["failed_requests"] += 1
            track_error(tool_name, "tool_execution_failed")
        
        return QueryResponse(
            query=result['query'],
            tool_used=result['tool_used'],
            result=result['result'],
            timestamp=datetime.now().isoformat(),
            processing_time=round(processing_time, 3)
        )
    
    except Exception as e:
        stats["failed_requests"] += 1
        track_error("unknown", "internal_error")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{user_id}")
def get_history(user_id: str):
    """
    Get conversation history for a user.
    """
    request_count.labels(endpoint="/history", method="GET").inc()
    history = memory.get_history(user_id)
    return {
        "user_id": user_id,
        "history_count": len(history),
        "history": history
    }

@app.delete("/history/{user_id}")
def clear_history(user_id: str):
    """
    Clear conversation history for a user.
    """
    request_count.labels(endpoint="/history", method="DELETE").inc()
    memory.clear_history(user_id)
    return {
        "message": f"History cleared for user: {user_id}"
    }

@app.get("/stats")
def get_stats():
    """
    Get API usage statistics.
    """
    request_count.labels(endpoint="/stats", method="GET").inc()
    return stats

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    request_count.labels(endpoint="/health", method="GET").inc()
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/metrics")
def metrics():
    """
    Prometheus metrics endpoint
    """
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.on_event("startup")
async def startup_event():
    """
    Start MLflow experiment on startup
    """
    experiment_tracker.start_experiment(run_name=f"api_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    print("✅ MLflow experiment started")

@app.on_event("shutdown")
async def shutdown_event():
    """
    End MLflow experiment on shutdown
    """
    experiment_tracker.end_experiment()
    print("✅ MLflow experiment ended")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)