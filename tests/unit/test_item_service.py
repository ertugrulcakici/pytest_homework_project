import pytest
from app.services.item_service import (
    get_all_items, get_item_by_id, search_items,
    add_item, update_item, delete_item
)

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit

class TestItemService:
    """Unit tests for item service."""
    
    def test_get_all_items(self, app, test_items):
        """Test retrieving all items."""
        with app.app_context():
            items = get_all_items()
            
            # Verify we got a list of items
            assert isinstance(items, list)
            assert len(items) >= len(test_items)
            
            # Verify each test item is in the result
            for test_item in test_items:
                found = False
                for item in items:
                    if item['id'] == test_item['id']:
                        found = True
                        break
                assert found, f"Test item {test_item['id']} not found in results"
    
    def test_get_item_by_id(self, app, test_items):
        """Test retrieving a specific item by ID."""
        with app.app_context():
            test_item = test_items[0]
            
            # Retrieve the item
            item = get_item_by_id(test_item['id'])
            
            # Verify it's the correct item
            assert item is not None
            assert item['id'] == test_item['id']
            assert item['name'] == test_item['name']
            assert item['description'] == test_item['description']
            assert abs(item['price'] - test_item['price']) < 0.01
            assert item['image_url'] == test_item['image_url']
    
    def test_get_nonexistent_item(self, app):
        """Test retrieving a non-existent item."""
        with app.app_context():
            # Try to get an item with an invalid ID
            item = get_item_by_id(9999)
            
            # Verify we got None
            assert item is None
    
    def test_search_items(self, app, test_items):
        """Test searching for items by name."""
        with app.app_context():
            # Get a search term from one of the test items
            search_term = test_items[0]['name'].split()[0]
            
            # Search for items
            results = search_items(search_term)
            
            # Verify we got results
            assert isinstance(results, list)
            assert len(results) > 0
            
            # Verify the search term is in each result's name
            for result in results:
                assert search_term.lower() in result['name'].lower()
    
    def test_add_item(self, app):
        """Test adding a new item."""
        with app.app_context():
            # Define a new item
            new_item = {
                'name': 'New Test Item',
                'description': 'A newly added test item',
                'price': 15.99,
                'image_url': 'https://via.placeholder.com/150'
            }
            
            # Add the item
            result = add_item(
                new_item['name'],
                new_item['description'],
                new_item['price'],
                new_item['image_url']
            )
            
            # Verify the result
            assert result['success'] is True
            
            # Retrieve all items and check if our new item is there
            items = get_all_items()
            found_item = None
            for item in items:
                if item['name'] == new_item['name']:
                    found_item = item
                    break
            
            # Verify the item was added correctly
            assert found_item is not None
            assert found_item['name'] == new_item['name']
            assert found_item['description'] == new_item['description']
            assert abs(found_item['price'] - new_item['price']) < 0.01
            assert found_item['image_url'] == new_item['image_url']
    
    def test_update_item(self, app, test_items):
        """Test updating an existing item."""
        with app.app_context():
            test_item = test_items[0]
            
            # Define updated values
            updated_values = {
                'name': f"{test_item['name']} Updated",
                'description': f"{test_item['description']} Updated",
                'price': test_item['price'] + 10.0,
                'image_url': 'https://via.placeholder.com/200'
            }
            
            # Update the item
            result = update_item(
                test_item['id'],
                updated_values['name'],
                updated_values['description'],
                updated_values['price'],
                updated_values['image_url']
            )
            
            # Verify the result
            assert result['success'] is True
            
            # Retrieve the updated item
            updated_item = get_item_by_id(test_item['id'])
            
            # Verify the updates
            assert updated_item['name'] == updated_values['name']
            assert updated_item['description'] == updated_values['description']
            assert abs(updated_item['price'] - updated_values['price']) < 0.01
            assert updated_item['image_url'] == updated_values['image_url']
    
    def test_delete_item(self, app, test_items):
        """Test deleting an item."""
        with app.app_context():
            # Add a new item specifically for deletion
            result = add_item(
                'Item To Delete',
                'This item will be deleted',
                9.99,
                'https://via.placeholder.com/150'
            )
            assert result['success'] is True
            
            # Find the newly created item
            items = get_all_items()
            item_to_delete = None
            for item in items:
                if item['name'] == 'Item To Delete':
                    item_to_delete = item
                    break
            
            assert item_to_delete is not None
            
            # Delete the item
            result = delete_item(item_to_delete['id'])
            
            # Verify the result
            assert result['success'] is True
            
            # Try to retrieve the deleted item
            deleted_item = get_item_by_id(item_to_delete['id'])
            
            # Verify it's gone
            assert deleted_item is None
