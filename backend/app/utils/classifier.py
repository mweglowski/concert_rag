from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

llm = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key,
)

def classify(text: str, classification_prompt: str) -> str:
    """
    Generic classifier using OpenRouter and a classification prompt.
    """
    response = llm.chat.completions.create(
        model="google/gemini-2.0-flash-exp:free",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{classification_prompt}\n\n{text}"
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content.strip().lower()


def is_concert_related(text: str) -> bool:
    """
    Determines if the provided text is about concerts/tours.
    """
    prompt = (
        "Answer 'yes' or 'no' only. Is the following text related to music concerts, tours, venues, "
        "or artist performance schedules in 2025 or 2026?"
    )
    result = classify(text, prompt)
    return "yes" in result


def get_prompt_type(text: str) -> bool:
    """
    Classifies whether the input is a document (not a question).
    """
    prompt = (
        "'document', 'question' or 'unknown'. Is the following input a document (a text describing something) "
        "or a question (asking something)? or unknown (something different). A document could be a prompt like: Please ingest a document ->  Lady Gaga - The Chromatica Tour 2025 Event: Lady Gaga - Chromatica Tour: Seattle Edition Date: December 30, 2025 Venue: Climate Pledge Arena, Seattle, WA Special Note: As part of the tour’s North American leg, Lady Gaga will host an exclusive fan meet-and-greet session before the show, set to take place on the main stage — the largest and most technologically advanced in the region. Fans can expect a full stadium experience, featuring dazzling visuals, live band performances, and a curated setlist of Gaga's iconic hits including 'Rain on Me', 'Shallow', and 'Poker Face'."
    )
    prompt_type = classify(text, prompt)
    return prompt_type


def is_artist_query(text: str) -> bool:
    """
    Determines if the prompt is a question about a music artist's concert/tour.
    """
    prompt = (
        "Answer 'yes' or 'no'. Is the following question asking about a music artist's concert or tour schedule?"
    )
    result = classify(text, prompt)
    return "yes" in result

# print(is_prompt_document(""))
# print(is_concert_related("lady gaga will have some meetings with fans on the biggest stage in seattle! This concert will take place at 30 December 2025!"))
# print(get_prompt_type("where coldplay will have next concerts?"))