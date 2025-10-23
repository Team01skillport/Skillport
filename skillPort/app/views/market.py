from flask import Blueprint, render_template

market_bp = Blueprint('market', __name__, url_prefix='/market')

# 1. 市场主页 market.market_top
@market_bp.route('/', methods=["GET"])
def market_top():
    return render_template('market/market.html')

# 2.
@market_bp.route('/create', methods=["GET"])
def create_product_page():
    # 渲染 'templates/market/product_create.html'
    return render_template('market/product_create.html')

# 3.(product_detail)
@market_bp.route('/product/<int:product_id>', methods=["GET"])
def product_detail(product_id):
    return render_template('market/product_detail.html')

# 4.(product_detail_edit)
@market_bp.route('/product/<int:product_id>/edit', methods=["GET"])
def edit_product_page(product_id):
    return render_template('market/product_detail_edit.html')

# 5.(product_management)
@market_bp.route('/manage', methods=["GET"])
def manage_products_page():
    return render_template('market/product_management.html')

# 商品購入手続きページ
# /market/product/1/checkout
@market_bp.route('/product/<int:product_id>/checkout', methods=["GET"])
def checkout_page(product_id):
    return render_template('order/checkout.html')