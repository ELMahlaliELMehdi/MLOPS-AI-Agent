import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.calculator import calculate
from tools.weather import get_weather
from tools.wiki import search_wikipedia
from tools.datetime_tool import get_current_datetime, calculate_date_difference

def decide_tool(query: str) -> str:
    """
    Decide which tool to use based on keywords in the query.
    Returns: tool name
    """
    query_lower = query.lower()
    
    # Calculator keywords
    if any(keyword in query_lower for keyword in ['calculate', 'compute', 'math', '+', '-', '*', '/', 'sum', 'multiply', 'divide']):
        return 'calculator'
    
    # Weather keywords
    elif any(keyword in query_lower for keyword in ['weather', 'temperature', 'forecast', 'rain', 'sunny', 'climate']):
        return 'weather'
    
    # Wikipedia keywords
    elif any(keyword in query_lower for keyword in ['wiki', 'wikipedia', 'who is', 'what is', 'tell me about', 'information about']):
        return 'wikipedia'
    
    # DateTime keywords
    elif any(keyword in query_lower for keyword in ['date', 'time', 'today', 'current time', 'what day', 'difference between']):
        return 'datetime'
    
    else:
        return 'unknown'

def extract_params(query: str, tool: str) -> dict:
    """
    Extract parameters from the query based on the tool.
    """
    query_clean = query.strip()
    
    if tool == 'calculator':
        # Extract math expression (remove words like "calculate", "what is", etc.)
        for word in ['calculate', 'compute', 'what is', 'solve', 'math']:
            query_clean = query_clean.lower().replace(word, '').strip()
        return {'expression': query_clean}
    
    elif tool == 'weather':
        # Extract city name
        for word in ['weather in', 'weather', 'temperature in', 'forecast for']:
            query_clean = query_clean.lower().replace(word, '').strip()
        return {'city': query_clean}
    
    elif tool == 'wikipedia':
        # Extract topic
        for word in ['wiki', 'wikipedia', 'who is', 'what is', 'tell me about', 'information about']:
            query_clean = query_clean.lower().replace(word, '').strip()
        return {'query': query_clean}
    
    elif tool == 'datetime':
        # For now, just return current datetime
        return {}
    
    return {}

def run_tool(tool_name: str, params: dict) -> dict:
    """
    Execute the selected tool with parameters.
    """
    try:
        if tool_name == 'calculator':
            return calculate(params.get('expression', ''))
        
        elif tool_name == 'weather':
            return get_weather(params.get('city', 'London'))
        
        elif tool_name == 'wikipedia':
            return search_wikipedia(params.get('query', ''))
        
        elif tool_name == 'datetime':
            return get_current_datetime()
        
        elif tool_name == 'unknown':
            return {
                'success': False,
                'error': 'Could not determine which tool to use. Try asking about weather, calculations, Wikipedia, or date/time.'
            }
        
        else:
            return {
                'success': False,
                'error': f'Unknown tool: {tool_name}'
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def process_query(query: str) -> dict:
    """
    Main function: decide tool, extract params, run tool, return result.
    """
    # Step 1: Decide which tool to use
    tool = decide_tool(query)
    
    # Step 2: Extract parameters
    params = extract_params(query, tool)
    
    # Step 3: Run the tool
    result = run_tool(tool, params)
    
    # Step 4: Return structured response
    return {
        'query': query,
        'tool_used': tool,
        'params': params,
        'result': result
    }

# Test it
if __name__ == "__main__":
    # Test different queries
    test_queries = [
        "Calculate 25 + 17",
        "What is the weather in Paris?",
        "Tell me about Machine Learning",
        "What is the current date?",
        "Hello, how are you?"  # Should return unknown
    ]
    
    for q in test_queries:
        print(f"\nQuery: {q}")
        response = process_query(q)
        print(f"Tool: {response['tool_used']}")
        print(f"Result: {response['result']}")
        print("-" * 50)