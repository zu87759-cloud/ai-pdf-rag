from langchain_community.document_loaders import PyPDFLoader

cv_docs = PyPDFLoader(r"C:\Users\786\Desktop\New folder (5)\dataset\Zain_ul_Abidin_CV.pdf").load()
gold_docs = PyPDFLoader(r"C:\Users\786\Desktop\New folder (5)\dataset\pakistan_gold_prices_last_1_year (1).pdf").load()

print(len(cv_docs), len(gold_docs))
print(cv_docs[0].page_content[:300])
print(gold_docs[0].page_content[:300])

all_docs = cv_docs + gold_docs