import pytest
from app.services.user_service import (
    validate_name, validate_email, validate_password, validate_date_of_birth
)

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit

class TestEquivalencePartitioning:
    """Tests that demonstrate equivalence partitioning technique."""
    
    def test_name_validation_with_equivalence_partitioning(self):
        """Test name validation using equivalence partitioning."""
        # Valid name partition (2 or more characters)
        valid_names = ["Jo", "John", "John-Paul", "O'Brien", "María José"]
        for name in valid_names:
            is_valid, message = validate_name(name)
            assert is_valid is True, f"Valid name {name} failed validation"
            assert message == ""
        
        # Invalid name partition (less than 2 characters)
        invalid_names = ["", "J", None]
        for name in invalid_names:
            is_valid, message = validate_name(name)
            assert is_valid is False, f"Invalid name {name} passed validation"
            assert "at least 2 characters" in message
    
    def test_email_validation_with_equivalence_partitioning(self):
        """Test validation of email addresses using equivalence partitioning."""
        # Valid email partition (valid format)
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user123@example.co.uk",
            "user-name@example.org"
        ]
        for email in valid_emails:
            is_valid, message = validate_email(email)
            assert is_valid is True, f"Valid email {email} failed validation"
            assert message == ""
        
        # Invalid email partitions
        # Partition 1: Missing @ symbol
        invalid_emails_missing_at = [
            "userexample.com",
            "user.example.com",
            "userexample"
        ]
        for email in invalid_emails_missing_at:
            is_valid, message = validate_email(email)
            assert is_valid is False, f"Invalid email {email} passed validation"
            assert "Invalid email format" in message
        
        # Partition 2: Missing domain
        invalid_emails_missing_domain = [
            "user@",
            "user@.",
            "user@.com"
        ]
        for email in invalid_emails_missing_domain:
            is_valid, message = validate_email(email)
            assert is_valid is False, f"Invalid email {email} passed validation"
            assert "Invalid email format" in message
        
        # Partition 3: Invalid characters
        invalid_emails_invalid_chars = [
            "user@exam ple.com",
            "user@exam\tple.com",
            "us er@example.com"
        ]
        for email in invalid_emails_invalid_chars:
            is_valid, message = validate_email(email)
            assert is_valid is False, f"Invalid email {email} passed validation"
            assert "Invalid email format" in message
    
    def test_password_validation_with_equivalence_partitioning(self):
        """Test password validation using equivalence partitioning."""
        # Valid password partition (meets all requirements)
        valid_passwords = [
            "Password1!",
            "SecurePass123@",
            "Abcde123!",
            "ComplexPwd1#"
        ]
        for password in valid_passwords:
            is_valid, message = validate_password(password)
            assert is_valid is True, f"Valid password failed validation"
            assert message == ""
        
        # Invalid password partitions
        # Partition 1: Too short (< 8 characters)
        short_passwords = ["Pass1!", "Ab1$", "P@ss1"]
        for password in short_passwords:
            is_valid, message = validate_password(password)
            assert is_valid is False, f"Short password {password} passed validation"
            assert "at least 8 characters" in message
        
        # Partition 2: Missing lowercase
        no_lowercase_passwords = ["PASSWORD123!", "PASS123$", "P4SSW0RD!"]
        for password in no_lowercase_passwords:
            is_valid, message = validate_password(password)
            assert is_valid is False, f"Password without lowercase {password} passed validation"
            assert "lowercase letter" in message
        
        # Partition 3: Missing uppercase
        no_uppercase_passwords = ["password123!", "pass123$", "p4ssw0rd!"]
        for password in no_uppercase_passwords:
            is_valid, message = validate_password(password)
            assert is_valid is False, f"Password without uppercase {password} passed validation"
            assert "uppercase letter" in message
        
        # Partition 4: Missing number
        no_number_passwords = ["Password!", "PassWord$", "PassWord!"]
        for password in no_number_passwords:
            is_valid, message = validate_password(password)
            assert is_valid is False, f"Password without number {password} passed validation"
            assert "number" in message
        
        # Partition 5: Missing symbol
        no_symbol_passwords = ["Password123", "PassWord123", "Pass123Word"]
        for password in no_symbol_passwords:
            is_valid, message = validate_password(password)
            assert is_valid is False, f"Password without symbol {password} passed validation"
            assert "symbol" in message
    
    def test_date_validation_with_equivalence_partitioning(self):
        """Test date validation using equivalence partitioning."""
        # Valid date partition (correct format and valid date)
        valid_dates = [
            "01/01/1990",
            "31/12/2000",
            "29/02/2020"  # Leap year
        ]
        for date in valid_dates:
            is_valid, message = validate_date_of_birth(date)
            assert is_valid is True, f"Valid date {date} failed validation"
            assert message == ""
        
        # Invalid date partitions
        # Partition 1: Invalid format
        invalid_format_dates = [
            "1/1/1990",
            "01-01-1990",
            "01/01/90",
            "1990/01/01",
            "01.01.1990"
        ]
        for date in invalid_format_dates:
            is_valid, message = validate_date_of_birth(date)
            assert is_valid is False, f"Date with invalid format {date} passed validation"
            assert "format" in message.lower()
        
        # Partition 2: Invalid dates (impossible dates)
        impossible_dates = [
            "31/04/2020",  # April has 30 days
            "29/02/2019",  # Not a leap year
            "00/01/2020",  # Day can't be 0
            "32/01/2020",  # Day can't be 32
            "01/13/2020"   # Month can't be 13
        ]
        for date in impossible_dates:
            is_valid, message = validate_date_of_birth(date)
            assert is_valid is False, f"Impossible date {date} passed validation"
            assert "Invalid date" in message