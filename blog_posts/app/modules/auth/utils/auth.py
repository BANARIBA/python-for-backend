import os
from datetime import datetime, timedelta, timezone

from typing import Optional

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Configuración
ph = PasswordHasher()
SECRET_KEY = os.getenv('SECRET_KEY', 'incluide-secret-key-in.env')
ALGORITHM = "HS256"

class AuthHelpers:
    @staticmethod
    def hash_password(password: str) -> str:
        return ph.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        try:
            return ph.verify(hashed_password, plain_password)
        except (VerifyMismatchError, Exception):
            return False

    @staticmethod
    def create_token(data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.PyJWTError:
            return None