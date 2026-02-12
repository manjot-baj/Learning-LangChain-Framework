import requests
import streamlit as st


def get_llm_essay_response(input_text):
    response = requests.post(
        "http://localhost:8000/essay/invoke", json={"input": {"topic": input_text}}
    )
    return response.json()["output"]["content"]


def get_llm_poem_response(input_text):
    response = requests.post(
        "http://localhost:8000/poem/invoke", json={"input": {"topic": input_text}}
    )
    return response.json()["output"]["content"]


st.title("LangChain: LangServe Demo with MistralAI Custom APIs")
input_text_1 = st.text_input("Write an Essay on: ")
input_text_2 = st.text_input("Write a Poem on: ")

if input_text_1:
    st.write(get_llm_essay_response(input_text_1))

if input_text_2:
    st.write(get_llm_poem_response(input_text_2))
