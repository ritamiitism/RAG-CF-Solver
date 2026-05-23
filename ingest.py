from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ---------------- LOAD PDF ---------------- #
loader = PyPDFLoader("data/cp_handbook.pdf")

documents = loader.load()

print(f"Loaded {len(documents)} pages")


# ---------------- SPLIT INTO CHUNKS ---------------- #
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")


# ---------------- EMBEDDINGS ---------------- #
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ---------------- CREATE VECTOR DB ---------------- #
vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)


# ---------------- SAVE VECTOR DB ---------------- #
vectorstore.save_local("vectorstore")

print("FAISS vector database saved successfully!")