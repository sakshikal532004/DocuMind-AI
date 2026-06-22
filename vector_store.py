from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import tempfile
import os

DB_DIR = "vector_db"

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_vector_store(uploaded_files):

    docs = []

    for pdf in uploaded_files:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:

            tmp.write(pdf.read())

            path = tmp.name

        loader = PyPDFLoader(path)

        docs.extend(loader.load())

        os.remove(path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    splits = splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=DB_DIR
    )

    return vectorstore


def load_vector_store():

    return Chroma(
        persist_directory=DB_DIR,
        embedding_function=embedding
    )