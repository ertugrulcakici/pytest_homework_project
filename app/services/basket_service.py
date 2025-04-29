import sqlite3
from app.db import get_db

def get_basket_items(user_id):
    """Get all items in a user's basket with item details."""
    db = get_db()
    basket_items = db.execute(
        '''
        SELECT b.id, b.user_id, b.item_id, b.quantity, 
               i.name, i.description, i.price, i.image_url
        FROM basket_items b
        JOIN items i ON b.item_id = i.id
        WHERE b.user_id = ?
        ORDER BY b.id
        ''',
        (user_id,)
    ).fetchall()
    
    return [dict(item) for item in basket_items]

def add_to_basket(user_id, item_id, quantity=1):
    """Add an item to the user's basket."""
    db = get_db()
    
    try:
        # Check if item exists
        item = db.execute('SELECT id FROM items WHERE id = ?', (item_id,)).fetchone()
        if item is None:
            return {'success': False, 'message': 'Item not found'}
        
        # Check if item is already in basket
        existing = db.execute(
            'SELECT id, quantity FROM basket_items WHERE user_id = ? AND item_id = ?',
            (user_id, item_id)
        ).fetchone()
        
        if existing:
            # Update quantity if already in basket
            new_quantity = existing['quantity'] + quantity
            db.execute(
                'UPDATE basket_items SET quantity = ? WHERE id = ?',
                (new_quantity, existing['id'])
            )
        else:
            # Add new basket item
            db.execute(
                'INSERT INTO basket_items (user_id, item_id, quantity) VALUES (?, ?, ?)',
                (user_id, item_id, quantity)
            )
        
        db.commit()
        return {'success': True, 'message': 'Item added to basket'}
    except sqlite3.Error as e:
        return {'success': False, 'message': f"Database error: {e}"}

def update_basket_quantity(basket_item_id, quantity):
    """Update the quantity of an item in the basket."""
    db = get_db()
    
    try:
        if quantity <= 0:
            # Remove item if quantity is 0 or negative
            db.execute('DELETE FROM basket_items WHERE id = ?', (basket_item_id,))
        else:
            # Update quantity
            db.execute(
                'UPDATE basket_items SET quantity = ? WHERE id = ?',
                (quantity, basket_item_id)
            )
        
        db.commit()
        return {'success': True, 'message': 'Basket updated'}
    except sqlite3.Error as e:
        return {'success': False, 'message': f"Database error: {e}"}

def remove_from_basket(basket_item_id):
    """Remove an item from the basket."""
    db = get_db()
    
    try:
        db.execute('DELETE FROM basket_items WHERE id = ?', (basket_item_id,))
        db.commit()
        return {'success': True, 'message': 'Item removed from basket'}
    except sqlite3.Error as e:
        return {'success': False, 'message': f"Database error: {e}"}

def clear_basket(user_id):
    """Remove all items from a user's basket."""
    db = get_db()
    
    try:
        db.execute('DELETE FROM basket_items WHERE user_id = ?', (user_id,))
        db.commit()
        return {'success': True, 'message': 'Basket cleared'}
    except sqlite3.Error as e:
        return {'success': False, 'message': f"Database error: {e}"}

def get_basket_total(user_id):
    """Calculate the total cost of all items in the basket."""
    db = get_db()
    
    total = db.execute(
        '''
        SELECT SUM(i.price * b.quantity) as total
        FROM basket_items b
        JOIN items i ON b.item_id = i.id
        WHERE b.user_id = ?
        ''',
        (user_id,)
    ).fetchone()
    
    return total['total'] if total['total'] else 0.0
