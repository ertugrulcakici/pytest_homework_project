import sqlite3
import os
from flask import g, current_app

def get_db():
    """Connect to the application's configured database."""
    if 'db' not in g:
        db_path = os.path.join(current_app.root_path, '..', 'data', 'shop.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """Close the database connection."""
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """Initialize the database with schema."""
    db = get_db()
    
    with current_app.open_resource('db/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)
