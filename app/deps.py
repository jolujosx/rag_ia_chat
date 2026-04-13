# app/deps.py

from fastapi import Header, HTTPException, status
from app.auth import verificar_token

async def obtener_usuario(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token requerido en el header Authorization",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Extraer token de forma segura (case-insensitive)
    token = authorization.replace("Bearer ", "").replace("bearer ", "").strip()
    
    if not token:
        raise HTTPException(status_code=401, detail="Formato de token inválido")

    user = verificar_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    return user