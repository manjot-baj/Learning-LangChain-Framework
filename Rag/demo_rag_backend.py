import os
from fastapi import FastAPI, UploadFile, File, Form
import tempfile
import uvicorn
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from decouple import config
import pandas as pd
from docx2txt import process as docx_process
from PIL import Image
import traceback

# ================= CONFIG =================
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = config("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "DEMO_RAG_APP"

os.environ["MISTRAL_API_KEY"] = config("MISTRALAI_KEY")

# ================= Constants =============
EMBEDDINGS = MistralAIEmbeddings()
LLM = ChatMistralAI(model="mistral-large-latest")

TEXT_SPLITTER = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# PROMPT = ChatPromptTemplate.from_template(
#     """
# You are a strict data extraction assistant.

# RULES:
# - Answer ONLY using the provided context.
# - If the answer is not clearly present, reply exactly:
#   "Answer not found in document."
# - Do NOT guess.
# - Do NOT infer missing columns.
# - Give short factual answer.

# <context>
# {context}
# </context>

# Question: {input}
# """
# )

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a Senior Data Analyst AI working exclusively on the
Depot Management System (DMS) developed by
Sun and Pearls IT Solutions Pvt Ltd.

You must follow ALL rules below strictly.

──────────────── DOMAIN SCOPE ────────────────
Allowed domains ONLY:
- Depot Operations
- Stock lifecycle
- MNR workflow
- Allotment
- Gate IN / Gate OUT
- Billing
- Invoicing

If a question is outside these → return fallback.

──────────────── DATA RULES ────────────────
- Use ONLY uploaded file data + provided context.
- NEVER guess, infer, estimate, or fabricate numbers.
- NEVER use external knowledge.
- If required data is missing → return fallback.

MANDATORY FALLBACK RESPONSE (exact text):
INSUFFICIENT DATA TO ANALYZE

No extra words. No markdown. Nothing else.

──────────────── OUTPUT FORMAT ────────────────
When sufficient data exists, response MUST:

1. Be valid Markdown
2. Contain EXACTLY these sections in order:

## Business Insights
• Bullet-point, data-driven findings
• Refer to DMS workflow stages where relevant

## Summary Conclusions
• Concise operational conclusions
• State impact on depot efficiency, MNR, stock, or billing

──────────────── BEHAVIOR RULES ────────────────
- No conversational tone
- No explanations about the AI
- No filler text
- No assumptions
- No emojis
- No tables unless explicitly supported by data

Act as a strict enterprise analytics engine.
Only facts. Only data. Only DMS.
""",
        ),
        (
            "human",
            """
<context>
{context}
</context>

Question: {input}
""",
        ),
    ]
)

# ================= LOADERS =================


def excel_loader(file_path: str) -> list[Document]:
    try:
        sheets = pd.read_excel(file_path, sheet_name=None)

        docs = []
        for sheet_name, df in sheets.items():
            df = df.fillna("")
            table_text = df.to_markdown(index=False)

            docs.append(
                Document(
                    page_content=f"Sheet: {sheet_name}\n{table_text}",
                    metadata={"source": file_path, "sheet": sheet_name},
                )
            )

        return docs

    except Exception:
        return [
            Document(
                page_content="Unable to extract Excel content",
                metadata={"source": file_path},
            )
        ]


def image_loader(file_path: str) -> list[Document]:
    try:
        with Image.open(file_path) as img:
            content = f"Image: {img.size} pixels, mode: {img.mode}"
        return [Document(page_content=content, metadata={"source": file_path})]
    except Exception:
        return [Document(page_content="Image file", metadata={"source": file_path})]


def load_file(file_path: str):
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        return PyPDFLoader(file_path).load()
    elif ext in [".doc", ".docx"]:
        return Docx2txtLoader(file_path).load()
    elif ext in [".xls", ".xlsx"]:
        return excel_loader(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        return image_loader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


# ================= BUILD RAG =================
def build_chain(docs):
    split_docs = TEXT_SPLITTER.split_documents(docs)
    db = FAISS.from_documents(split_docs, EMBEDDINGS)
    retriever = db.as_retriever(search_kwargs={"k": 20})
    doc_chain = create_stuff_documents_chain(LLM, PROMPT)
    return create_retrieval_chain(retriever, doc_chain)


# ================= FASTAPI APP =================
app = FastAPI(title="RAG Backend", version="1.0")


@app.get("/")
def root():
    return {"message": "RAG backend running..."}


@app.post("/ask")
async def ask(file: UploadFile = File(...), question: str = Form(...)):
    suffix = Path(file.filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name

    try:
        docs = load_file(temp_path)
        chain = build_chain(docs)
        response = chain.invoke({"input": question})
        return {
            "answer": response["answer"],
            "sources": [doc.metadata for doc in response["context"]],
        }
    except:
        pass
    finally:
        os.unlink(temp_path)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
