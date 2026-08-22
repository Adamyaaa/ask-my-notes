from pypdf import PdfReader

reader = PdfReader("data/notes.pdf")
mylist=[]
for page in reader.pages:
    mylist.append(page.extract_text())
print(len(mylist))

