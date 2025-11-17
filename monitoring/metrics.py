from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from functools import wraps
import time

# Define metrics
request_count = Counter(
    'agent_request_total',
    'Total number of requests to the agent',
    ['endpoint', 'method']
)

tool_usage = Counter(
    'agent_tool_usage_total',
    'Number of times each tool was used',
    ['tool_name']
)

request_latency = Histogram(
    'agent_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint', 'tool']
)

error_count = Counter(
    'agent_error_total',
    'Total number of errors',
    ['tool_name', 'error_type']
)

active_users = Gauge(
    'agent_active_users',
    'Number of active users'
)

successful_requests = Counter(
    'agent_successful_requests_total',
    'Total number of successful requests',
    ['tool_name']
)

def track_request(endpoint: str, method: str = "POST"):
    """
    Decorator to track request metrics
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Increment request counter
            request_count.labels(endpoint=endpoint, method=method).inc()
            
            # Track latency
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                # We'll add tool name after we know which tool was used
                request_latency.labels(endpoint=endpoint, tool="unknown").observe(duration)
        
        return wrapper
    return decorator

def track_tool_usage(tool_name: str, success: bool):
    """
    Track which tools are being used and their success rate
    """
    tool_usage.labels(tool_name=tool_name).inc()
    
    if success:
        successful_requests.labels(tool_name=tool_name).inc()

def track_error(tool_name: str, error_type: str):
    """
    Track errors by tool and type
    """
    error_count.labels(tool_name=tool_name, error_type=error_type).inc()

def update_active_users(count: int):
    """
    Update the number of active users
    """
    active_users.set(count)