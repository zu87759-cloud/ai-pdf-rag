from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents, chunk_size=1500, chunk_overlap=150):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    chunks = splitter.split_documents(documents)
    return chunks


if __name__ == "__main__":
    from pdf import load_pdf

    docs = load_pdf("Zain_ul_Abidin_CV.pdf")

    chunks = split_documents(docs)

    print(f"Split into {len(chunks)} chunks")

    if chunks:
        print(chunks[0].page_content)