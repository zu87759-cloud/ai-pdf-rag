import os
import tempfile

import streamlit as st

from pdf import load_pdf
from lengthbasesplitting import split_documents
from vecterstore import create_vectorstore
from rag_chain import answer_question

# ---------- Page setup ----------
st.set_page_config(page_title="AI PDF Assistant", page_icon="📄", layout="centered")

st.title("📄 AI PDF Assistant")
st.caption("Upload a PDF and ask questions about it (RAG + LangChain + Groq)")

# ---------- 1. File uploader (header / top of the page) ----------
uploaded_file = st.file_uploader("Browse a PDF file", type="pdf")

if uploaded_file is None:
    st.info("Upload a PDF to start.")
    st.stop()

# ---------- 2. Process the PDF only once per file ----------
file_key = (uploaded_file.name, uploaded_file.size)

if st.session_state.get("file_key") != file_key:
    temp_path = None
    with st.spinner("Reading and indexing your PDF..."):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getbuffer())
                temp_path = tmp.name

            documents = load_pdf(temp_path)

            if not documents or not any(d.page_content.strip() for d in documents):
                st.error(
                    "No text could be extracted from this PDF. "
                    "It may be a scanned/image-only PDF."
                )
                st.stop()

            chunks = split_documents(
                documents,
                chunk_size=1500,
                chunk_overlap=150,
            )

            # CHECK: use the same call your old app.py used here
            vectorstore = create_vectorstore(chunks)

        except Exception as e:
            st.error(f"Could not process the PDF: {e}")
            st.stop()
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    st.session_state.vectorstore = vectorstore
    st.session_state.file_key = file_key
    st.session_state.messages = []
    st.success(f"Ready! Indexed {len(documents)} pages into {len(chunks)} chunks.")

# ---------- 3. Chat ----------
for msg in st.session_state.get("messages", []):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask a question about your PDF")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # CHECK: use the same call your old app.py used here
                answer = answer_question(question, st.session_state.vectorstore)
            except Exception as e:
                answer = f"Sorry, something went wrong: {e}"
        st.markdown(str(answer))

    st.session_state.messages.append({"role": "assistant", "content": str(answer)})