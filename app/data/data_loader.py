from langchain_community.document_loaders import TextLoader, PDFPlumberLoader, WebBaseLoader, GitHubRepoLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.core.config import settings
from app.core.vectorstore import create_vector_store

def load_local_docs():
    files = ["data/about_me.txt", "data/projects.txt", "data/programs.md", "data/resume.pdf"]
    docs = []
    for f in files:
        try:
            if f.endswith('.pdf'):
                docs.extend(PDFPlumberLoader(f).load())
            else:
                docs.extend(TextLoader(f).load())
        except Exception:
            continue
    return docs

def load_web_profiles():
    urls = [settings.GITHUB_PROFILE, settings.LINKEDIN_PROFILE,
            settings.MEDIUM_PROFILE, settings.KAGGLE_PROFILE,
            settings.TWITTER_PROFILE]
    docs = []
    for url in urls:
        if not url:
            continue
        try:
            if 'github.com' in url:
                docs.extend(GitHubRepoLoader(repo_url=url).load())
            else:
                docs.extend(WebBaseLoader(url).load())
        except Exception:
            continue
    return docs

def get_all_chunks():
    docs = load_local_docs() + load_web_profiles()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)

create_vector_store.add_documents(get_all_chunks)



