# app/utils.py

import io
import logging
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

# Intentar importar librerías de OCR (pytesseract y pdf2image)
try:
    from pdf2image import convert_from_bytes
    import pytesseract
    OCR_ENABLED = True
except ImportError:
    OCR_ENABLED = False
    logger.warning("⚠️ OCR no disponible: pytesseract o pdf2image no instalados.")

def procesar_pdf(contenido_archivo: bytes) -> list:
    """
    Extrae texto de PDF. Intenta método estándar, si falla usa OCR.
    """
    try:
        pdf_stream = io.BytesIO(contenido_archivo)
        lector = PdfReader(pdf_stream)
        
        textos = []
        for pagina in lector.pages:
            texto = pagina.extract_text()
            if texto and len(texto.strip()) > 20:
                textos.append(texto.strip())

        # Si se extrajo texto válido, retornarlo
        if textos:
            texto_completo = "\n".join(textos)
            splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
            return splitter.split_text(texto_completo)

        # Si no hay texto y OCR está habilitado, intentar OCR
        if not textos and OCR_ENABLED:
            logger.info("🔍 No se encontró texto. Iniciando OCR...")
            return procesar_con_ocr(contenido_archivo)

        return []

    except Exception as e:
        logger.error(f"Error PDF: {e}")
        return []

def procesar_con_ocr(contenido_bytes: bytes) -> list:
    """Extrae texto usando OCR para PDFs escaneados/imágenes."""
    try:
        imagenes = convert_from_bytes(contenido_bytes)
        textos = []
        for img in imagenes:
            texto = pytesseract.image_to_string(img, lang='spa')
            if texto.strip():
                textos.append(texto.strip())
        
        if not textos:
            return []

        texto_completo = "\n".join(textos)
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        return splitter.split_text(texto_completo)
    except Exception as e:
        logger.error(f"Error OCR: {e}")
        return []