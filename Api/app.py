from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langserve import add_routes
import uvicorn
import os
from decouple import config

# LangSmith Tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = config("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "Tutorial 2"

# MistralAI
MISTRALAI_KEY = config("MISTRALAI_KEY")

app = FastAPI(
    title="LangChain Server", version="1.0", description="A simple API Server"
)

llm = ChatMistralAI(model="mistral-large-latest", api_key=MISTRALAI_KEY)

prompt1 = ChatPromptTemplate.from_template(
    "Write me an essay about {topic} with 100 words"
)
prompt2 = ChatPromptTemplate.from_template(
    "Write me an poem about {topic} with 100 words"
)

add_routes(app, prompt1 | llm, path="/essay")
add_routes(app, prompt2 | llm, path="/poem")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
