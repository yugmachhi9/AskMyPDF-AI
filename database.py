#load pdf
#split into chunks
#crete embeddings 
#store into chroma (vector database)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv 

load_dotenv()

loader = PyPDFLoader("document loader/deeplearning.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)
chunks = splitter.split_documents(docs)

embedding_model = HuggingFaceEmbeddings()

Vectorstore = Chroma.from_documents(
    documents=chunks, 
    embedding=embedding_model,
    persist_directory="chroma_db"
)