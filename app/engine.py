# app/engine.py
import os
from dotenv import load_dotenv

# Importaciones diferidas para no saturar RAM al inicio
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
# Usamos embeddings más ligeros o carga bajo demanda
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

load_dotenv()

# Variable global para el modelo (None al inicio para ahorrar RAM)
_embeddings_model = None

def get_embeddings():
    global _embeddings_model
    if _embeddings_model is None:
        # Solo carga el modelo cuando se llama a esta función
        _embeddings_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embeddings_model

def crear_motor_rag(trozos_texto, user_id):
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("Falta GROQ_API_KEY")

    # 1. Carga embeddings solo ahora
    embeddings = get_embeddings()

    # 2. Crea vectorstore
    # Usamos persist_directory para evitar recrear todo en memoria RAM si es posible
    persist_dir = f"./chroma_db_{user_id}"
    vectorstore = Chroma.from_texts(
        texts=trozos_texto,
        embedding=embeddings,
        persist_directory=persist_dir # Guarda en disco para liberar RAM
    )

    # 3. Configura LLM
    llm = ChatGroq(
        temperature=0,
        model_name="llama-3.1-8b-instant", # Modelo rápido y ligero
        groq_api_key=groq_api_key
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )