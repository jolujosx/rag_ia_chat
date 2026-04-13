import io
import logging
from pdf2image import convert_from_bytes
import pytesseract
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

def procesar_pdf_con_ocr(contenido_archivo: bytes) -> list:
    """
    Extrae texto de PDFs escaneados usando OCR (Tesseract).
    Más lento pero funciona con imágenes.
    """
    try:
        logger.info("🔍 Procesando PDF con OCR...")
        
        # Convertir PDF a imágenes
        imagenes = convert_from_bytes(contenido_archivo)
        
        textos = []
        for i, imagen in enumerate(imagenes):
            texto = pytesseract.image_to_string(imagen, lang='spa')
            if texto.strip():
                textos.append(texto.strip())
            logger.info(f"✓ Página {i+1} OCR: {len(texto)} caracteres")
        
        if not textos:
            logger.error("OCR no pudo extraer texto")
            return []
        
        texto_completo = "\n\n".join(textos)
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150
        )
        
        return splitter.split_text(texto_completo)
        
    except Exception as e:
        logger.error(f"❌ Error en OCR: {e}")
        return []