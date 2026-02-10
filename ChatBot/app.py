from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os
from decouple import config

# LangSmith Tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = config("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = config("LANGCHAIN_PROJECT", default="default")

# MistralAI
MISTRALAI_KEY = config("MISTRALAI_KEY")


# Prompt Template

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant, Please response to user queries"),
        ("user", "Question:{question}"),
    ]
)

# streamlit framwork

st.title("Langchain Demo With MistralAI API")
input_text = st.text_input("Search the topic u want")

# MistralAI LLM

llm = ChatMistralAI(model="mistral-large-latest", api_key=MISTRALAI_KEY)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    st.write(chain.invoke({"question": input_text}))
