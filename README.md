# 🧠 Intelligent Document QA Assistant

> A smart assistant that can handle `.txt`, `.pdf`, and `.docx` documents — and intelligently answer user queries based on them.

This project is completely **free** to use, but it leverages **SerpAPI** for up to **100 requests/month** and **OpenRouter** for up to **50 requests/month**. These services provide essential capabilities, and the free tiers should be enough for basic usage.

---

## 🎥 Video Preview

Check out the video below to see the **Intelligent Document QA Assistant** in action! Watch as it processes documents and generates smart responses based on user queries.

[![Watch the Demo](https://img.youtube.com/vi/HANnxs0kN7Q/0.jpg)](https://youtu.be/HANnxs0kN7Q)

> **Note**: The video demonstrates how the assistant works with different files, as well as its intelligent querying capabilities using SerpAPI and Google AI Overview and efficient document retrieval.

---

## ✨ Features

- 🗂️ **Supports** `.txt`, `.pdf`, and `.docx` files and documents provided in user prompts for maximum flexibility
- 🧠 **Understands** user prompts — even with or without attached documents
- 📦 **Vector storage** via [ChromaDB](https://www.trychroma.com/)
- 🌍 **Smart fallback** using **SerpAPI** and **Google AI Overview** for enriching results
- 🛠️ **Flexible & extendable architecture** — adapt it to your needs
- ⚡ **Powered by** [OpenRouter](https://openrouter.ai/) and [SerpAPI](https://serpapi.com/) for seamless integrations
- 💡 **Automatically summarizes, filters**, and stores relevant data for optimal results

---

## ⚙️ How It Works

### 📁 When the user provides a document or includes content in the prompt:

- If **related to the theme**:
  - ➕ Add to Chroma vector store
  - 🧾 Generate a summary
- If **unrelated**:
  - ❌ Inform the user

### 💬 When the user enters a prompt (without a document):

- If the prompt is **related** to the theme:
  - If **similar documents exist** in Chroma:
    - ✅ Answer is generated based on those docs
  - If **no related docs**:
    - 🔎 Use SerpAPI:
      - If **Google AI Overview is available**:
        - ✅ Use overview responses
      - Else:
        - 🕵️ Use default SerpAPI responses

---

## 🚀 Installation

> 🧰 **Before you begin**  
> Make sure you have **Python** and **Node.js** installed on your system. I have **Python (3.11.0)** and **Node.js (v22.13.0)** 
> You can check your versions by running:
> ```bash
> python --version
> node --version
> ```

### 🧑‍💻 Clone the repository

Start by cloning the repository:

```bash
git clone https://github.com/mweglowski/concert_rag.git
cd concert_rag
```

### ⚙️ Backend Setup (Python + FastAPI)

**Set up the virtual environment**

Linux/macOS:
```bash
cd backend
python -m venv venv
source venv/bin/activate

```

Windows (PowerShell):
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows (CMD):
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate.bat
```

### 🎨 Frontend Setup (React + Vite + TypeScript)

```bash
cd frontend
npm install
npm run dev
```
> 🟢 This will start your Vite development server on http://localhost:5173 by default.

### 📦 Install dependencies

Once the virtual environment is activated, you can install all necessary dependencies by running:

```bash
pip install -r requirements.txt
```

> 💡 **Chroma Setup Issues?**  
> Using Chroma **locally** requires **Rust**, **C++ build tools**, and additional dependencies. On **Windows**, this commonly leads to:
> `error: Could not build wheels for hnswlib...`  
> 🔗 [Fix thread here](https://stackoverflow.com/questions/73969269/error-could-not-build-wheels-for-hnswlib-which-is-required-to-install-pyprojec/76245995#76245995)

To **avoid pain**, you can try running it on docker 🐳. It's clean and platform-independent, but I will not dive into it here.

### 📝 Description of packages in requirements.txt

- **`fastapi`**: A high-performance web framework for building APIs with Python 3.6+.
- **`uvicorn`**: Fast ASGI server for serving FastAPI applications asynchronously.
- **`chromadb`**: A vector database for efficient document and text embeddings storage.
- **`requests`**: HTTP library for making requests to external APIs (e.g., SerpAPI, OpenRouter).
- **`sentence-transformers`**: Computes sentence and document embeddings for vector representation.
- **`pydantic`**: Data validation and settings management using Python type hints.
- **`python-dotenv`**: Reads environment variables from `.env` files for secure config management.
- **`langchain-community`**: Framework for working with LLMs and integrating documents for intelligent search.
- **`langchain-experimental`**: Experimental functionality in Langchain for advanced use cases.
- **`langchain-huggingface`**: Integrates Hugging Face models with Langchain for text processing.
- **`openai`**: Python client for interacting with OpenAI's API, here used for OpenRouter services.
- **`google-search-results`**: Python client for querying Google search results via SerpAPI.
- **`python-multipart`**: Handles multi-part form data (e.g., file uploads) in FastAPI.
- **`python-docx`**: Library for reading and writing `.docx` files.
- **`pymupdf`**: Python binding for MuPDF to process PDF documents.

---

## 🔑 Configuration

Before running the backend, ensure you have set up the following **environment variables** in your /backend/.env file:

```env
SERPAPI_API_KEY=your_serpapi_key

OPENROUTER_API_KEY=your_openrouter_api_key
```

---

## 🧱 Tech Stack

### ⚙️ Backend

- **Python 3.11**: Clean syntax, async capabilities, and a rich ecosystem for fast development.
- **FastAPI**: Modern web framework for building APIs with async support and automatic documentation.
- **Uvicorn**: Lightning-fast ASGI server to run FastAPI applications.
- **Pydantic**: Data validation and settings management using Python's type hints.
- **ChromaDB**: Lightweight vector store for handling document embeddings.
- **Sentence-Transformers**: Converts documents into embeddings using transformer models.
- **Requests**: Simple HTTP requests to external APIs for data fetching (SerpAPI, OpenRouter).

### 🎨 Frontend

- **React**: Component-based UI library for building interactive web interfaces.
- **Vite**: Fast development server and build tool for modern web projects.
- **TypeScript**: Statically typed superset of JavaScript for more robust code.
  
### 🔧 DevOps & Deployment

- **python-dotenv**: Managing environment variables and configuration securely.
  
### 🌐 External API Integrations

- **SerpAPI**: 100 free search requests per month for querying Google search results.
- **OpenRouter**: 50 free requests per month for integrating AI-powered responses (free, because we are using gemini-2.0-flash-exp to which requests are free on openrouter).
  
### 🧠 AI/ML

- **Langchain**: Framework for working with LLMs to process and analyze documents and prompts.
- **OpenRouter API**: Used for generating AI-based responses using GPT models.
- **Hugging Face**: Integration for using transformer models for text processing.

---

## 🎉 Have Fun!

Now that everything’s set up, it’s time to explore and have fun with the **Intelligent Document QA Assistant**! 🤖💬

- Upload a document 📄 and ask questions about it 🧐.
- Get smart, concert-related answers 🎶🎤.
- Experiment with different documents, and see how it summarizes and responds to your prompts! 🎉

Remember, this project is all about making document queries smarter and fun — so dive in and see what you can do! 😎

**ENJOY!** 🚀
