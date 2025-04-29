import sqlite3
from app.db import get_db

def get_all_items():
    """Get all items from the database."""
    db = get_db()
    items = db.execute(
        'SELECT * FROM items ORDER BY name'
    ).fetchall()
    
    return [dict(item) for item in items]

def get_item_by_id(item_id):
    """Get an item by its ID."""
    db = get_db()
    item = db.execute(
        'SELECT * FROM items WHERE id = ?',
        (item_id,)
    ).fetchone()
    
    if item is None:
        return None
    
    return dict(item)

def search_items(query):
    """Search for items by name."""
    db = get_db()
    items = db.execute(
        'SELECT * FROM items WHERE name LIKE ? ORDER BY name',
        (f'%{query}%',)
    ).fetchall()
    
    return [dict(item) for item in items]

def add_item(name, description, price, image_url=None):
    """Add a new item to the database."""
    db = get_db()
    try:
        db.execute(
            'INSERT INTO items (name, description, price, image_url) VALUES (?, ?, ?, ?)',
            (name, description, price, image_url)
        )
        db.commit()
        return {'success': True, 'message': 'Item added successfully'}
    except sqlite3.Error as e:
        return {'success': False, 'message': f"Database error: {e}"}

def update_item(item_id, name, description, price, image_url=None):
    """Update an existing item."""
    db = get_db()
    try:
        db.execute(
            'UPDATE items SET name = ?, description = ?, price = ?, image_url = ? WHERE id = ?',
            (name, description, price, image_url, item_id)
        )
        db.commit()
        return {'success': True, 'message': 'Item updated successfully'}
    except sqlite3.Error as e:
        return {'success': False, 'message': f"Database error: {e}"}

def delete_item(item_id):
    """Delete an item from the database."""
    db = get_db()
    try:
        db.execute('DELETE FROM items WHERE id = ?', (item_id,))
        db.commit()
        return {'success': True, 'message': 'Item deleted successfully'}
    except sqlite3.Error as e:
        return {'success': False, 'message': f"Database error: {e}"}

def generate_sample_items():
    """Generate sample items for testing and demonstration."""
    sample_items = [
        {
            'name': 'Laptop',
            'description': 'High-performance laptop with 16GB RAM and 512GB SSD.',
            'price': 999.99,
            'image_url': 'https://via.placeholder.com/150'
        },
        {
            'name': 'Smartphone',
            'description': 'Latest smartphone with 6.5" screen and 128GB storage.',
            'price': 699.99,
            'image_url': 'https://via.placeholder.com/150'
        },
        {
            'name': 'Headphones',
            'description': 'Noise-cancelling wireless headphones with 20-hour battery life.',
            'price': 199.99,
            'image_url': 'https://via.placeholder.com/150'
        },
        {
            'name': 'Tablet',
            'description': '10.2" tablet with 64GB storage and long battery life.',
            'price': 329.99,
            'image_url': 'https://via.placeholder.com/150'
        },
        {
            'name': 'Smart Watch',
            'description': 'Fitness tracking smart watch with heart rate monitor.',
            'price': 249.99,
            'image_url': 'https://via.placeholder.com/150'
        },
        {
            'name': 'Wireless Earbuds',
            'description': 'True wireless earbuds with charging case.',
            'price': 129.99,
            'image_url': 'https://via.placeholder.com/150'
        },
        {
            'name': 'Desktop Computer',
            'description': 'Powerful desktop computer for gaming and productivity.',
            'price': 1299.99,
            'image_url': 'https://via.placeholder.com/150'
        },
        {
            'name': 'Keyboard',
            'description': 'Mechanical keyboard with RGB lighting.',
            'price': 89.99,
            'image_url': 'https://via.placeholder.com/150'
        },
        {
            'name': 'Mouse',
            'description': 'Ergonomic wireless mouse with adjustable DPI.',
            'price': 49.99,
            'image_url': 'https://via.placeholder.com/150'
        },
        {
            'name': 'Monitor',
            'description': '27" 4K monitor with HDR support.',
            'price': 349.99,
            'image_url': 'https://via.placeholder.com/150'
        }
    ]
    
    db = get_db()
    for item in sample_items:
        try:
            db.execute(
                'INSERT INTO items (name, description, price, image_url) VALUES (?, ?, ?, ?)',
                (item['name'], item['description'], item['price'], item['image_url'])
            )
        except sqlite3.Error:
            # Skip if item already exists
            pass
    
    db.commit()
    return {'success': True, 'message': f'Added {len(sample_items)} sample items'}
