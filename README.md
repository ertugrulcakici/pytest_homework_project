# Online Shop

TEST - A Flask web application for an online shop with features like authentication, item listings, search, and shopping basket functionality.

## Features

* User authentication (login, register, access token) - **Required for all features**
* Item listings on the main page
* Search functionality for items by name
* Adding items to basket
* Removing items from basket
* SQLite database with sample data
* GitHub Actions for automated testing

## Project Structure

```
online_shop/
├── app/
│   ├── db/                 # Database related modules
│   ├── models/             # Data models
│   ├── routes/             # Route blueprints
│   │   ├── auth.py         # Authentication routes
│   │   ├── main.py         # Main routes
│   │   └── shop.py         # Shop routes
│   ├── services/           # Business logic
│   │   ├── auth_decorator.py      # Authentication decorator
│   │   ├── basket_service.py      # Basket management
│   │   ├── item_service.py        # Item management
│   │   ├── token_service.py       # JWT token handling
│   │   └── user_service.py        # User management
│   ├── static/             # Static files (CSS, JS)
│   ├── templates/          # HTML templates
│   │   ├── auth/           # Authentication templates
│   │   ├── main/           # Main templates
│   │   └── shop/           # Shop templates
│   └── __init__.py         # App factory
├── data/                   # SQLite database
├── tests/                  # Test modules
│   └── unit/               # Unit tests
│       ├── test_user_service.py                # User service tests
│       ├── test_item_service.py                # Item service tests
│       ├── test_basket_service.py              # Basket service tests
│       ├── test_token_service.py               # Token service tests
│       ├── test_equivalence_partitioning.py    # Equivalence partitioning examples
│       ├── test_boundary_value_analysis.py     # Boundary value analysis examples
│       └── test_assert_methods.py              # Assert method examples
├── .github/workflows/      # GitHub Actions workflows
├── run_unit_tests.py       # Script to run specific unit tests
├── run_all_tests.py        # Script to run all unit tests with coverage
├── requirements.txt        # Project dependencies
└── run.py                  # Application entry point
```

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```
   flask --app app init-db
   ```
4. Generate sample data:
   ```
   flask --app app generate-data
   ```
5. Run the application:
   ```
   python run.py
   ```

## Authentication Flow

The application requires authentication for all features:

1. When a user accesses the root URL (`/`):
   - If not logged in, they are redirected to the login page
   - If logged in, they are redirected to the home page

2. New users can register by providing:
   - First name (minimum 2 characters)
   - Last name (minimum 2 characters)
   - Email (valid email format)
   - Password (minimum 8 characters, must include lowercase, uppercase, number, and symbol)
   - Date of birth (dd/mm/yyyy format)

3. After successful login, users gain access to:
   - Home page with featured products
   - Full shop item listings
   - Search functionality
   - Shopping basket

## Unit Testing

### Running All Unit Tests

To run all unit tests with a single command and generate a unified coverage report:

```bash
# Run all unit tests with full coverage reporting
python run_all_tests.py

# Run specific unit tests
python run_unit_tests.py

# Generate HTML coverage report
python run_unit_tests.py --html
```

### Testing Specific Services

You can run tests for specific services:

```bash
# Test user service (including validation)
python run_unit_tests.py --service user

# Test item service
python run_unit_tests.py --service item

# Test basket service
python run_unit_tests.py --service basket

# Test token service
python run_unit_tests.py --service token
```

### Testing Specific Testing Techniques

You can run tests for specific testing techniques:

```bash
# Run equivalence partitioning tests
python run_unit_tests.py --service equivalence

# Run boundary value analysis tests
python run_unit_tests.py --service boundary

# Run assert method demonstration tests
python run_unit_tests.py --service assert
```

### Test Coverage

The unit tests cover:

1. **User Service**:
   - Input validation (name, email, password, date)
   - User registration with validation
   - User authentication
   - Password hashing and verification

2. **Item Service**:
   - Adding, retrieving, updating, and deleting items
   - Searching for items
   - Error handling

3. **Basket Service**:
   - Adding items to basket
   - Updating item quantities
   - Removing items
   - Calculating basket totals

4. **Token Service**:
   - Token generation
   - Token validation
   - Handling expired or invalid tokens

## Routes

