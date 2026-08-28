import streamlit as st
import os
import tempfile
from rag_engine import RAGEngine

st.set_page_config(page_title="Ask My Notes", page_icon="📚", layout="centered")

st.title("📚 Ask My Notes (RAG + LLM)")
st.write("Upload a PDF document and ask questions about it. The AI will answer using *only* the context from your document.")

# Sidebar for configuration / upload
with st.sidebar:
    st.header("Configuration")
    uploaded_file = st.file_uploader("Upload a PDF (or use default)", type=["pdf"])
    
    chunk_size = st.slider("Chunk Size (Words)", min_value=50, max_value=500, value=100, step=10)
    overlap = st.slider("Chunk Overlap", min_value=0, max_value=100, value=20, step=5)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "engine" not in st.session_state:
    st.session_state.engine = None
if "current_pdf_name" not in st.session_state:
    st.session_state.current_pdf_name = None

# Logic to initialize or update the RAG engine
target_pdf_path = "data/notes.pdf"
pdf_name = "Default Notes (data/notes.pdf)"

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    target_pdf_path = temp_path
    pdf_name = uploaded_file.name

# Re-initialize engine if the PDF or parameters changed
if st.session_state.engine is None or st.session_state.current_pdf_name != pdf_name:
    with st.spinner(f"Processing '{pdf_name}'... Building vector store..."):
        try:
            st.session_state.engine = RAGEngine(
                pdf_path=target_pdf_path, 
                chunk_size=chunk_size, 
                overlap=overlap
            )
            st.session_state.current_pdf_name = pdf_name
            st.success("Knowledge base ready!")
        except Exception as e:
            st.error(f"Error initializing RAG Engine: {e}")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask a question about the document..."):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Searching document and thinking..."):
            if st.session_state.engine:
                try:
                    result = st.session_state.engine.query(prompt)
                    answer = result["answer"]
                    sources = result["sources"]
                    
                    source_str = f"*(Sources: Pages {', '.join(map(str, sources))})*"
                    full_response = f"{answer}\n\n{source_str}"
                    
                    st.markdown(full_response)
                    
                    with st.expander("View Retrieved Context"):
                        st.text(result["context_used"])
                        
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    error_msg = f"An error occurred: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
            else:
                st.error("RAG engine is not initialized.")
