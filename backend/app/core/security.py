import hashlib
import os
import secrets

def get_password_hash(password: str) -> str:
    """Hash a password using PBKDF2-HMAC-SHA256 with a secure random salt."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}:{key}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against the stored salt:hash string."""
    try:
        salt, stored_key = hashed_password.split(':')
        key = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return secrets.compare_digest(key, stored_key)
    except Exception:
        return False
