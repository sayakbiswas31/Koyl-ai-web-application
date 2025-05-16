import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from transformers import pipeline
import torch
import os

FAISS_INDEX_DIR = "data/faiss_index"

def preprocess_and_embed(documents):
    if not documents:
        return [], np.array([])
    
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
    # Create LangChain Document objects
    texts = [f"Title: {doc['title']}\nAbstract: {doc['abstract']}" for doc in documents if doc.get('title') and doc.get('abstract')]
    langchain_documents = [Document(page_content=text) for text in texts]
    
    # Split documents into chunks
    chunks = text_splitter.split_documents(langchain_documents)
    chunk_texts = [chunk.page_content for chunk in chunks]
    
    # Generate embeddings
    embeddings = embedding_model.encode(chunk_texts, show_progress_bar=True)
    return chunk_texts, embeddings

def store_in_faiss(texts, embeddings):
    if not texts or embeddings.size == 0:
        return None
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype(np.float32))
    
    embeddings_wrapper = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    vector_store = FAISS.from_texts(texts, embeddings_wrapper)
    
    # Save Faiss index
    os.makedirs(FAISS_INDEX_DIR, exist_ok=True)
    vector_store.save_local(FAISS_INDEX_DIR)
    
    return vector_store

def load_faiss_vector_store():
    if not os.path.exists(FAISS_INDEX_DIR):
        return None
    embeddings_wrapper = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    return FAISS.load_local(FAISS_INDEX_DIR, embeddings_wrapper)

def setup_rag_pipeline(vector_store):
    if vector_store is None:
        return None
    generator = pipeline("text2text-generation", model="t5-small", device=0 if torch.cuda.is_available() else -1)
    llm = HuggingFacePipeline(pipeline=generator)
    rag_pipeline = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    return rag_pipeline

def query_rag(rag_pipeline, question):
    if rag_pipeline is None:
        return "No data available to answer the query.", []
    result = rag_pipeline({"query": question})
    return result["result"], result["source_documents"]
