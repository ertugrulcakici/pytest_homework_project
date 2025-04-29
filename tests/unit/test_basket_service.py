import pytest
from app.services.basket_service import (
    add_to_basket, get_basket_items, update_basket_quantity,
    remove_from_basket, clear_basket, get_basket_total
)

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit

class TestBasketService:
    """Unit tests for the basket service."""
    
    def test_add_to_basket(self, app, test_user, test_items):
        """Test adding an item to the basket."""
        with app.app_context():
            # Add an item to the basket
            result = add_to_basket(test_user['id'], test_items[0]['id'], 2)
            
            # Check the result
            assert result['success'] is True
            assert "added to basket" in result['message'].lower()
            
            # Verify item was added correctly
            basket_items = get_basket_items(test_user['id'])
            
            # Find the item we just added
            added_item = None
            for item in basket_items:
                if item['item_id'] == test_items[0]['id']:
                    added_item = item
                    break
            
            # Verify item details
            assert added_item is not None
            assert added_item['user_id'] == test_user['id']
            assert added_item['item_id'] == test_items[0]['id']
            assert added_item['quantity'] == 2
    
    def test_update_basket_quantity(self, app, test_user, test_items):
        """Test updating the quantity of an item in the basket."""
        with app.app_context():
            # First add an item to the basket
            add_to_basket(test_user['id'], test_items[0]['id'], 1)
            
            # Get the basket item ID
            basket_items = get_basket_items(test_user['id'])
            basket_item_id = None
            for item in basket_items:
                if item['item_id'] == test_items[0]['id']:
                    basket_item_id = item['id']
                    break
            
            assert basket_item_id is not None
            
            # Update the quantity
            result = update_basket_quantity(basket_item_id, 5)
            
            # Check the result
            assert result['success'] is True
            
            # Verify quantity was updated
            updated_basket = get_basket_items(test_user['id'])
            updated_item = None
            for item in updated_basket:
                if item['id'] == basket_item_id:
                    updated_item = item
                    break
            
            assert updated_item is not None
            assert updated_item['quantity'] == 5
    
    def test_remove_from_basket(self, app, test_user, test_items):
        """Test removing an item from the basket."""
        with app.app_context():
            # Add an item to the basket
            add_to_basket(test_user['id'], test_items[1]['id'], 3)
            
            # Get the basket item ID
            basket_items = get_basket_items(test_user['id'])
            basket_item_id = None
            for item in basket_items:
                if item['item_id'] == test_items[1]['id']:
                    basket_item_id = item['id']
                    break
            
            assert basket_item_id is not None
            
            # Remove the item
            result = remove_from_basket(basket_item_id)
            
            # Check the result
            assert result['success'] is True
            
            # Verify item was removed
            updated_basket = get_basket_items(test_user['id'])
            removed_item = None
            for item in updated_basket:
                if item['id'] == basket_item_id:
                    removed_item = item
                    break
            
            assert removed_item is None
    
    def test_get_basket_total(self, app, test_user, test_items):
        """Test calculating the total cost of items in the basket."""
        with app.app_context():
            # Clear existing basket if any
            clear_basket(test_user['id'])
            
            # Add multiple items with known prices and quantities
            add_to_basket(test_user['id'], test_items[0]['id'], 2)  # 2 * price of item 0
            add_to_basket(test_user['id'], test_items[1]['id'], 1)  # 1 * price of item 1
            
            # Calculate expected total
            expected_total = (test_items[0]['price'] * 2) + (test_items[1]['price'] * 1)
            
            # Get actual total
            actual_total = get_basket_total(test_user['id'])
            
            # Compare with small tolerance for floating point errors
            assert abs(actual_total - expected_total) < 0.01
    
    def test_clear_basket(self, app, test_user, test_items):
        """Test clearing all items from the basket."""
        with app.app_context():
            # Add multiple items to the basket
            add_to_basket(test_user['id'], test_items[0]['id'], 2)
            add_to_basket(test_user['id'], test_items[1]['id'], 1)
            
            # Verify items are in the basket
            basket_before = get_basket_items(test_user['id'])
            assert len(basket_before) > 0
            
            # Clear the basket
            result = clear_basket(test_user['id'])
            
            # Check the result
            assert result['success'] is True
            
            # Verify basket is empty
            basket_after = get_basket_items(test_user['id'])
            assert len(basket_after) == 0
