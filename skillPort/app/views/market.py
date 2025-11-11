# 文件: skillPort/app/views/market.py

from flask import Blueprint, render_template, request, session, abort, redirect, url_for
from app.db import fetch_query, execute_query
import datetime
import uuid

market_bp = Blueprint('market', __name__, url_prefix='/market')

# ... market_top() 和 product_detail() 函数保持不变 ...
@market_bp.route('/', methods=["GET"])
def market_top():
    keyword = request.args.get('keyword')
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

    if keyword:
        sql_products += " AND l.product_name LIKE %s"
        params.append(f"%{keyword}%")

    if categories_filter:
        placeholders = ','.join(['%s'] * len(categories_filter))
        sql_products += f" AND l.product_category IN ({placeholders})"
        params.extend(categories_filter)

    if sale_status:
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
        condition_map = {'new': '新品', 'used': '中古'}
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

    all_products = fetch_query(sql_products, tuple(params))
    
    sql_categories = "SELECT DISTINCT product_category AS id, product_category AS name FROM listing_tbl WHERE product_category IS NOT NULL AND product_category != '' ORDER BY product_category;"
    all_categories = fetch_query(sql_categories)
    
    return render_template('market/market.html', all_products=all_products, all_categories=all_categories)

@market_bp.route('/product/<product_id>', methods=["GET"])
def product_detail(product_id):
    sql_product = "SELECT l.*, i.image_path, u.user_name AS seller_name, u.profile_icon AS seller_icon, u.user_tags AS seller_tags FROM listing_tbl l LEFT JOIN listing_images_tbl i ON l.product_id = i.product_id AND i.is_thumbnail = 1 LEFT JOIN user_tbl u ON l.product_upload_user = u.user_name WHERE l.product_id = %s"
    product_info = fetch_query(sql_product, (product_id,), fetch_one=True)
    if not product_info: abort(404)
    sql_images = "SELECT image_path FROM listing_images_tbl WHERE product_id = %s AND is_thumbnail = 0 ORDER BY uploaded_at"
    other_images = fetch_query(sql_images, (product_id,))
    thumbnail_sql = "SELECT image_path FROM listing_images_tbl WHERE product_id = %s AND is_thumbnail = 1"
    thumbnail_img = fetch_query(thumbnail_sql, (product_id,), fetch_one=True)
    thumbnail_img = thumbnail_img['image_path']
    uploader_sql = "SELECT u.id FROM user_tbl u INNER JOIN listing_tbl l ON u.user_name = l.product_upload_user WHERE l.product_id = %s;"
    uploader_id = fetch_query(uploader_sql, (product_id,), fetch_one=True)
    uploader_id = uploader_id['id']
    return render_template('market/product_detail.html', info=product_info, other_images=other_images, thumbnail_img=thumbnail_img, uploader_id=uploader_id)


# --- [修改] 新建和编辑的路由分离 ---

@market_bp.route('/create', methods=["GET"])
def create_product_page():
    """ (GET) 渲染新建商品页面 """
    if 'user_id' not in session:
        return redirect(url_for('auth.login')) 
    # [修改] 指向 product_create.html
    return render_template('market/product_create.html')

@market_bp.route('/product/<product_id>/edit', methods=["GET"])
def edit_product_page(product_id):
    """ (GET) 渲染编辑商品页面 """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user_name = session.get('user_name')
    
    sql_product = "SELECT * FROM listing_tbl WHERE product_id = %s AND product_upload_user = %s"
    product_data = fetch_query(sql_product, (product_id, user_name), fetch_one=True)
    
    if not product_data:
        abort(404) 

    # [修改] 指向 product_detail_edit.html 并传入数据
    return render_template('market/product_detail_edit.html', product=product_data)


# --- [修改] 新建和更新的表单处理函数分离 ---

