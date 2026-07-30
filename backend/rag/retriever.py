from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

embedding = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory="rag/chroma_db",
    embedding_function=embedding
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k":3}
)