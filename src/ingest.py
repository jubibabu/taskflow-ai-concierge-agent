import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

def build_vectorstore():
    docs = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            loader = TextLoader(os.path.join(DATA_DIR, filename))
            docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )
    print("Ingested " + str(len(chunks)) + " chunks into ChromaDB at " + PERSIST_DIR)
    return vectorstore

if __name__ == "__main__":
    build_vectorstore()
