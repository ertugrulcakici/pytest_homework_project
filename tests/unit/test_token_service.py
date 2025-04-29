import pytest
import time
import jwt
from app.services.token_service import generate_token, decode_token

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit


class TestTokenService:
    """Unit tests for token service."""

    def test_generate_token(self, app):
        """Test token generation."""
        with app.app_context():
            # Generate a token for a user ID
            user_id = 123
            token = generate_token(user_id)

            # Verify token is a string
            assert isinstance(token, str)

            # Decode the token manually to verify payload
            secret_key = app.config.get("SECRET_KEY", "dev")
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])

            # Verify payload contains correct user ID (as string)
            assert payload["sub"] == str(user_id)

            # Verify token has expiration time in the future
            assert "exp" in payload
            assert payload["exp"] > time.time()

            # Verify token has issued at time
            assert "iat" in payload
            assert payload["iat"] <= time.time()

    def test_decode_token(self, app):
        """Test token decoding."""
        with app.app_context():
            # Generate a token
            user_id = 456
            token = generate_token(user_id)

            # Decode the token
            result = decode_token(token)

            # Verify successful decoding
            assert result["success"] is True
            assert result["user_id"] == str(user_id)

    def test_decode_invalid_token(self, app):
        """Test decoding an invalid token."""
        with app.app_context():
            # Try to decode an invalid token
            result = decode_token("invalid.token.string")

            # Verify failure
            assert result["success"] is False
            assert "Invalid token" in result["message"]

    def test_token_expiration(self, app):
        """Test token expiration."""
        with app.app_context():
            # Generate a token
            user_id = 789
            token = generate_token(user_id)

            # Decode the token to get its payload
            secret_key = app.config.get("SECRET_KEY", "dev")
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])

            # Modify the payload to set the expiration time in the past
            payload["exp"] = int(time.time()) - 10

            # Re-encode the token with the expired time
            expired_token = jwt.encode(payload, secret_key, algorithm="HS256")

            # Try to decode the expired token
            result = decode_token(expired_token)

            # Verify failure due to expiration
            assert result["success"] is False
            assert "expired" in result["message"].lower()
