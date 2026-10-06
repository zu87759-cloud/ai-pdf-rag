from langchain_community.document_loaders import webbaseloader
loader = webbaseloader.WebBaseLoader("https://www.example.com")
documents = loader.load()
print(documents[0].page_content)