from fastapi import FastAPI, UploadFile, File
from langserve import add_routes
from nl2sql_chain import build_chain
from db_utils import excel_to_sqlite
import shutil
import os
from decouple import config

app = FastAPI(title="NL2SQL API")

# ================= CONFIG =================
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = config("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "DEMO_RAG_APP"

os.environ["MISTRAL_API_KEY"] = config("MISTRALAI_KEY")

# ================= Constants =============

DB_PATH = "data.db"
CHAIN = None


@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    global CHAIN

    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_path = excel_to_sqlite(temp_path, DB_PATH)

    # Build a real runnable chain after DB creation
    CHAIN = build_chain(db_path)

    os.remove(temp_path)

    return {"status": "Database created", "db": db_path}


@app.get("/health")
def health():
    return {"status": "ok"}


# LangServe route
# IMPORTANT: LangServe expects a Runnable instance, not a function
# We register the route after the chain is created.

from langchain_core.runnables import RunnableLambda

# Dynamic runnable wrapper so LangServe always calls the latest CHAIN
from langchain_core.runnables import RunnableLambda


def dynamic_chain(input_dict):
    """Proxy that forwards calls to the latest built chain."""
    global CHAIN

    # If Excel not uploaded yet
    if CHAIN is None:
        return {"output": "Upload an Excel file first."}

    return CHAIN.invoke(input_dict)


CHAIN = None

add_routes(app, RunnableLambda(dynamic_chain), path="/nl2sql")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
