import os
import tempfile
import pytest
from app import create_app
from app.db import get_db, init_db
from app.services.user_service import register_user, authenticate_user
from app.services.item_service import add_item


@pytest.fixture
def app():
    """Create a Flask application for testing."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
        }
    )

    # Create the database and load test data
    with app.app_context():
        init_db()
        # Create sample test data
        _initialize_test_data()

    yield app

    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


# Test client simulates a browser and allows you to make requests to the application
@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


# CLI runner allows you to invoke command line interface commands
@pytest.fixture
def runner(app):
    """Create a CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def test_user(app):
    """Create a test user and return the user details."""
    with app.app_context():
        # Check if user already exists first
        db = get_db()
        existing_user = db.execute(
            "SELECT * FROM users WHERE email = ?", ("testuser@example.com",)
        ).fetchone()

        if existing_user:
            user_id = existing_user["id"]
        else:
            register_user(
                "Test", "User", "testuser@example.com", "Password123!", "01/01/1990"
            )
            user = db.execute(
                "SELECT * FROM users WHERE email = ?", ("testuser@example.com",)
            ).fetchone()
            user_id = user["id"]

        return {
            "id": user_id,
            "email": "testuser@example.com",
            "password": "Password123!",
        }


@pytest.fixture
def auth_client(client, test_user):
    """Create a client that is authenticated with the test user."""
    client.post(
        "/auth/login",
        data={"email": test_user["email"], "password": test_user["password"]},
    )
    return client


@pytest.fixture
def test_items(app):
    """Create test items and return their details."""
    with app.app_context():
        # Check if we already have test items
        db = get_db()
        existing_items = db.execute("SELECT COUNT(*) as count FROM items").fetchone()

        if existing_items["count"] > 0:
            # Items already exist, just return them
            items = db.execute("SELECT * FROM items LIMIT 3").fetchall()
            return [dict(item) for item in items]

        # Create test items
        item_data = [
            {
                "name": "Test Item 1",
                "description": "Description for test item 1",
                "price": 10.99,
                "image_url": "https://via.placeholder.com/150",
            },
            {
                "name": "Test Item 2",
                "description": "Description for test item 2",
                "price": 20.99,
                "image_url": "https://via.placeholder.com/150",
            },
            {
                "name": "Test Item 3",
                "description": "Description for test item 3",
                "price": 30.99,
                "image_url": "https://via.placeholder.com/150",
            },
        ]

        created_items = []
        for item in item_data:
            add_item(
                item["name"], item["description"], item["price"], item["image_url"]
            )

            # Get the newly created item
            new_item = db.execute(
                "SELECT * FROM items WHERE name = ?", (item["name"],)
            ).fetchone()

            created_items.append(dict(new_item))

        return created_items


def _initialize_test_data():
    """Initialize database with test data."""
    # Create test user
    register_user("Test", "User", "testuser@example.com", "Password123!", "01/01/1990")

    # Create some test items
    add_item("Laptop", "A test laptop", 999.99, "https://via.placeholder.com/150")
    add_item(
        "Smartphone", "A test smartphone", 499.99, "https://via.placeholder.com/150"
    )
    add_item("Headphones", "Test headphones", 99.99, "https://via.placeholder.com/150")
