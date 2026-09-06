import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="NL2SQL Demo", page_icon="🗄️", layout="wide")

st.title("🗄️ Natural Language → SQL Explorer")

# ---------------- Upload Excel ----------------
st.header("1️⃣ Upload Excel File")

uploaded_file = st.file_uploader("Upload .xlsx file", type=["xlsx"])

if uploaded_file is not None:
    if st.button("Create Database"):
        with st.spinner("Uploading & creating database..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            res = requests.post(f"{API_URL}/upload", files=files)

        if res.status_code == 200:
            st.success("Database created successfully!")
            st.json(res.json())
        else:
            st.error("Upload failed")
            st.text(res.text)

# ---------------- Ask Question ----------------
st.header("2️⃣ Ask a Question")

question = st.text_input(
    "Enter your question in natural language",
    placeholder="e.g. What is total sales by region?",
)

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                res = requests.post(
                    f"{API_URL}/nl2sql/invoke",
                    json={"input": {"question": question}},
                )

                if res.status_code == 200:
                    data = res.json()
                    st.subheader("📊 Answer")
                    st.write(data.get("output", data))
                else:
                    st.error("Query failed")
                    st.text(res.text)

            except Exception as e:
                st.error(f"Error connecting to API: {e}")

# ---------------- Health Check ----------------
st.sidebar.header("🔧 Server Status")

if st.sidebar.button("Check Health"):
    try:
        res = requests.get(f"{API_URL}/health")
        st.sidebar.success(res.json()["status"])
    except:
        st.sidebar.error("API not reachable")
