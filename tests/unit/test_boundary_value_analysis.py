import pytest
from app.services.user_service import (
    validate_name, validate_email, validate_password, validate_date_of_birth
)
from app.services.basket_service import add_to_basket, update_basket_quantity

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit

class TestBoundaryValueAnalysis:
    """Tests that demonstrate boundary value analysis technique."""
    
    def test_name_length_boundaries(self):
        """Test name validation at length boundaries."""
        # Boundary: Exactly 2 characters (minimum valid length)
        is_valid, message = validate_name("Jo")
        assert is_valid is True, "Name with exactly 2 characters should be valid"
        
        # Boundary: 1 character (just below minimum)
        is_valid, message = validate_name("J")
        assert is_valid is False, "Name with 1 character should be invalid"
        assert "at least 2 characters" in message
        
        # Boundary: 0 characters (empty string)
        is_valid, message = validate_name("")
        assert is_valid is False, "Empty name should be invalid"
        assert "at least 2 characters" in message
        
        # Test very long name (not a formal boundary, but good to check)
        very_long_name = "A" * 100
        is_valid, message = validate_name(very_long_name)
        assert is_valid is True, "Very long name should still be valid"
    
    def test_password_length_boundaries(self):
        """Test password validation at length boundaries."""
        # Valid password template with all requirements
        # We'll modify the length while keeping other requirements
        
        # Boundary: Exactly 8 characters (minimum valid length)
        is_valid, message = validate_password("Aa1!wxyz")
        assert is_valid is True, "Password with exactly 8 characters should be valid"
        
        # Boundary: 7 characters (just below minimum)
        is_valid, message = validate_password("Aa1!xyz")
        assert is_valid is False, "Password with 7 characters should be invalid"
        assert "at least 8 characters" in message
        
        # Boundary: 9 characters (just above minimum)
        is_valid, message = validate_password("Aa1!xyzab")
        assert is_valid is True, "Password with 9 characters should be valid"
        
        # Test very long password
        very_long_password = "Aa1!" + "x" * 96  # 100 characters total
        is_valid, message = validate_password(very_long_password)
        assert is_valid is True, "Very long password should still be valid"
    
    def test_date_boundaries(self):
        """Test date validation at calendar boundaries."""
        # Test boundary days for months
        
        # January 1st (first day of year)
        is_valid, message = validate_date_of_birth("01/01/2000")
        assert is_valid is True, "January 1st should be valid"
        
        # January 31st (last day of January)
        is_valid, message = validate_date_of_birth("31/01/2000")
        assert is_valid is True, "January 31st should be valid"
        
        # February boundary tests
        # February 28th in non-leap year
        is_valid, message = validate_date_of_birth("28/02/2019")
        assert is_valid is True, "February 28th in non-leap year should be valid"
        
        # February 29th in non-leap year
        is_valid, message = validate_date_of_birth("29/02/2019")
        assert is_valid is False, "February 29th in non-leap year should be invalid"
        assert "Invalid date" in message
        
        # February 29th in leap year
        is_valid, message = validate_date_of_birth("29/02/2020")
        assert is_valid is True, "February 29th in leap year should be valid"
        
        # Day 0 (invalid)
        is_valid, message = validate_date_of_birth("00/01/2000")
        assert is_valid is False, "Day 0 should be invalid"
        assert "Invalid date" in message
        
        # Month 0 (invalid)
        is_valid, message = validate_date_of_birth("01/00/2000")
        assert is_valid is False, "Month 0 should be invalid"
        assert "Invalid date" in message
        
        # December 31st (last day of year)
        is_valid, message = validate_date_of_birth("31/12/2000")
        assert is_valid is True, "December 31st should be valid"
        
        # December 32nd (invalid)
        is_valid, message = validate_date_of_birth("32/12/2000")
        assert is_valid is False, "December 32nd should be invalid"
        assert "Invalid date" in message
    
    def test_basket_quantity_boundaries(self, app, test_user, test_items):
        """Test basket quantity boundaries."""
        with app.app_context():
            # Add an item with minimum quantity (1)
            result = add_to_basket(test_user['id'], test_items[0]['id'], 1)
            assert result['success'] is True, "Adding item with quantity 1 should succeed"
            
            # Get the basket item ID
            from app.db import get_db
            db = get_db()
            basket_item = db.execute(
                'SELECT id FROM basket_items WHERE user_id = ? AND item_id = ?',
                (test_user['id'], test_items[0]['id'])
            ).fetchone()
            basket_item_id = basket_item['id']
            
            # Update to 0 quantity (should remove the item)
            result = update_basket_quantity(basket_item_id, 0)
            assert result['success'] is True, "Updating to quantity 0 should succeed (remove item)"
            
            # Verify item was removed
            basket_item = db.execute(
                'SELECT id FROM basket_items WHERE id = ?', (basket_item_id,)
            ).fetchone()
            assert basket_item is None, "Item with quantity 0 should be removed"
            
            # Re-add the item for further tests
            add_to_basket(test_user['id'], test_items[0]['id'], 1)
            basket_item = db.execute(
                'SELECT id FROM basket_items WHERE user_id = ? AND item_id = ?',
                (test_user['id'], test_items[0]['id'])
            ).fetchone()
            basket_item_id = basket_item['id']
            
            # Update to negative quantity (should remove the item)
            result = update_basket_quantity(basket_item_id, -1)
            assert result['success'] is True, "Updating to negative quantity should succeed (remove item)"
            
            # Verify item was removed
            basket_item = db.execute(
                'SELECT id FROM basket_items WHERE id = ?', (basket_item_id,)
            ).fetchone()
            assert basket_item is None, "Item with negative quantity should be removed"
            
            # Add with very large quantity
            large_quantity = 999
            result = add_to_basket(test_user['id'], test_items[0]['id'], large_quantity)
            assert result['success'] is True, f"Adding item with quantity {large_quantity} should succeed"
            
            # Verify the quantity was set correctly
            basket_item = db.execute(
                'SELECT quantity FROM basket_items WHERE user_id = ? AND item_id = ?',
                (test_user['id'], test_items[0]['id'])
            ).fetchone()
            assert basket_item['quantity'] == large_quantity, f"Quantity should be {large_quantity}"