# app/auth.py

import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "00842c8d75a448eae7e0")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def autenticar_usuario(username: str, password: str):
    """Verifica credenciales simples."""
    if username == "admin" and password == "1234":
        return {"username": "admin"}
    return None


def crear_token(data):
    """Genera un token JWT con fecha de expiración."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(token: str):
    """Decodifica y valida el token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return username
    except JWTError:
        return None