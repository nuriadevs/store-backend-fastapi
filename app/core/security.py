import logging
import re
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext
import base64
from datetime import datetime, timezone, timedelta
from app.core import settings
from app.core.settings import get_settings



SPECIAL_CHARACTERS = ['@', '#', '$', '%', '=', ':', '?', '.', '-', '!','_']

dni = "TRWAGMYFPDXBNJZSQVHLCKE"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


settings = get_settings()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        if "sub" not in payload:
            raise HTTPException(status_code=401, detail="Token invalido: Missing user identifier")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def is_password_strong_enough(password: str) -> bool:
    if len(password) < 8:
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not any(char in SPECIAL_CHARACTERS for char in password):
        return False

    return True

def dni_valid(dni:str)->bool:

    if not re.fullmatch(r'\d{8}[A-Z]', dni):
        return False
    return True


def str_encode(string: str) -> str:
    return base64.b85encode(string.encode('ascii')).decode('ascii')


def str_decode(string: str) -> str:
    return base64.b85decode(string.encode('ascii')).decode('ascii')


async def load_user(email: str, db):
    from app.models.user.user import User
    try:
        user = db.query(User).filter(User.email == email).first()
    except Exception:
        logging.info(f"User Not Found, Email: {email}")
        user = None
    return user


def generate_token(payload: dict, expiry: timedelta):
    expire = datetime.now(timezone.utc) + expiry
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
