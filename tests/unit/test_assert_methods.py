import pytest
import sqlite3
from app.services.user_service import (
    hash_password,
    verify_password,
    register_user,
    authenticate_user,
    get_user_by_id,
)
from app.services.item_service import (
    get_all_items,
    get_item_by_id,
    search_items,
    add_item,
    update_item,
    delete_item,
)
from app.services.basket_service import (
    add_to_basket,
    get_basket_items,
    update_basket_quantity,
    remove_from_basket,
    clear_basket,
    get_basket_total,
)

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit


class TestAssertMethods:
    """Tests that demonstrate various assert methods for verification."""

    def test_assert_true_false(self):
        """Demonstrate assert True/False."""
        # Test password verification
        password = "testpassword123"
        hashed = hash_password(password)

        # Assert True: Verify correct password
        assert (
            verify_password(hashed, password) is True
        ), "Correct password should verify as True"

        # Assert False: Verify incorrect password
        assert (
            verify_password(hashed, "wrongpassword") is False
        ), "Wrong password should verify as False"

    def test_assert_equal(self, app, test_user):
        """Demonstrate assertEqual."""
        with app.app_context():
            # Get user by ID
            user = get_user_by_id(test_user["id"])

            # Assert Equal: User ID should match
            assert user["id"] == test_user["id"], "User ID should match"

            # Assert Equal: User email should match
            assert user["email"] == test_user["email"], "User email should match"

    def test_assert_not_equal(self, app):
        """Demonstrate assertNotEqual."""
        with app.app_context():
            # Add two different items
            add_item("Test Item 1", "Description 1", 10.99)
            add_item("Test Item 2", "Description 2", 20.99)

            # Get all items
            items = get_all_items()

            # Find our test items
            item1 = next((i for i in items if i["name"] == "Test Item 1"), None)
            item2 = next((i for i in items if i["name"] == "Test Item 2"), None)

            # Assert Not Equal: Items should have different IDs
            assert (
                item1["id"] != item2["id"]
            ), "Different items should have different IDs"

            # Assert Not Equal: Items should have different prices
            assert (
                item1["price"] != item2["price"]
            ), "Different items should have different prices"

    def test_assert_in(self, app):
        """Demonstrate assertIn (membership testing)."""
        with app.app_context():
            # Add an item with specific name
            add_item("Unique Test Item", "Description for assertIn test", 15.99)

            # Search for items with that name
            search_result = search_items("Unique Test")

            # Convert results to a list of names for easier assertion
            item_names = [item["name"] for item in search_result]

            # Assert In: Our item should be in the search results
            assert (
                "Unique Test Item" in item_names
            ), "Item name should be in search results"

    def test_assert_not_in(self, app):
        """Demonstrate assertNotIn."""
        with app.app_context():
            # Search for a non-existent item
            search_result = search_items("NonExistentTestItem12345")

            # Convert results to a list of names
            item_names = [item["name"] for item in search_result]

            # Assert Not In: Our item should not be in the results
            assert (
                "NonExistentTestItem12345" not in item_names
            ), "Non-existent item should not be in results"

    def test_assert_is_none(self, app):
        """Demonstrate assertIsNone."""
        with app.app_context():
            # Try to get a non-existent item
            item = get_item_by_id(9999)

            # Assert Is None: Item should be None
            assert item is None, "Non-existent item should be None"

    def test_assert_is_not_none(self, app, test_items):
        """Demonstrate assertIsNotNone."""
        with app.app_context():
            # Get an existing item
            item = get_item_by_id(test_items[0]["id"])

            # Assert Is Not None: Item should not be None
            assert item is not None, "Existing item should not be None"

    def test_assert_raises(self, app):
        """Demonstrate assertRaises."""
        with app.app_context():
            # Create a test to force a SQLite error (unique constraint violation)
            def cause_sqlite_error():
                from app.db import get_db

                db = get_db()
                # Try to insert a duplicate email (will fail due to UNIQUE constraint)
                db.execute(
                    "INSERT INTO users (first_name, last_name, email, password, date_of_birth) "
                    "VALUES (?, ?, ?, ?, ?)",
                    ("Test", "User", "testuser@example.com", "password", "01/01/1990"),
                )
                db.execute(
                    "INSERT INTO users (first_name, last_name, email, password, date_of_birth) "
                    "VALUES (?, ?, ?, ?, ?)",
                    ("Test", "User", "testuser@example.com", "password", "01/01/1990"),
                )

            # Assert Raises: Should raise a SQLite error for duplicate email
            with pytest.raises(sqlite3.IntegrityError):
                cause_sqlite_error()

    def test_assert_greater_less(self, app, test_user, test_items):
        """Demonstrate greater than and less than assertions."""
        with app.app_context():
            # Add items to basket with known prices
            add_to_basket(
                test_user["id"], test_items[0]["id"], 2
            )  # 2 * price of first item

            # Calculate basket total
            total = get_basket_total(test_user["id"])

            # Expected total (price of first item * 2)
            expected_min = test_items[0]["price"] * 1.9  # Slightly less than 2*price
            expected_max = test_items[0]["price"] * 2.1  # Slightly more than 2*price

            # Assert Greater: Total should be greater than minimum expected
            assert (
                total > expected_min
            ), "Basket total should be greater than minimum expected"

            # Assert Less: Total should be less than maximum expected
            assert (
                total < expected_max
            ), "Basket total should be less than maximum expected"

    def test_assert_almost_equal(self, app, test_user, test_items):
        """Demonstrate approximately equal assertions for floating point."""
        with app.app_context():
            # Clear existing basket
            clear_basket(test_user["id"])

            # Add item with known price
            add_to_basket(test_user["id"], test_items[0]["id"], 1)

            # Get basket total
            total = get_basket_total(test_user["id"])

            # For floating point values, use approximate equality
            # Here we check that the total is within 0.01 of the expected price
            assert (
                abs(total - test_items[0]["price"]) < 0.01
            ), "Basket total should be approximately equal to item price"

    def test_assert_length(self, app, test_user, test_items):
        """Demonstrate assertions on collection length."""
        with app.app_context():
            # Clear existing basket
            clear_basket(test_user["id"])

            # Add exact number of unique items
            for i in range(3):
                if i < len(test_items):
                    add_to_basket(test_user["id"], test_items[i]["id"], 1)

            # Get basket items
            basket_items = get_basket_items(test_user["id"])

            # Assert Length: Basket should have exactly 3 items
            assert len(basket_items) == 3, "Basket should have exactly 3 items"

            # Remove one item
            remove_from_basket(basket_items[0]["id"])

            # Get updated basket
            basket_items = get_basket_items(test_user["id"])

            # Assert Length: Basket should now have exactly 2 items
            assert (
                len(basket_items) == 2
            ), "After removing 1 item, basket should have 2 items"
