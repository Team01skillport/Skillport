from flask import Blueprint, render_template, request, make_response, session
from app.db import fetch_query

market_bp = Blueprint('market', __name__, url_prefix='/market')

@market_bp.route('/', methods=["GET"])
def market_top():
    sql = "SELECT * FROM listing_tbl;"
    all_products = fetch_query(sql)
    return render_template('market/market.html', all_products=all_products)

@market_bp.route('/create', methods=["GET"])
def create_product_page():
    return render_template('market/product_create.html')

@market_bp.route('/product/<product_id>', methods=["GET"])
def product_detail(product_id):
    sql = "SELECT * FROM listing_tbl WHERE product_id ='"+product_id+"';"
    info = fetch_query(sql, True)
    return render_template('market/product_detail.html', info=info)

@market_bp.route('/product/<int:product_id>/edit', methods=["GET"])
def edit_product_page(product_id):
    return render_template('market/product_detail_edit.html')

@market_bp.route('/manage', methods=["GET"])
def manage_products_page():
    return render_template('market/product_management.html')

@market_bp.route('/product/<int:product_id>/checkout', methods=["GET"])
def checkout_page(product_id):
    return render_template('order/checkout.html')