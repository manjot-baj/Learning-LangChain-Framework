from langchain_community.utilities import SQLDatabase
from langchain_classic.chains import create_sql_query_chain
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_mistralai import ChatMistralAI


def build_chain(db_path: str):
    """Create NL → SQL → Answer chain."""

    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

    llm = ChatMistralAI(model="mistral-large-latest", temperature=0)

    sql_chain = create_sql_query_chain(llm, db)

    answer_prompt = PromptTemplate.from_template(
        """
        Given the user question, SQL query, and SQL result, return a natural language answer.

        Question: {question}
        SQL Query: {query}
        SQL Result: {result}
        Answer:
        """
    )

    def run_sql(query: str):
        return db.run(query)

    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            result=lambda x: run_sql(x["query"])
        )
        | answer_prompt
        | llm
        | StrOutputParser()
    )

    return chain
