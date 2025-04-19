from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=openrouter_api_key,
)

def summarize_text(text: str) -> str:
    """
    Generate a detailed summary for long concert-related texts by chunking.
    Focuses on preserving key information like dates, bands, tours, places, concerts, and artists. 
    The summary is presented in clean, structured HTML format.

    Args:
        text (str): The concert-related text to be summarized.

    Returns:
        str: A detailed, HTML-structured summary containing key information.
    
    The summary is structured using HTML elements like <div>, <p>, <span>, <strong>, <br />, <ul>, and <li>.
    The generated summary will prioritize clarity and readability with minimal HTML formatting.
    """

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Generate detailed summary focusing on preserving key info like dates, bands, tours, places, concerts, artists of text provided. Present it in clean and structured html only using div, p, span, strong, br, ul, li. Use more <br /> and do not include  ```html ```, begin with just elements. Text: {text}"
                }
            ]
        }
    ]
    
    completion = client.chat.completions.create(
        model="google/gemini-2.0-flash-exp:free",
        messages=messages
    )
    
    return completion.choices[0].message.content