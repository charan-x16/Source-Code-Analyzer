from src.helper import repo_ingestion, load_repo, load_embedding, text_splitter
from langchain.vectorstores import Chroma
import os 



documents = load_repo("repo/")
text_chunks = text_splitter(documents)
embedding = load_embedding()


vectordb = Chroma.from_documents(text_chunks, embedding=embedding, persist_directory='./db')
vectordb.persist()