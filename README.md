# 🇪🇨 Ecuador Legal RAG AI

![FastAPI](https://shields.io)
![Python](https://shields.io)
![LangChain](https://shields.io)
![Groq](https://shields.io)

## 🚀 Descripción del Proyecto
Este es un sistema de **Arquitectura RAG (Retrieval-Augmented Generation)** diseñado para ingenieros que buscan optimizar el análisis de documentos legales y corporativos en Ecuador. Permite cargar archivos PDF complejos y realizar consultas en lenguaje natural utilizando el modelo **Llama 3** a través de **Groq**.

## 🛠️ Tecnologías Utilizadas
- **Backend:** FastAPI (Python)
- **Motor de IA:** LangChain + Groq (Llama 3)
- **Base de Datos Vectorial:** ChromaDB
- **Embeddings:** HuggingFace (all-MiniLM-L6-v2)
- **Infraestructura:** GitHub Codespaces (DevContainers)

## 🏗️ Arquitectura RAG
1. **Ingesta:** El sistema recibe un PDF y lo fragmenta usando `RecursiveCharacterTextSplitter`.
2. **Vectorización:** Convierte el texto en vectores numéricos (Embeddings).
3. **Recuperación:** Busca los fragmentos más relevantes basados en la pregunta del usuario.
4. **Generación:** Envía el contexto recuperado a Llama 3 para generar una respuesta precisa y contextualizada.

## 📦 Instalación y Uso
1. Clona este repositorio.
2. Configura tu `.env` con `GROQ_API_KEY`.
3. Ejecuta el servidor:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
