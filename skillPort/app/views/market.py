# 文件: skillPort/app/views/market.py

from flask import Blueprint, render_template, request, session, abort
from app.db import fetch_query
import datetime # 日期处理需要导入

market_bp = Blueprint('market', __name__, url_prefix='/market')

# 文件: skillPort/app/views/market.py

@market_bp.route('/', methods=["GET"])
def market_top():
    
    categories_filter = request.args.getlist('category')
    sale_status = request.args.getlist('sale_status')
    conditions = request.args.getlist('condition')
    seller_name = request.args.get('seller_name')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    sql_products = """
        SELECT 
            l.*, 
            l.product_upload_user AS seller_name,
            i.image_path
        FROM 
            listing_tbl l
        LEFT JOIN 
            listing_images_tbl i ON l.product_id = i.product_id AND i.is_thumbnail = 1
        WHERE 1=1
    """
    params = []

    if categories_filter:
        placeholders = ','.join(['%s'] * len(categories_filter))
        sql_products += f" AND l.product_category IN ({placeholders})"
        params.extend(categories_filter)

    if sale_status:
        # 'on_sale' 对应 S, 'sold_out' 对应 C
        status_map = {'on_sale': 'S', 'sold_out': 'C'}
        mapped_status = [status_map.get(s) for s in sale_status if s in status_map]
        if mapped_status:
            placeholders = ','.join(['%s'] * len(mapped_status))
            sql_products += f" AND l.sales_status IN ({placeholders})"
            params.extend(mapped_status)

    if seller_name:
        sql_products += " AND l.product_upload_user LIKE %s"
        params.append(f"%{seller_name}%")

    if conditions:
        # HTMLの value ('new', 'used') を 
        # データベースの値 ('新品', '中古') にマッピングします
        condition_map = {
            'new': '新品',
            'used': '中古'
        }
        mapped_conditions = [condition_map.get(c) for c in conditions if c in condition_map]
        if mapped_conditions:
            placeholders = ','.join(['%s'] * len(mapped_conditions))
            sql_products += f" AND l.product_condition IN ({placeholders})"
            params.extend(mapped_conditions)

    if min_price:
        sql_products += " AND l.product_price >= %s"
        params.append(int(min_price))
        
    if max_price:
        sql_products += " AND l.product_price <= %s"
        params.append(int(max_price))

    all_products = fetch_query(sql_products)
    
    sql_categories = """
        SELECT DISTINCT 
            product_category AS id, 
            product_category AS name 
        FROM 
            listing_tbl 
        WHERE 
            product_category IS NOT NULL 
        ORDER BY 
            product_category;
    """
    all_categories = fetch_query(sql_categories)
    
    return render_template('market/market.html', 
                            all_products=all_products,
                            all_categories=all_categories)

@market_bp.route('/product/<product_id>', methods=["GET"])
def product_detail(product_id):
    """
    [已修改]
    - 'listing_tbl' (l) と 'user_tbl' (u) を JOIN します。
    - 'l.product_upload_user' (出品者名) と 'u.user_name' を紐付けます。
    - 出品者のアイコン (seller_icon) とタグ (seller_tags) を SELECT に追加します。
    """
    
    sql_product = """
        SELECT 
            l.*, 
            i.image_path,
            u.user_name AS seller_name,
            u.profile_icon AS seller_icon,
            u.user_tags AS seller_tags
        FROM 
            listing_tbl l
        LEFT JOIN 
            listing_images_tbl i ON l.product_id = i.product_id AND i.is_thumbnail = 1
        LEFT JOIN 
            user_tbl u ON l.product_upload_user = u.user_name
        WHERE l.product_id = %s
    """
    product_info = fetch_query(sql_product, (product_id,), fetch_one=True)
    
    if not product_info:
        abort(404) # 商品が見つからない場合

    sql_images = """
        SELECT image_path 
        FROM listing_images_tbl 
        WHERE product_id = %s AND is_thumbnail = 0
        ORDER BY uploaded_at
    """
    other_images = fetch_query(sql_images, (product_id,))

    # 3. データを product_detail.html テンプレートに渡す
    return render_template('market/product_detail.html', 
                            info=product_info,
                            other_images=other_images)

@market_bp.route('/create', methods=["GET"])
def create_product_page():
    return render_template('market/product_create.html')

@market_bp.route('/product/<product_id>/edit', methods=["GET"])
def edit_product_page(product_id):
    return render_template('market/product_detail_edit.html')

@market_bp.route('/manage', methods=["GET"])
def manage_products_page():
    return render_template('market/product_management.html')

@market_bp.route('/product/<product_id>/checkout', methods=["GET"])
def checkout_page(product_id):
    return render_template('order/checkout.html')