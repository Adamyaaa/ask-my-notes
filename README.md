# Ask My Notes (RAG + LLM)

A completed, modular implementation of Retrieval-Augmented Generation (RAG) using local vector embeddings (FAISS) and Google Gemini as the LLM. 

This project allows you to query your personal PDF notes and get AI-generated answers based *strictly* on the context retrieved from the documents.

## Features
- **PDF Extraction**: Reads text directly from uploaded PDFs.
- **Chunking Strategy**: Configurable chunk size and overlap for optimal context retrieval.
- **Vector Database**: Uses FAISS for lightning-fast similarity search.
- **Embeddings**: Uses `sentence-transformers` (`all-MiniLM-L6-v2`) to create high-quality vector embeddings.
- **LLM Integration**: Uses Google's Gemini Flash model to synthesize answers based on retrieved context.
- **Dual Interfaces**: Includes both a fast Command-Line Interface (CLI) and a rich Web Interface (Streamlit).

## Setup & Installation

1. Create a virtual environment and activate it (recommended):
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Make sure you have `streamlit` installed for the web app: `pip install streamlit`)*

3. Create a `.env` file in the root directory and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

### 1. Web Application (Streamlit)
For a completed, production-like interface, use the Streamlit app. It supports drag-and-drop PDF uploads and chat history.
```bash
streamlit run app.py
```

### 2. Command Line Interface (CLI)
For quick, terminal-based interaction:
```bash
python main.py --pdf data/notes.pdf
```
Type your questions at the prompt and type `exit` to quit.

## Project Structure
- `rag_engine.py`: The core RAG pipeline (Object-Oriented).
- `main.py`: CLI wrapper for the RAG engine.
- `app.py`: Streamlit web interface.
- `data/`: Directory containing default PDF notes.
