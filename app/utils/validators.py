from typing import Optional
import re

def validate_username(username: str) -> None:
    if not username or len(username) < 3:
        raise ValueError("Username must be at least 3 characters long")
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValueError("Username can only contain letters, numbers and underscore")

    
def validate_password(password: str) -> None:
    errors = []
    
    if not password or len(password) < 8:
        errors.append("La contraseña debe tener al menos 8 caracteres")
    
    if not re.search(r'[A-Z]', password):
        errors.append("La contraseña debe contener al menos una mayúscula")
    
    if not re.search(r'[0-9]', password):
        errors.append("La contraseña debe contener al menos un número")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("La contraseña debe contener al menos un carácter especial")
    
    if errors:
        raise ValueError("\n".join(errors))