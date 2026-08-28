import sys
import argparse
from rag_engine import RAGEngine

def main():
    parser = argparse.ArgumentParser(description="Ask My Notes - RAG CLI")
    parser.add_argument("--pdf", type=str, default="data/notes.pdf", help="Path to the PDF file")
    args = parser.parse_args()

    print("\n--- Ask My Notes ---")
    print(f"Initializing AI and reading '{args.pdf}'...")
    
    try:
        engine = RAGEngine(pdf_path=args.pdf)
    except Exception as e:
        print(f"Error initializing RAG Engine: {e}")
        sys.exit(1)
        
    print("\nReady! Ask questions about your notes. Type 'exit' or 'quit' to stop.")
    
    while True:
        try:
            query = input("\nQ: ").strip()
            if query.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            if not query:
                continue
                
            print("Thinking...")
            result = engine.query(query)
            
            print(f"\nA: {result['answer']}")
            print(f"(Sources: Pages {', '.join(map(str, result['sources']))})")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()