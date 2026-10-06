import streamlit as st
import tempfile
import os

from pdf import load_pdf
from lengthbasesplitting import split_documents
from vecterstore import create_vectorstore
from rag_chain import answer_question


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI PDF Assistant",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("📚 AI PDF Assistant")

    st.write(
        "Upload a PDF and ask questions about its content."
    )

    st.divider()

    # PDF uploader
    uploaded_file = st.file_uploader(
        "📄 Upload your PDF",
        type=["pdf"]
    )

    # Process uploaded PDF
    if uploaded_file is not None:

        # Only process when a new PDF is uploaded
        if st.session_state.pdf_name != uploaded_file.name:

            with st.spinner("Processing PDF..."):

                # Create temporary file
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_file:

                    temp_file.write(uploaded_file.getbuffer())

                    temp_path = temp_file.name

                try:

                    # Load PDF
                    documents = load_pdf(temp_path)

                    # Split PDF
                    chunks = split_documents(
                        documents,
                        chunk_size=500,
                        chunk_overlap=50
                    )

                    # Create Chroma vectorstore
                    vectorstore = create_vectorstore(chunks)

                    # Save in session
                    st.session_state.vectorstore = vectorstore
                    st.session_state.pdf_name = uploaded_file.name

                    # Clear old conversation
                    st.session_state.messages = []

                    st.success("PDF processed successfully!")

                finally:

                    # Remove temporary PDF
                    if os.path.exists(temp_path):
                        os.remove(temp_path)


    st.divider()

    # Show uploaded PDF
    if st.session_state.pdf_name:

        st.subheader("📄 Current PDF")

        st.write(
            f"**{st.session_state.pdf_name}**"
        )

        st.divider()

    # Clear chat
    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# -----------------------------
# Main Interface
# -----------------------------
st.title("🤖 AI PDF Assistant")

st.caption(
    "Upload a PDF and ask questions about its content."
)


# -----------------------------
# Check PDF
# -----------------------------
if st.session_state.vectorstore is None:

    st.info(
        "👈 Please upload a PDF from the sidebar to start chatting."
    )

    st.stop()


# -----------------------------
# Display Chat History
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# -----------------------------
# Chat Input
# -----------------------------
question = st.chat_input(
    "Ask a question about your PDF..."
)


if question:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Display user question
    with st.chat_message("user"):

        st.write(question)


    # Generate answer
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            # Previous conversation
            history = st.session_state.messages[:-1]

            answer = answer_question(
                question,
                vectorstore=st.session_state.vectorstore,
                history=history
            )

        st.write(answer)


    # Save assistant answer
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
