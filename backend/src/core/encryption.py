"""Simple encryption utility for storing sensitive data."""
from cryptography.fernet import Fernet
import base64
import os


class Encryptor:
    """Simple encryption/decryption for sensitive data."""

    def __init__(self):
        """Initialize encryptor with key from environment or generate new."""
        # In production, this should be stored securely
        key = os.environ.get('ENCRYPTION_KEY')
        if not key:
            # Generate a key (in production, save this securely)
            key = Fernet.generate_key().decode()

        if isinstance(key, str):
            key = key.encode()

        self.cipher = Fernet(key)

    def encrypt(self, text: str) -> str:
        """Encrypt text."""
        if not text:
            return ""
        return self.cipher.encrypt(text.encode()).decode()

    def decrypt(self, encrypted_text: str) -> str:
        """Decrypt text."""
        if not encrypted_text:
            return ""
        try:
            return self.cipher.decrypt(encrypted_text.encode()).decode()
        except Exception:
            return encrypted_text  # Return as-is if decryption fails


# Global encryptor instance
encryptor = Encryptor()
