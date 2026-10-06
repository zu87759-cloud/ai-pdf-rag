from groq import Groq
from dotenv import load_dotenv
import os


# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()


# -----------------------------
# Groq API
# -----------------------------
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Check your .env file."
    )

client = Groq(api_key=api_key)


# -----------------------------
# Answer Question
# -----------------------------
def answer_question(question, vectorstore, history=None, k=3):

    # Search the uploaded PDF
    results = vectorstore.similarity_search(
        question,
        k=k
    )

    # Create context from retrieved chunks
    context = "\n\n".join(
        [doc.page_content for doc in results]
    )


    # -----------------------------
    # Conversation History
    # -----------------------------
    conversation = ""

    if history:

        for message in history:

            conversation += (
                f"{message['role'].capitalize()}: "
                f"{message['content']}\n"
            )


    # -----------------------------
    # Prompt
    # -----------------------------
    prompt = f"""
You are an AI PDF Assistant.

Your job is to answer the user's question using
ONLY the information contained in the uploaded PDF.

You may also use the previous conversation to
understand follow-up questions.

If the answer cannot be found in the uploaded PDF,
say:

"I couldn't find that information in the uploaded PDF."

Do NOT make up information.

-----------------------------
PDF CONTENT
-----------------------------
{context}

-----------------------------
PREVIOUS CONVERSATION
-----------------------------
{conversation}

-----------------------------
CURRENT QUESTION
-----------------------------
{question}

-----------------------------
ANSWER
-----------------------------
"""


    # -----------------------------
    # Groq Response
    # -----------------------------
    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response.choices[0].message.content