@market_bp.route('/create_action', methods=["POST"])
def create_product_action():
    """ (POST) 处理来自 product_create.html 的新建请求 """
    if 'user_id' not in session: abort(403)
    user_name = session.get('user_name')

    try:
        product_name = request.form.get('product_name')
        price = int(request.form.get('price'))
        description = request.form.get('description')
        category = request.form.get('product_category') 
        condition = request.form.get('condition')
        shipping_area = request.form.get('shipping_from')
        if not all([product_name, price, description, category, condition, shipping_area]):
            return "必须项目不能为空。", 400
    except (ValueError, TypeError) as e:
        return "表单数据的格式不正确。", 400

    try:
        sql_last_id = "SELECT product_id FROM listing_tbl WHERE product_id LIKE 'LSG-%' ORDER BY CAST(SUBSTRING(product_id, 5) AS UNSIGNED) DESC LIMIT 1"
        last_product = fetch_query(sql_last_id, fetch_one=True)
        new_id_num = 1
        if last_product and last_product['product_id']:
            try:
                last_num = int(last_product['product_id'].replace('LSG-', ''))
                new_id_num = last_num + 1
            except (ValueError, IndexError):
                new_id_num = 1
        product_id = f"LSG-{new_id_num:03d}"
        
        sql_insert = "INSERT INTO listing_tbl (product_id, product_name, product_price, shipping_area, product_category, product_condition, product_description, listing_status, listing_date, sales_status, update_date, product_upload_user) VALUES (%s, %s, %s, %s, %s, %s, %s, 1, %s, 'S', %s, %s)"
        current_time = datetime.datetime.now()
        params = (product_id, product_name, price, shipping_area, category, condition, description, current_time, current_time, user_name)
        if not execute_query(sql_insert, params): raise Exception("数据库插入失败")
    except Exception as e:
        print(f"数据库注册错误: {e}")
        return "服务器错误，商品登陆失败。", 500

    return redirect(url_for('market.manage_products_page'))

@market_bp.route('/product/<product_id>/update', methods=["POST"])
def update_product_action(product_id):
    """ (POST) 处理来自 product_detail_edit.html 的更新请求 """
    if 'user_id' not in session: abort(403)
    user_name = session.get('user_name')
    
    product = fetch_query("SELECT product_id FROM listing_tbl WHERE product_id = %s AND product_upload_user = %s", (product_id, user_name), fetch_one=True)
    if not product: abort(403)

    try:
        product_name = request.form.get('product_name')
        price = int(request.form.get('price'))
        description = request.form.get('description')
        category = request.form.get('product_category') 
        condition = request.form.get('condition')
        shipping_area = request.form.get('shipping_from')
        if not all([product_name, price, description, category, condition, shipping_area]):
            return "必须项目不能为空。", 400
    except (ValueError, TypeError) as e:
        return "表单数据的格式不正确。", 400

    try:
        sql_update = "UPDATE listing_tbl SET product_name = %s, product_price = %s, product_description = %s, product_category = %s, product_condition = %s, shipping_area = %s, update_date = %s WHERE product_id = %s AND product_upload_user = %s"
        params = (product_name, price, description, category, condition, shipping_area, datetime.datetime.now(), product_id, user_name)
        if not execute_query(sql_update, params): raise Exception("数据库更新失败")
    except Exception as e:
        print(f"数据库更新错误: {e}")
        return "服务器错误，商品更新失败。", 500
    
    return redirect(url_for('market.manage_products_page'))


# --- 删除和管理页面的函数保持不变 ---

@market_bp.route('/product/<product_id>/delete', methods=["GET"])
def delete_product(product_id):
    if 'user_id' not in session: abort(403)
    user_name = session.get('user_name')
    
    product = fetch_query("SELECT product_id FROM listing_tbl WHERE product_id = %s AND product_upload_user = %s", (product_id, user_name), fetch_one=True)
    if not product: abort(403)

    try:
        execute_query("DELETE FROM listing_images_tbl WHERE product_id = %s", (product_id,))
        execute_query("DELETE FROM listing_tbl WHERE product_id = %s", (product_id,))
    except Exception as e:
        print(f"数据库删除错误: {e}")
        return "服务器错误，商品删除失败。", 500

    return redirect(url_for('market.manage_products_page'))

@market_bp.route('/manage', methods=["GET"])
def manage_products_page():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    user_name = session.get('user_name')
    if not user_name: return redirect(url_for('auth.login'))

    sql = "SELECT l.product_id, l.product_name, l.sales_status, i.image_path FROM listing_tbl l LEFT JOIN listing_images_tbl i ON l.product_id = i.product_id AND i.is_thumbnail = 1 WHERE l.product_upload_user = %s ORDER BY l.listing_date DESC"
    my_products = fetch_query(sql, (user_name,))
    
    return render_template('market/product_management.html', my_products=my_products)

@market_bp.route('/product/<product_id>/checkout', methods=["GET"])
def checkout_page(product_id):
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    return render_template('order/checkout.html')
