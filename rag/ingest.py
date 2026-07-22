from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

loader = DirectoryLoader(
    "data/policies",
    glob="*.md",
    loader_cls=TextLoader
)

documents = loader.load()

headers = [
    ("#", "title"),
    ("##", "section"),
]

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers
)

chunks = []

for doc in documents:
    chunks.extend(splitter.split_text(doc.page_content))

embedding = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory="rag/chroma_db"
)

print(f"Stored {len(chunks)} chunks.")