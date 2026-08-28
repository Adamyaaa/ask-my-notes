import os
import faiss
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from google import genai
from dotenv import load_dotenv

class RAGEngine:
    def __init__(self, pdf_path: str, chunk_size: int = 100, overlap: int = 20):
        """
        Initializes the RAG Engine with a given PDF document.
        """
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size
        self.overlap = overlap
        
        self.pages = []
        self.chunks = []
        self.index = None
        
        self._initialize_knowledge_base()

    def _initialize_knowledge_base(self):
        """Extracts text, chunks it, and builds the FAISS vector index."""
        print(f"Loading document: {self.pdf_path}...")
        self._extract_pages()
        self._chunk_pages()
        self._build_vector_store()
        print("Knowledge base initialized successfully.")

    def _extract_pages(self):
        reader = PdfReader(self.pdf_path)
        for index, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                self.pages.append({
                    "page": index + 1,
                    "text": text
                })

    def _chunk_pages(self):
        c_count = 0
        for page_data in self.pages:
            text = page_data["text"].strip()
            if not text:
                continue
                
            words = text.split()
            for start in range(0, len(words), self.chunk_size - self.overlap):
                chunk_words = words[start:start + self.chunk_size]
                self.chunks.append({
                    "chunk_id": c_count,
                    "page": page_data["page"],
                    "text": " ".join(chunk_words)
                })
                c_count += 1

    def _build_vector_store(self):
        if not self.chunks:
            raise ValueError("No text chunks found to build the vector store.")
            
        texts = [chunk["text"] for chunk in self.chunks]
        embeddings = self.embed_model.encode(texts)
        
        dimensions = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimensions)
        self.index.add(embeddings)

    def retrieve(self, query: str, k: int = 5):
        """Retrieves top-k most relevant chunks for a given query."""
        query_embedding = self.embed_model.encode([query])
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.chunks):
                results.append(self.chunks[idx])
        return results

    def query(self, query: str) -> dict:
        """Answers a query using RAG."""
        retrieved_chunks = self.retrieve(query)
        
        context = ""
        sources = []
        for chunk in retrieved_chunks:
            context += f"Source (Page {chunk['page']}):\n{chunk['text']}\n\n"
            if chunk['page'] not in sources:
                sources.append(chunk['page'])
                
        prompt = f"""
        You are a helpful AI assistant answering questions based on provided notes.
        Answer the user's question using ONLY the provided context. If the answer is not contained in the context, say "I cannot find the answer in the provided notes."
        
        Context:
        {context}
        
        Question:
        {query}
        """
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        return {
            "answer": response.text,
            "sources": sources,
            "context_used": context
        }
