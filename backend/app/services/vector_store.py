import chromadb
from sentence_transformers import SentenceTransformer
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from openai import OpenAI
import uuid
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

client = chromadb.Client()

index_name = "concerts"

if index_name in [i.name for i in client.list_collections()]:
    client.delete_collection(index_name)

index = client.create_collection(
    name=index_name,
    metadata={"hnsw:space": "cosine"}
)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

chunker = SemanticChunker(HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))


client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=openrouter_api_key,
)

def get_llm_response(prompt: str, context: str) -> str:
    """
    Get the response from the model based on the provided prompt and context.

    Args:
        prompt (str): The user's question or prompt.
        context (str): The relevant context or documents to help answer the question.

    Returns:
        str: The generated response from the model in HTML format.
    
    This function checks if the provided documents are relevant to the question and generates a structured HTML response.
    """

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Check if docs provided in the context are relevant to question. If not return 'docs not relevant' else answer the following question based on the context. Present it in clean and structured html only using div, p, span, strong, br, ul, li. Use more <br /> and do not include  ```html ```, begin with just elements. Context:\n\n{context}\n\nQuestion: {prompt}"
                }
            ]
        }
    ]
    
    completion = client.chat.completions.create(
        model="google/gemini-2.0-flash-exp:free",
        messages=messages
    )
    
    return completion.choices[0].message.content

def store_to_chroma(text: str) -> None:
    """
    Store the text into Chroma by chunking the text and encoding each chunk into embeddings.

    Args:
        text (str): The text to be stored in the Chroma database.
    
    This function splits the provided text into chunks, encodes them using a pre-trained model, and stores the embeddings in Chroma.
    """

    chunks = chunker.split_text(text)

    text_embeddings = embedding_model.encode(chunks)

    index.add(
        embeddings=text_embeddings,
        documents=chunks,
        ids=[str(uuid.uuid4())[:15] for _ in chunks]
    )

    print(f"Successfully stored {len(chunks)} chunks in Chroma.")

def get_relevant_docs(prompt: str) -> List:
    """
    Retrieve the most relevant documents from the Chroma index based on the user's prompt.

    Args:
        prompt (str): The user's prompt or query to find relevant documents.

    Returns:
        List[str]: A list of relevant documents based on the prompt.
    
    This function generates an embedding for the prompt, queries the Chroma collection, and retrieves the top matching documents.
    """

    query_embedding = embedding_model.encode([prompt])

    results = index.query(query_embeddings=query_embedding, n_results=2)
    
    # print("All Docs:", index.get())
    # print("Relevant Docs:", results)
    
    return results["documents"] if results["documents"] else []

def answer_question(prompt: str) -> str:
    """
    Answer a question by retrieving relevant documents from Chroma and generating a response using openrouter.

    Args:
        prompt (str): The user's question to be answered.

    Returns:
        str: The generated answer based on the relevant documents.
    
    This function combines document retrieval from Chroma and response generation from the model to provide a complete answer.
    """

    relevant_docs = get_relevant_docs(prompt)

    return get_llm_response(prompt, str(relevant_docs))
