from git import Repo 
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.blob_loaders import FileSystemBlobLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
import os



def repo_ingestion(repo_url):
    os.makedirs('repo', exist_ok=True)
    repo_path = "repo/"
    repo = Repo.clone_from('https://github.com/charan-x16/end-to-end-medical-chatbot-GEN-AI', to_path=repo_path)



def load_repo(repo_path):
    blob_loader = FileSystemBlobLoader(repo_path, suffixes=[".py"])

    loader = GenericLoader(
        blob_loader=blob_loader, 
        blob_parser=LanguageParser(language=Language.PYTHON, parser_threshold=500)  
    )

    documents = loader.load()
    return documents


def text_splitter(documents):
    document_loader = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON,
                                                               chunk_size=500,
                                                               chunk_overlap = 20)
    text = document_loader.split_documents(documents)
    return text



def load_embedding():
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embeddings