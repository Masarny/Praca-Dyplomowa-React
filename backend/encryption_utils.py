import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from functools import lru_cache


load_dotenv()


@lru_cache(maxsize=1)
def get_fernet():
    FERNET_KEY = os.environ.get("FERNET_KEY")
    if not FERNET_KEY:
        raise RuntimeError("Brak ustawionego klucza FERNET_KEY w zmiennych środowiskowych!")
    return Fernet(FERNET_KEY.encode())


def encrypt_text(plaintext: str) -> str:
    f = get_fernet()
    if not f:
        return plaintext
    return f.encrypt(plaintext.encode()).decode()


def decrypt_text(token: str) -> str:
    f = get_fernet()
    if not f:
        return token
    return f.decrypt(token.encode()).decode()
