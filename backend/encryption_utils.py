import os
from cryptography.fernet import Fernet


FERNET_KEY = os.environ.get("FERNET_KEY")


def get_fernet():
    if not FERNET_KEY:
        return None
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
