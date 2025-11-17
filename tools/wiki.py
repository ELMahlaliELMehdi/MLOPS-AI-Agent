import wikipedia

def search_wikipedia(query: str, sentences: int = 3) -> dict:
    """
    Search Wikipedia and return a summary.
    """
    try:
        # Search for the topic
        search_results = wikipedia.search(query, results=1)
        
        if not search_results:
            return {
                "success": False,
                "error": "No results found"
            }
        
        # Get the page
        page = wikipedia.page(search_results[0], auto_suggest=False)
        
        # Get summary
        summary = wikipedia.summary(search_results[0], sentences=sentences)
        
        return {
            "success": True,
            "title": page.title,
            "summary": summary,
            "url": page.url
        }
    except wikipedia.exceptions.DisambiguationError as e:
        # Multiple results - pick the first one
        try:
            page = wikipedia.page(e.options[0])
            summary = wikipedia.summary(e.options[0], sentences=sentences)
            return {
                "success": True,
                "title": page.title,
                "summary": summary,
                "url": page.url
            }
        except:
            return {
                "success": False,
                "error": "Disambiguation error"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