- `/` - Main entry point (redirects based on auth status)
- `/home` - Home page with featured products (requires login)
- `/auth/register` - User registration
- `/auth/login` - User login
- `/auth/logout` - User logout
- `/shop/items` - All shop items (requires login)
- `/shop/items/<id>` - Item detail (requires login)
- `/shop/search` - Search for items (requires login)
- `/shop/basket` - View basket (requires login)
- `/profile` - User profile (requires login)

## API Endpoints

- `/shop/api/items` - Get all items (requires authentication)
- `/shop/api/items/<id>` - Get a specific item (requires authentication)
- `/shop/api/search?query=<query>` - Search for items (requires authentication)
- `/shop/api/basket` - Get basket items (requires authentication)
- `/auth/api/login` - Login and get access token

## Testing Techniques

Tests implement various verification and validation techniques:

### 1. Equivalence Partitioning

Equivalence partitioning is a testing technique that divides input data into groups that are expected to exhibit similar behavior. This allows us to test one representative value from each group rather than every possible input.

Examples in our codebase:
- **Email Validation**: Partitioned into valid emails, emails missing @, emails missing domain, emails with invalid characters
- **Password Validation**: Partitioned into valid passwords, passwords too short, passwords missing lowercase/uppercase/symbols/numbers
- **Date Validation**: Partitioned into valid dates, incorrectly formatted dates, and impossible dates

```python
# Example: Email validation with equivalence partitioning
def test_email_validation_with_equivalence_partitioning(self):
    # Valid email partition
    valid_emails = ["user@example.com", "user.name@example.com"]
    
    # Invalid email partitions
    invalid_emails_missing_at = ["userexample.com", "user.example.com"]
    invalid_emails_missing_domain = ["user@", "user@."]
    invalid_emails_invalid_chars = ["user@exam ple.com", "us er@example.com"]
    
    # Test each partition
    for email in valid_emails:
        is_valid, _ = validate_email(email)
        assert is_valid is True
    
    for email in invalid_emails_missing_at:
        is_valid, _ = validate_email(email)
        assert is_valid is False
```

### 2. Boundary Value Analysis

Boundary value analysis focuses on testing at the boundaries of input domains, since errors often occur at the extreme ends of input ranges.

Examples in our codebase:
- **Name Length**: Testing exactly 2 characters (minimum), 1 character (invalid), and very long names
- **Password Length**: Testing exactly 8 characters (minimum), 7 characters (invalid), 9 characters (valid)
- **Date Validation**: Testing boundary days like February 28/29 in leap/non-leap years, day 0, month 0, etc.

```python
# Example: Testing name length boundaries
def test_name_length_boundaries(self):
    # Boundary: Exactly 2 characters (minimum valid length)
    is_valid, _ = validate_name("Jo")
    assert is_valid is True
    
    # Boundary: 1 character (just below minimum)
    is_valid, _ = validate_name("J")
    assert is_valid is False
```

### 3. Assert Methods

Various assertion methods are used for verification:

- **assert True/False**: Verifying boolean conditions
- **assert equal/not equal**: Comparing values for equality/inequality
- **assert is None/is not None**: Checking for existence
- **assert in/not in**: Testing for membership in collections
- **assert raises**: Verifying exceptions are raised
- **assert greater/less than**: Comparing numeric values
- **assert almost equal**: Comparing floating-point values

```python
# Example: Different assert methods
def test_assert_methods(self):
    # Assert True
    assert verify_password(hashed, password) is True
    
    # Assert Equal
    assert user['id'] == test_user['id']
    
    # Assert Is None
    assert get_item_by_id(9999) is None
    
    # Assert Raises
    with pytest.raises(sqlite3.IntegrityError):
        cause_sqlite_error()
```

### 4. Database Testing

- In-memory SQLite database for isolated testing
- Test fixtures to create and tear down test data
- Testing all CRUD operations on users, items, and basket items

### 5. Automated Testing with GitHub Actions

Our CI/CD pipeline automatically runs tests on every push and pull request:

- Runs all unit tests
- Runs specialized equivalence partitioning tests
- Runs specialized boundary value analysis tests
- Runs specialized assert method tests
- Generates and uploads coverage reports

## GitHub Actions

The project is configured with GitHub Actions for continuous integration:
- Automatic testing on push and pull requests
- Database initialization and sample data generation
- Test coverage reports
- Codecov integration for visualizing test coverage

To see the GitHub Actions workflow in action, push changes to the repository and check the "Actions" tab on GitHub.
