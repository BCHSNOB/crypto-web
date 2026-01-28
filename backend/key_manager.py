import hashlib

def derive_key(password: str, size=32):
    return hashlib.sha256(password.encode()).digest()[:size]
