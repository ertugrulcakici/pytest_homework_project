import pytest
from app.services.user_service import (
    validate_name,
    validate_email,
    validate_password,
    validate_date_of_birth,
    register_user,
    authenticate_user,
    get_user_by_id,
    hash_password,
    verify_password,
)

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit


class TestUserValidation:
    """Unit tests for user input validation."""

    def test_name_validation(self):
        """Test validation of first and last names."""
        # Valid names (2 or more characters)
        valid_names = ["Jo", "John", "John-Paul", "O'Brien", "María José"]
        for name in valid_names:
            is_valid, _ = validate_name(name)
            assert is_valid is True

        # Invalid names (less than 2 characters)
        invalid_names = ["", "J", None]
        for name in invalid_names:
            is_valid, message = validate_name(name)
            assert is_valid is False
            assert "at least 2 characters" in message

    def test_email_validation(self):
        """Test validation of email addresses."""
        # Valid email formats
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user123@example.co.uk",
            "user-name@example.org",
        ]
        for email in valid_emails:
            is_valid, _ = validate_email(email)
            assert is_valid is True

        # Invalid email formats
        invalid_emails = [
            "",
            "user",
            "user@",
            "@example.com",
            "user@example",
            "user@.com",
            "user@exam ple.com",
        ]
        for email in invalid_emails:
            is_valid, message = validate_email(email)
            assert is_valid is False
            assert "Invalid email format" in message

    def test_password_validation(self):
        """Test validation of password complexity."""
        # Valid passwords
        valid_passwords = ["Password1!", "SecurePass123@", "Abcde123!", "ComplexPwd1#"]
        for password in valid_passwords:
            is_valid, _ = validate_password(password)
            assert is_valid is True

        # Password too short
        is_valid, message = validate_password("Abc1!")
        assert is_valid is False
        assert "at least 8 characters" in message

        # Missing lowercase
        is_valid, message = validate_password("PASSWORD123!")
        assert is_valid is False
        assert "lowercase letter" in message

        # Missing uppercase
        is_valid, message = validate_password("password123!")
        assert is_valid is False
        assert "uppercase letter" in message

        # Missing number
        is_valid, message = validate_password("PasswordTest!")
        assert is_valid is False
        assert "number" in message

        # Missing symbol
        is_valid, message = validate_password("Password123")
        assert is_valid is False
        assert "symbol" in message

    def test_date_validation(self):
        """Test validation of date of birth format."""
        # Valid dates
        valid_dates = ["01/01/1990", "31/12/2000", "29/02/2020"]  # Leap year
        for date in valid_dates:
            is_valid, _ = validate_date_of_birth(date)
            assert is_valid is True

        # Invalid date formats
        invalid_formats = ["", "1/1/1990", "01-01-1990", "01/01/90", "1990/01/01"]
        for date in invalid_formats:
            is_valid, message = validate_date_of_birth(date)
            assert is_valid is False
            assert "format" in message.lower()

        # Invalid dates
        invalid_dates = [
            "31/04/2020",  # April has 30 days
            "29/02/2019",  # Not a leap year
            "00/01/2020",  # Day can't be 0
            "32/01/2020",  # Day can't be 32
            "01/13/2020",  # Month can't be 13
        ]
        for date in invalid_dates:
            is_valid, message = validate_date_of_birth(date)
            assert is_valid is False
            assert "Invalid date" in message


class TestUserService:
    """Unit tests for user service functions."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "testpassword123"

        # Hash with auto-generated salt
        hashed1 = hash_password(password)

        # Verify hash format (should contain salt and hash separated by $)
        assert "$" in hashed1

        # Hash with specific salt
        salt = "abcdef1234567890"
        hashed2 = hash_password(password, salt)

        # Verify hash starts with the salt
        assert hashed2.startswith(salt + "$")

        # Hash the same password twice, should get different results with auto salt
        hashed3 = hash_password(password)
        assert hashed1 != hashed3

    def test_verify_password(self):
        """Test password verification."""
        password = "testpassword123"
        hashed = hash_password(password)

        # Verify correct password
        assert verify_password(hashed, password) is True

        # Verify incorrect password
        assert verify_password(hashed, "wrongpassword") is False

    def test_register_user(self, app, get_random_string):
        """Test user registration with valid data."""
        with app.app_context():
            # Register a new user
            result = register_user(
                "John",
                "Doe",
                f"john.doe.{get_random_string}@example.com",
                "Password123!",
                "01/01/1990",
            )

            # Verify success
            assert result["success"] is True
            assert "registered successfully" in result["message"]

    def test_register_user_with_invalid_data(self, app):
        """Test user registration with invalid data."""
        with app.app_context():
            # Test with invalid name
            result1 = register_user(
                "J",  # Too short
                "Doe",
                "john@example.com",
                "Password123!",
                "01/01/1990",
            )
            assert result1["success"] is False
            assert "at least 2 characters" in result1["message"]

            # Test with invalid email
            result2 = register_user(
                "John", "Doe", "not-an-email", "Password123!", "01/01/1990"
            )
            assert result2["success"] is False
            assert "Invalid email format" in result2["message"]

            # Test with invalid password
            result3 = register_user(
                "John",
                "Doe",
                "john@example.com",
                "password",  # Missing uppercase, number, and symbol
                "01/01/1990",
            )
            assert result3["success"] is False
            assert (
                "uppercase letter" in result3["message"]
                or "number" in result3["message"]
                or "symbol" in result3["message"]
            )

            # Test with invalid date
            result4 = register_user(
                "John",
                "Doe",
                "john@example.com",
                "Password123!",
                "31/02/1990",  # February 31st doesn't exist
            )
            assert result4["success"] is False
            assert "Invalid date" in result4["message"]

    def test_register_duplicate_user(self, app, test_user):
        """Test registering a user with an email that already exists."""
        with app.app_context():
            result = register_user(
                "Another",
                "User",
                test_user["email"],  # Same email as test_user
                "Password123!",
                "01/01/1990",
            )

            # Verify failure
            assert result["success"] is False
            assert "already exists" in result["message"]

    def test_authenticate_user(self, app, test_user):
        """Test user authentication."""
        with app.app_context():
            # Test successful authentication
            result = authenticate_user(test_user["email"], test_user["password"])

            # Verify success
            assert result["success"] is True
            assert "user" in result
            assert result["user"]["email"] == test_user["email"]

            # Test authentication with wrong password
            result = authenticate_user(test_user["email"], "wrongpassword")

            # Verify failure
            assert result["success"] is False
            assert "password" in result["message"].lower()

            # Test authentication with non-existent email
            result = authenticate_user("nonexistent@example.com", "anypassword")

            # Verify failure
            assert result["success"] is False
            assert "email" in result["message"].lower()

    def test_get_user_by_id(self, app, test_user):
        """Test retrieving a user by ID."""
        with app.app_context():
            # Get user by ID
            user = get_user_by_id(test_user["id"])

            # Verify user details
            assert user is not None
            assert user["id"] == test_user["id"]
            assert user["email"] == test_user["email"]

            # Test with non-existent ID
            non_existent_user = get_user_by_id(9999)

            # Verify result is None
            assert non_existent_user is None


# Helper function to generate random strings for emails
@pytest.fixture
def get_random_string():
    """Generate a random string for test email addresses."""
    import random
    import string

    return "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
