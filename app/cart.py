from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import CartItem, Product
from app import db

cart = Blueprint('cart', __name__)

@cart.route('/cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@cart.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product.id)
        db.session.add(cart_item)

    db.session.commit()
    flash('Product added to cart!')
    return redirect(url_for('views.catalog'))

@cart.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        return redirect(url_for('views.index'))

    db.session.delete(cart_item)
    db.session.commit()
    flash('Product removed from cart!')
    return redirect(url_for('cart.view_cart'))