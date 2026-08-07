import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from utils.paths import BACKEND_DIR

embedding = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory=str(BACKEND_DIR / "rag" / "chroma_db"),
    embedding_function=embedding
)

print("Number of documents:", vectorstore._collection.count())

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)