from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
from .summarizer import summarize_text
import requests
from typing import Optional

load_dotenv()
serpapi_api_key = os.getenv("SERPAPI_API_KEY")

def search_online(prompt: str) -> str:
    """
    Perform an online search for concerts and tours for the years 2025 and 2026, 
    and summarize the results using AI or default Google search results.

    Args:
        prompt (str): The search query to search for concerts and tours.

    Returns:
        str: A summarized text of the concert-related information found online.
    """

    search_query = f"{prompt} 2025 2026 concerts and tours"
    
    page_token = get_page_token(search_query)
    ai_answer = get_google_ai_answer(page_token)
    
    summarized_answer = ""
    if ai_answer:
        summarized_answer = summarize_text(ai_answer)
        # print("AI ANSWER SUMMARIZED:", summarized_answer)
        return summarized_answer
    else:
        default_results = get_default_results(search_query)
        summarized_answer = summarize_text(default_results)
        # print("DEFAULT SUMMARIZED:", summarized_answer)
        return summarized_answer
    

def get_page_token(search_query: str) -> Optional[str]:
    """
    Retrieve the page token for Google AI search results.

    Args:
        search_query (str): The search query used for fetching results.

    Returns:
        Optional[str]: The page token used for fetching Google AI search results,
                        or None if no token is available.
    """

    params = {
        "engine": "google",
        "q": search_query,
        "api_key": serpapi_api_key,
        "ai": 1,
        "hl": "en",
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("ai_overview", {}).get("page_token")

def get_google_ai_answer(page_token: Optional[str]) -> str:
    """
    Fetch AI-generated answers from Google AI overview, using the provided page token.

    Args:
        page_token (Optional[str]): The page token from previous search results.

    Returns:
        str: The AI-generated text block and references, or an empty string if no data is found.
    """

    params = {
        "engine": "google_ai_overview",
        "api_key": serpapi_api_key,
        "page_token": page_token
    }

    response = requests.get("https://serpapi.com/search", params=params)

    # print(response.json())

    try:
        data = response.json()["ai_overview"]
    except:
        return ""

    text_blocks = data.get("text_blocks", [])
    text_blocks_text = "\n".join([f"{block['snippet']}" for block in text_blocks])

    references = data.get("references", [])
    references_text = ""
    
    for reference in references:
        title = reference.get('title', 'No title available')
        snippet = reference.get('snippet', 'No snippet available')
        references_text += f"Title: {title}\nSnippet: {snippet}\n\n"

    return text_blocks_text + references_text

def get_default_results(search_query: str) -> str:
    """
    Fetch default search results from Google, when AI overview is unavailable.

    Args:
        search_query (str): The search query used for fetching results.

    Returns:
        str: A string containing default search results with titles and snippets.
    """

    params = {
        "engine": "google",
        "q": search_query,
        "api_key": serpapi_api_key,
        "hl": "en",
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    default_results = []
    for result in results.get("organic_results", []):
        title = result.get('title', 'No title available')
        snippet = result.get('snippet', 'No snippet available')
        default_results.append(f"Title: {title}\nSnippet: {snippet}\n")
    
    return "\n".join(default_results)