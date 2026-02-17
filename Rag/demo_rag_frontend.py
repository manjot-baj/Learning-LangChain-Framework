import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="Multi‑File RAG", layout="wide")

st.title("Multi‑File RAG Chatbot")

uploaded_file = st.file_uploader(
    "Upload a file (PDF, Word, Excel, Image)",
    type=["pdf", "docx", "doc", "xlsx", "xls", "png", "jpg", "jpeg"],
)

question = st.text_input("Ask a question from the document:")

if st.button("Get Answer"):

    if not uploaded_file or not question:
        st.warning("Please upload a file and enter a question.")

    else:
        with st.spinner("Thinking..."):

            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {"question": question}

            response = requests.post(BACKEND_URL, files=files, data=data)

            if response.status_code == 200:
                st.markdown("### Answer")
                st.write(response.json()["answer"])
            else:
                st.error("Error from backend")
