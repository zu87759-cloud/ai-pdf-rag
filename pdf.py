from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

if __name__ == "__main__":
    docs = load_pdf("Zain_ul_Abidin_CV.pdf")  # or your study notes PDF
    print(f"Loaded {len(docs)} pages")
    print(docs[0].page_content[:300])