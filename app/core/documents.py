from langchain.document_loaders import (
    TextLoader,
    PDFPlumberLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader_funcions = [
    lambda: TextLoader("data/about_me.txt").load(),
    lambda: PDFPlumberLoader("data/resume.pdf").load(),
    lambda: TextLoader("data/projects.txt").load()
]

docs = []
for fn in loader_funcions:
    try:
        docs.extend(fn())
    except Exception as e:
        print(f"Error loading document: {e}")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50)

def split_documents(docs):
    """
    Split documents into smaller chunks for processing.
    """
    return text_splitter.split_documents(docs)

