from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader

loader = DirectoryLoader(
    r"C:\Users\786\Desktop\New folder (5)\dataset",
    glob="*.pdf",
    loader_cls=PyPDFLoader
)
documents = loader.load()

print(documents[0].page_content)
print(len(documents))