import os
from pdf import load_pdf
from lengthbasesplitting import split_documents
from vecterstore import create_vectorstore

folder = r"C:\Users\786\Desktop\New folder (5)\dataset"
all_docs = []
for filename in os.listdir(folder):
    if filename.endswith(".pdf"):
        path = os.path.join(folder, filename)
        docs = load_pdf(path)
        all_docs.extend(docs)
        print(f"Loaded {filename}: {len(docs)} pages")

chunks = split_documents(all_docs)
vectorstore = create_vectorstore(chunks)
print(f"Vectorstore created with {len(chunks)} chunks from {len(all_docs)} pages total")