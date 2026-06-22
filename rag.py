from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_qa_chain(vectorstore):

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.2
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    return llm, retriever