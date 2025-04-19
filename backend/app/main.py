from fastapi import (
    FastAPI,
    Request,
    UploadFile,
    Form,
    File,
)
from fastapi.middleware.cors import CORSMiddleware

from .services.file_processor import process_file
from .services.summarizer import summarize_text
from .services.vector_store import store_to_chroma, answer_question
from .services.search import search_online
from .utils.classifier import get_prompt_type, is_concert_related

app = FastAPI(
    title="Concert RAG Bot",
    description="RAG for answering concert related questions (2025-2026).",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Concert RAG API!"}

@app.post("/interact")
async def interact(
    prompt: str = Form(default=None),
    file: UploadFile = File(default=None)
):
    """
    Main route for user interaction with the concert-related RAG system.

    Args:
        prompt (str, optional): A user-inputted prompt (such as a question or text).
        file (UploadFile, optional): A file uploaded by the user that may contain concert-related information.

    Returns:
        dict: A response message with either a summary, answer, or an out-of-context notice.

    Logic:

    When the user provides a document or includes content in the prompt:

    - If related to the theme (concerts and tours):
      - Add to Chroma vector store
      - Generate a summary and store it
    - If unrelated:
      - Inform the user that the content is out of context and not added

    When the user enters a prompt (without a document):

    - If the prompt is related to the theme (concerts and tours):
      - If similar documents exist in Chroma:
        - Answer is generated using relevant documents from Chroma
      - If no related documents:
        - Perform a search using SerpAPI:
          - If Google AI Overview is available:
            - Use AI-powered overview responses
          - Else:
            - Use default SerpAPI responses for more general results
    - If unrelated:
      - Inform the user that the prompt is out of context
    """

    file_text = ""
    file_summary = ""
    file_related = False

    if file:
        content = await file.read()
        file_text = process_file(file.filename, content)
        
        if is_concert_related(file_text):
            summary = summarize_text(file_text)
            store_to_chroma(summary)

            return {"message": f"Thank you! Document ingested. Here's a summary:\n{summary}"}
        else:
            return {"message": "Sorry, the uploaded document is out of context and was not added."}

    if prompt:
        prompt_type = get_prompt_type(prompt)

        if prompt_type == "document":
            if is_concert_related(prompt):
                summary = summarize_text(prompt)
                store_to_chroma(summary)

                return {"message": f"Thank you! Document ingested. Here's a summary:\n{summary}"}
            else:
                return {"message": "Sorry, the provided text is out of context and was not added."}

        elif prompt_type == "question":
            if is_concert_related(prompt):
                answer = answer_question(prompt)

                if "docs not relevant" not in answer.lower():
                    return {"message": answer}
                else:
                    # print("serpapi search...")
                    online_result = search_online(prompt)

                    if online_result:
                        return {"message": online_result}
            else:
                return {"message": "Sorry, I couldn’t provide an answer. The message is out of theme context."}
        
        else:
            return {"message": "Sorry, the input seems out of context. Please upload a concert-related document or ask a specific question."}

    return {"message": "Please upload a file or enter text."}
