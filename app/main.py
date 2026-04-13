# app/main.py

import os
import logging
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# 🔹 1. Cargar variables de entorno
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# 🔹 2. Importaciones
from app.utils import procesar_pdf
from app.engine import crear_motor_rag
from app.db import guardar_motor, obtener_motor
from app.auth import autenticar_usuario, crear_token
from app.deps import obtener_usuario

app = FastAPI(title="Analista Legal IA")

# 🔹 3. Archivos estáticos
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ==========================================
#  RUTAS
# ==========================================

@app.get("/", include_in_schema=False)
async def serve_frontend():
    return FileResponse(STATIC_DIR / "index.html")

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = autenticar_usuario(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = crear_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/entrenar")
async def entrenar(
    user: str = Depends(obtener_usuario),
    archivo: UploadFile = File(...)
):
    try:
        logger.info(f"📥 Recibiendo PDF para: {user}")
        contenido = await archivo.read()
        
        # 👉 Aquí es donde ocurre la magia del OCR si es necesario
        trozos = procesar_pdf(contenido)
        
        if not trozos:
            raise HTTPException(status_code=400, detail="No se pudo extraer texto. Intenta subir un PDF nativo o instala Tesseract para OCR.")

        guardar_motor(user, trozos)
        logger.info(f"✅ Guardados {len(trozos)} fragmentos")
        
        return {"status": "Listo", "fragmentos": len(trozos)}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.post("/preguntar")
async def preguntar(
    user: str = Depends(obtener_usuario),
    pregunta: str = Form(...)
):
    trozos = obtener_motor(user)
    if not trozos:
        raise HTTPException(status_code=400, detail="Sube un documento primero")

    try:
        motor = crear_motor_rag(trozos, user)
        res = motor.invoke({"query": pregunta})
        return {"respuesta": res.get("result", "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al consultar a la IA")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)