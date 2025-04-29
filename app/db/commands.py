import click
from flask.cli import with_appcontext
from app.db import init_db
from app.services.item_service import generate_sample_items

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('generate-data')
@with_appcontext
def generate_data_command():
    """Generate sample data for testing and demonstration."""
    result = generate_sample_items()
    click.echo(result['message'])
