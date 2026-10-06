from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader
loader = DirectoryLoader("C:\\Users\\786\\Downloads",
                         glob="*.pdf",
                         loader_cls=PyPDFLoader)
documents = loader.load()
print(documents[0].page_content)
print(len(documents))