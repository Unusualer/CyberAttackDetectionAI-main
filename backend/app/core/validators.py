from typing import Any
from pydantic import BaseModel, validator, EmailStr
import re

class PasswordValidator:
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

class EmailValidator:
    @classmethod
    def validate_email(cls, v: str) -> str:
        email = EmailStr.validate(v)
        domain = email.split("@")[1]
        if domain in ["tempmail.com", "throwaway.com"]:  # Add disposable email domains
            raise ValueError("Disposable email addresses are not allowed")
        return email

class ApiKeyValidator:
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        if not v or len(v) < 32:
            raise ValueError("Invalid API key format")
        return v 