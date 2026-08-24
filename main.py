from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_pages(pdf_path):
    reader = PdfReader(pdf_path)

    pages = []

    for index, page in enumerate(reader.pages):
        page_data = {
            "page": index + 1,
            "text": page.extract_text()
        }
        pages.append(page_data)

    return pages
pages = extract_pages("data/notes.pdf")



def chunk_pages(pages,chunk_size,overlap):

    chunks=[]
    c_count=0

    for page_data in pages:
        text=page_data["text"].strip()

        if text:
            words=text.split()

            for start in range(0,len(words),chunk_size-overlap):
                chunk_words=words[start:start+chunk_size]

                chunk_data={
                    "chunk_id": c_count,
                    "page": page_data["page"],
                    "text": " ".join(chunk_words)
                }
                chunks.append(chunk_data)
                c_count+=1
    return chunks

chunk_size=100
overlap=20
chunks=chunk_pages(pages,chunk_size,overlap)
# print("number of pages:", len(pages))
# print("number of chunks:", len(chunks))
# print(chunks[0])
# print(chunks[1])
# print(chunks[2])

texts=[chunk["text"] for chunk in chunks]
embeddings=model.encode(texts)

dimensions=embeddings.shape[1]
index=faiss.IndexFlatL2(dimensions)
index.add(embeddings)
# print(index.ntotal)


query = "What is an API?"


query_embedding = model.encode([query])

k = 5
distances, indices = index.search(query_embedding, k)

# print(indices)
# print(distances)

for i in indices[0]:
    print(chunks[i])