from pathlib import Path
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
load_dotenv()
pdf_Path= Path(__file__).parent/"SystemDesign.pdf"
loader= PyPDFLoader(file_path=pdf_Path)
docs = loader.load()
text_splitter= RecursiveCharacterTextSplitter(
    chunk_size=100000,
    chunk_overlap=20000
)
chunks = text_splitter.split_documents(documents=docs)
#Vector embedding from chunks
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)
print("Indexing of pdf done")