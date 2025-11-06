from flask import Blueprint, render_template, request, session, abort
from app.db import fetch_query

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.route('/checkout', methods=["GET"])
def product_checkout():
    return render_template('order/checkout.html')