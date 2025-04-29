from flask import Blueprint, render_template, request, redirect, url_for, g, flash, jsonify, session
from app.services.item_service import get_all_items, get_item_by_id, search_items
from app.services.basket_service import (
    get_basket_items, add_to_basket, remove_from_basket, 
    update_basket_quantity, get_basket_total
)
from app.services.auth_decorator import login_required

shop_bp = Blueprint('shop', __name__, url_prefix='/shop')

@shop_bp.route('/items')
@login_required
def items():
    """Display all items in the shop. Requires authentication."""
    items = get_all_items()
    return render_template('shop/items.html', items=items)

@shop_bp.route('/items/<int:item_id>')
@login_required
def item_detail(item_id):
    """Display details for a specific item. Requires authentication."""
    item = get_item_by_id(item_id)
    if item is None:
        flash('Item not found.')
        return redirect(url_for('shop.items'))
    
    return render_template('shop/item_detail.html', item=item)

@shop_bp.route('/search')
@login_required
def search():
    """Search for items by name. Requires authentication."""
    query = request.args.get('query', '')
    if query:
        items = search_items(query)
    else:
        items = get_all_items()
    
    return render_template('shop/items.html', items=items, query=query)

@shop_bp.route('/basket')
@login_required
def basket():
    """Display the user's basket."""
    basket_items = get_basket_items(g.user['id'])
    total = get_basket_total(g.user['id'])
    
    return render_template('shop/basket.html', basket_items=basket_items, total=total)

@shop_bp.route('/basket/add/<int:item_id>', methods=['POST'])
@login_required
def add_item_to_basket(item_id):
    """Add an item to the user's basket."""
    quantity = int(request.form.get('quantity', 1))
    
    result = add_to_basket(g.user['id'], item_id, quantity)
    
    if not result['success']:
        flash(result['message'])
    else:
        flash('Item added to basket!')
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify(result)
    
    # Redirect back to the referring page or item list
    return redirect(request.referrer or url_for('shop.items'))

@shop_bp.route('/basket/update/<int:basket_item_id>', methods=['POST'])
@login_required
def update_item_quantity(basket_item_id):
    """Update the quantity of an item in the basket."""
    quantity = int(request.form.get('quantity', 1))
    
    result = update_basket_quantity(basket_item_id, quantity)
    
    if not result['success']:
        flash(result['message'])
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify(result)
    
    return redirect(url_for('shop.basket'))

@shop_bp.route('/basket/remove/<int:basket_item_id>', methods=['POST'])
@login_required
def remove_item_from_basket(basket_item_id):
    """Remove an item from the basket."""
    result = remove_from_basket(basket_item_id)
    
    if not result['success']:
        flash(result['message'])
    else:
        flash('Item removed from basket.')
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify(result)
    
    return redirect(url_for('shop.basket'))

# API routes
@shop_bp.route('/api/items')
@login_required
def api_items():
    """API endpoint to get all items. Requires authentication."""
    items = get_all_items()
    return jsonify({'items': items})

@shop_bp.route('/api/items/<int:item_id>')
@login_required
def api_item_detail(item_id):
    """API endpoint to get a specific item. Requires authentication."""
    item = get_item_by_id(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    
    return jsonify({'item': item})

@shop_bp.route('/api/search')
@login_required
def api_search():
    """API endpoint to search for items. Requires authentication."""
    query = request.args.get('query', '')
    if query:
        items = search_items(query)
    else:
        items = get_all_items()
    
    return jsonify({'items': items, 'query': query})

@shop_bp.route('/api/basket', methods=['GET'])
@login_required
def api_basket():
    """API endpoint to get the user's basket."""
    basket_items = get_basket_items(g.user['id'])
    total = get_basket_total(g.user['id'])
    
    return jsonify({
        'basket_items': basket_items,
        'total': total
    })
