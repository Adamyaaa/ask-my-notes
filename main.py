from pypdf import PdfReader

reader = PdfReader("data/notes.pdf")

pages=[]

for index,page in enumerate(reader.pages):
    page_data={
        "page": index+1,
        "text": page.extract_text()
    }
    pages.append(page_data)
chunks=[]
for page_data in pages:
    words=page_data["text"].split(" ")
    for start in range(0,len(words),100):
        chunk_words=words[start:start+100]

        chunk_data={
            "page": page_data["page"],
            "text": " ".join(chunk_words)
        }
        chunks.append(chunk_data)

print("number of pages:", len(pages))
print("number of chunks:", len(chunks))
print(chunks[0])
