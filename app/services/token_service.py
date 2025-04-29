import jwt
import datetime
from flask import current_app


def generate_token(user_id):
    """Generate a JWT token for authentication."""
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
        "sub": str(user_id),  # Convert user_id to string
    }

    return jwt.encode(
        payload, current_app.config.get("SECRET_KEY", "dev"), algorithm="HS256"
    )


def decode_token(token):
    """Decode a JWT token."""
    try:
        payload = jwt.decode(
            token, current_app.config.get("SECRET_KEY", "dev"), algorithms=["HS256"]
        )
        return {"success": True, "user_id": payload["sub"]}
    except jwt.ExpiredSignatureError:
        return {"success": False, "message": "Token expired. Please log in again."}
    except jwt.InvalidTokenError:
        return {"success": False, "message": "Invalid token. Please log in again."}
