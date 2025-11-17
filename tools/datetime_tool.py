from datetime import datetime, timedelta
from dateutil import parser

def get_current_datetime() -> dict:
  
    now = datetime.now()
    return {
        "success": True,
        "datetime": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day_of_week": now.strftime("%A"),
        "timezone": "UTC"
    }

def calculate_date_difference(date1_str: str, date2_str: str) -> dict:
    """
    Calculate difference between two dates.
    Example: "2024-01-01" and "2024-12-31"
    """
    try:
        date1 = parser.parse(date1_str)
        date2 = parser.parse(date2_str)
        
        difference = abs((date2 - date1).days)
        
        return {
            "success": True,
            "date1": date1.strftime("%Y-%m-%d"),
            "date2": date2.strftime("%Y-%m-%d"),
            "difference_days": difference
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

