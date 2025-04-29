from flask import Blueprint, render_template, g, redirect, url_for, session
from app.services.auth_decorator import login_required
from app.services.item_service import get_all_items

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Redirect to home page if logged in, otherwise to login page."""
    if session.get('user_id'):
        return redirect(url_for('main.home'))
    else:
        return redirect(url_for('auth.login'))

@main_bp.route('/home')
@login_required
def home():
    """Display the home page with items. Requires authentication."""
    items = get_all_items()
    return render_template('main/home.html', items=items)

@main_bp.route('/profile')
@login_required
def profile():
    """Display the user's profile."""
    return render_template('main/profile.html', user=g.user)
