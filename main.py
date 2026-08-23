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
chunk_size=100
overlap=20

for page_data in pages:
    text=page_data["text"].strip()
    if text:
        words=text.split()
        for index,start in enumerate(range(0,len(words),chunk_size-overlap)):
            chunk_words=words[start:start+chunk_size]

            chunk_data={
                "chunk_id": index,
                "page": page_data["page"],
                "text": " ".join(chunk_words)
            }
            chunks.append(chunk_data)

# print("number of pages:", len(pages))
# print("number of chunks:", len(chunks))
print(chunks[0])
print(chunks[1])
print(chunks[2])
