import re
from fastapi import HTTPException


def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters long")
    if not re.search(r'[a-z]', password):
        raise HTTPException(
            status_code=400, detail="Password must include a lowercase letter")
    if not re.search(r'[A-Z]', password):
        raise HTTPException(
            status_code=400, detail="Password must include an uppercase letter")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise HTTPException(
            status_code=400, detail="Password must include a special character")
