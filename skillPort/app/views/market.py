from flask import Blueprint, render_template, request, session, abort, redirect, url_for, jsonify, current_app
from app.db import fetch_query, execute_query
import datetime
import uuid
import os
from werkzeug.utils import secure_filename

market_bp = Blueprint('market', __name__, url_prefix='/market')

# ==========================================
# Route 1: 市场顶部/商品列表页面 (GET)
# ==========================================
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

# ==========================================
# Route 2: 商品详情页面 (GET)
# ==========================================
@market_bp.route('/product/<product_id>', methods=["GET"])
def product_detail(product_id):
    sql_product = "SELECT l.*, i.image_path, u.user_name AS seller_name, u.profile_icon AS seller_icon, u.user_tags AS seller_tags FROM listing_tbl l LEFT JOIN listing_images_tbl i ON l.product_id = i.product_id AND i.is_thumbnail = 1 LEFT JOIN user_tbl u ON l.product_upload_user = u.user_name WHERE l.product_id = %s"
    product_info = fetch_query(sql_product, (product_id,), fetch_one=True)
    if not product_info: abort(404)
    sql_images = "SELECT image_path FROM listing_images_tbl WHERE product_id = %s AND is_thumbnail = 0 ORDER BY uploaded_at"
    other_images = fetch_query(sql_images, (product_id,))
    thumbnail_sql = "SELECT image_path FROM listing_images_tbl WHERE product_id = %s AND i.is_thumbnail = 1"
    thumbnail_img = fetch_query(thumbnail_sql, (product_id,), fetch_one=True)
    #! 修改开始====
    thumbnail_img = thumbnail_img['image_path'] if thumbnail_img else None
    #! 修改结束====
    uploader_sql = "SELECT u.id FROM user_tbl u INNER JOIN listing_tbl l ON u.user_name = l.product_upload_user WHERE l.product_id = %s;"
    #! 修改开始====
    uploader_id_result = fetch_query(uploader_sql, (product_id,), fetch_one=True)
    if uploader_id_result:
        uploader_id = uploader_id_result['id']
    else:
        uploader_id = None
    #! 修改结束====
    print("uploader_id 検索結果：", uploader_id)
    return render_template('market/product_detail.html', info=product_info, other_images=other_images, thumbnail_img=thumbnail_img, uploader_id=uploader_id)

# ==========================================
# Route 3: 商品创建页面 (GET)
# ==========================================
@market_bp.route('/create', methods=["GET"])
def create_product_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login')) 
    return render_template('market/product_create.html')

# ==========================================
# Route 4: 商品编辑页面 (GET)
# ==========================================
@market_bp.route('/product/<product_id>/edit', methods=["GET"])
def edit_product_page(product_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user_name = session.get('user_name')
    
    sql_product = "SELECT * FROM listing_tbl WHERE product_id = %s AND product_upload_user = %s"
    product_data = fetch_query(sql_product, (product_id, user_name), fetch_one=True)
    
    if not product_data:
        abort(404) 

    return render_template('market/product_detail_edit.html', product=product_data)

# ==========================================
# Route 5: 执行商品创建动作 (POST)
# ==========================================
@market_bp.route('/create_action', methods=["POST"])
def create_product_action():
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
            return "必須項目が入力されていません。", 400
    except (ValueError, TypeError) as e:
        return "フォームデータの形式が正しくありません。", 400

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
        if not execute_query(sql_insert, params): 
            raise Exception("データベースの挿入に失敗しました")
        
        files = request.files.getlist('images')
        if files and files[0].filename:
            
            base_upload_path = os.path.join(current_app.static_folder, 'uploads', 'products')
            product_upload_folder = os.path.join(base_upload_path, product_id)
            os.makedirs(product_upload_folder, exist_ok=True)
            
            is_first_image = True
            
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    save_path = os.path.join(product_upload_folder, filename)
                    file.save(save_path)
                    
                    db_path = f"uploads/products/{product_id}/{filename}"
                    
                    sql_image_insert = "INSERT INTO listing_images_tbl (image_id, product_id, image_path, is_thumbnail) VALUES (%s, %s, %s, %s)"
                    image_id = f"IMG-{product_id}-{uuid.uuid4().hex[:6]}"
                    
                    execute_query(sql_image_insert, (image_id, product_id, db_path, 1 if is_first_image else 0))
                    
                    is_first_image = False

    except Exception as e:
        print(f"データベース登録エラー: {e}")
        return "サーバーエラー、商品登録に失敗しました。", 500

    return redirect(url_for('market.manage_products_page'))

# ==========================================
# Route 6: 执行商品更新动作 (POST)
# ==========================================
# market.py (Route 6: update_product_action)

@market_bp.route('/product/<product_id>/update', methods=["POST"])
def update_product_action(product_id):
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
            return "必須項目が入力されていません。", 400
    except (ValueError, TypeError) as e:
        return "フォームデータの形式が正しくありません。", 400

    try:
        # A. 更新商品基本信息
        sql_update = "UPDATE listing_tbl SET product_name = %s, product_price = %s, product_description = %s, product_category = %s, product_condition = %s, shipping_area = %s, update_date = %s WHERE product_id = %s AND product_upload_user = %s"
        params = (product_name, price, description, category, condition, shipping_area, datetime.datetime.now(), product_id, user_name)
        if not execute_query(sql_update, params): raise Exception("データベースの更新に失敗しました")
        
        # B. 检查是否有新图片上传
        files = request.files.getlist('images')
        if files and files[0].filename: # 至少有一个文件被选择
            
            # B1. 删除旧图片记录
            execute_query("DELETE FROM listing_images_tbl WHERE product_id = %s", (product_id,))
            
            # B2. 在文件系统中创建/准备目录
            base_upload_path = os.path.join(current_app.static_folder, 'uploads', 'products')
            product_upload_folder = os.path.join(base_upload_path, product_id)
            os.makedirs(product_upload_folder, exist_ok=True) # 确保目录存在
            
            is_first_image = True
            
            # B3. 保存新图片并插入新记录
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    save_path = os.path.join(product_upload_folder, filename)
                    # 注意：这里假设你可以覆盖或使用唯一文件名来避免冲突
                    file.save(save_path)
                    
                    db_path = f"uploads/products/{product_id}/{filename}"
                    
                    sql_image_insert = "INSERT INTO listing_images_tbl (image_id, product_id, image_path, is_thumbnail) VALUES (%s, %s, %s, %s)"
                    image_id = f"IMG-{product_id}-{uuid.uuid4().hex[:6]}"
                    
                    execute_query(sql_image_insert, (image_id, product_id, db_path, 1 if is_first_image else 0))
                    
                    is_first_image = False # 确保只有第一张是缩略图

    except Exception as e:
        print(f"データベース更新エラー: {e}")
        return "サーバーエラー、商品更新に失敗しました。", 500
    
    return redirect(url_for('market.manage_products_page'))

# ==========================================
# Route 7: 执行商品删除动作 (GET)
# ==========================================
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
        print(f"データベース削除エラー: {e}")
        return "サーバーエラー、商品削除に失敗しました。", 500

    return redirect(url_for('market.manage_products_page'))

# ==========================================
# Route 8: 我的商品管理页面 (GET)
# ==========================================
@market_bp.route('/manage', methods=["GET"])
def manage_products_page():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    user_name = session.get('user_name')
    if not user_name: return redirect(url_for('auth.login'))

    sql = "SELECT l.product_id, l.product_name, l.sales_status, i.image_path FROM listing_tbl l LEFT JOIN listing_images_tbl i ON l.product_id = i.product_id AND i.is_thumbnail = 1 WHERE l.product_upload_user = %s ORDER BY l.listing_date DESC"
    my_products = fetch_query(sql, (user_name,))
    
    return render_template('market/product_management.html', my_products=my_products)

# ==========================================
# Route 9: 结账页面 (GET)
# ==========================================
@market_bp.route('/product/<product_id>/checkout', methods=["GET"])
def checkout_page(product_id):
    if 'user_id' not in session: 
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    sql_product = """
        SELECT 
            l.product_id, l.product_name, l.product_price, l.product_upload_user,
            i.image_path
        FROM 
            listing_tbl l
        LEFT JOIN 
            listing_images_tbl i ON l.product_id = i.product_id AND i.is_thumbnail = 1
        WHERE 
            l.product_id = %s
    """
    product_info = fetch_query(sql_product, (product_id,), fetch_one=True)
    
    if not product_info:
        abort(404)
        
    sql_user_address = """
        SELECT 
            first_name, last_name, first_name_katakana, last_name_katakana, 
            zip_code, prefecture, address1, address2
        FROM 
            user_tbl 
        WHERE 
            id = %s
    """
    user_address = fetch_query(sql_user_address, (user_id,), fetch_one=True)
    
    # 获取支付方法列表
    sql_payment_methods = """
        SELECT card_num, bank_name, bank_account_num, account_type 
        FROM payment_tbl 
        WHERE user_id = %s
    """
    payment_methods = fetch_query(sql_payment_methods, (user_id,))
    
    return render_template('order/checkout.html', product=product_info, address=user_address, payment_methods=payment_methods)


# ==========================================
# Route 10: 执行购买动作 (POST)
# ==========================================
@market_bp.route('/product/<product_id>/purchase', methods=["POST"])
def purchase_action(product_id):
    
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'ユーザーがログインしていません'}), 401
    
    purchaser_id = session['user_id']

    try:
        product = fetch_query(
            "SELECT product_price, product_upload_user FROM listing_tbl WHERE product_id = %s AND sales_status = 'S'", 
            (product_id,), 
            fetch_one=True
        )
        
        if not product:
            return jsonify({'success': False, 'error': '商品が存在しないか、売り切れです'}), 404

        seller_name = product['product_upload_user']
        seller = fetch_query("SELECT id FROM user_tbl WHERE user_name = %s", (seller_name,), fetch_one=True)
        
        if not seller:
            return jsonify({'success': False, 'error': '出品者のアカウントが見つかりません'}), 500
        
        seller_id = seller['id']
        
        price = product['product_price']
        commission = int(price * 0.10)
        profit = price - commission
        
        sql_insert_order = """
            INSERT INTO market_order_tbl 
            (purchaser_id, seller_id, transaction_status, total_amount, sales_profit, shipping_cost, total_commission, shipping_status, transaction_startdate, transaction_completeddate)
            VALUES (%s, %s, '進行中', %s, %s, 0, %s, '発送待', %s, %s)
        """
        current_time = datetime.datetime.now()
        params_order = (purchaser_id, seller_id, price, profit, commission, current_time, current_time)
        
        if not execute_query(sql_insert_order, params_order):
            raise Exception("注文の作成に失敗しました")

        sql_update_listing = "UPDATE listing_tbl SET sales_status = 'C', update_date = %s WHERE product_id = %s"
        if not execute_query(sql_update_listing, (current_time, product_id)):
            raise Exception("商品ステータスの更新に失敗しました")
            
        return jsonify({'success': True, 'redirect_url': url_for('market.purchase_history_page')})

    except Exception as e:
        print(f"購入処理エラー: {e}")
        return jsonify({'success': False, 'error': 'サーバー内部エラー'}), 500

# ==========================================
# Route 11: 购买历史页面 (GET)
# ==========================================
@market_bp.route('/manage/purchases', methods=["GET"])
def purchase_history_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    purchaser_id = session['user_id']
    
    sql_complex = """
        SELECT 
            o.transaction_startdate, 
            o.total_amount, 
            o.shipping_status,
            l.product_id,
            l.product_name,
            i.image_path
        FROM 
            market_order_tbl o
        JOIN 
            user_tbl u ON o.seller_id = u.id
        JOIN 
            listing_tbl l ON u.user_name = l.product_upload_user AND o.total_amount = l.product_price
        LEFT JOIN
            listing_images_tbl i ON l.product_id = i.product_id AND i.is_thumbnail = 1
        WHERE 
            o.purchaser_id = %s
        ORDER BY 
            o.transaction_startdate DESC
    """
    my_orders = fetch_query(sql_complex, (purchaser_id,))
    
    return render_template('market/purchase_management.html', my_orders=my_orders)


# ==========================================
# Route 12: AJAX：添加支付方式 (POST)
# ==========================================
@market_bp.route('/checkout/add_payment', methods=["POST"])
def checkout_add_payment():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'ログインしていません'}), 401
    
    user_id = session['user_id']
    data = request.json
    payment_type = data.get('payment_type')
    
    try:
        if payment_type == 'credit':
            # 1. 取得数据并清除卡号和有效期中的所有空格/斜杠
            card_num_raw = data.get('card_num')
            card_exp_raw = data.get('card_expiration')

            if not card_num_raw or not card_exp_raw:
                return jsonify({'success': False, 'error': 'カード番号と有効期限は必須です'}), 400
                
            card_num = card_num_raw.replace(' ', '')
            card_name = data.get('card_name')
            
            # 【关键修复】：移除有效期中的斜杠，确保只有 MMYY (4个字符)
            card_exp = card_exp_raw.replace('/', '') 

            # 2. 检查清理后的数据
            if len(card_num) < 14 or len(card_num) > 16 or len(card_exp) != 4:
                return jsonify({'success': False, 'error': 'カード情報の形式が正しくありません (14-16桁/MMYY)'}), 400

            sql_check = "SELECT 1 FROM payment_tbl WHERE user_id = %s AND card_num = %s"
            if fetch_query(sql_check, (user_id, card_num), fetch_one=True):
                return jsonify({'success': False, 'error': 'このカードは既に登録されています'}), 400

            sql_insert = "INSERT INTO payment_tbl (user_id, card_num, card_name, card_expiration, card_block, account_type) VALUES (%s, %s, %s, %s, 0, 'クレジット')"
            params = (user_id, card_num, card_name, card_exp)
            
            if not execute_query(sql_insert, params):
                raise Exception("クレジットカードの登録に失敗しました")
            
            return jsonify({
                'success': True,
                'new_payment': {
                    'value': card_num,
                    'text': f'クレジットカード (**** {card_num[-4:]})'
                }
            })

        elif payment_type == 'bank':
            # (银行部分)
            bank_name = data.get('bank_name')
            acc_type = data.get('account_type')
            acc_num = data.get('bank_account_num')
            acc_name = data.get('acc_holder_name')
            
            if not all([bank_name, acc_type, acc_num, acc_name]):
                return jsonify({'success': False, 'error': '銀行口座情報が不完全です'}), 400

            # 银行账户不使用 card_num 字段作为主键，而是使用占位符
            card_num_for_bank = acc_num 
            
            sql_check = "SELECT 1 FROM payment_tbl WHERE user_id = %s AND bank_account_num = %s"
            if fetch_query(sql_check, (user_id, acc_num), fetch_one=True):
                return jsonify({'success': False, 'error': 'この銀行口座は既に登録されています'}), 400

            sql_insert = "INSERT INTO payment_tbl (user_id, card_num, bank_name, bank_account_num, acc_holder_name, account_type) VALUES (%s, %s, %s, %s, %s, %s)"
            params = (user_id, card_num_for_bank, bank_name, acc_num, acc_name, acc_type)
            
            if not execute_query(sql_insert, params):
                raise Exception("銀行口座の登録に失敗しました")

            return jsonify({
                'success': True,
                'new_payment': {
                    'value': acc_num,
                    'text': f'{bank_name} ({acc_type})'
                }
            })
        
        else:
            return jsonify({'success': False, 'error': '不明な支払いタイプです'}), 400

    except Exception as e:
        print(f"支払い方法の追加エラー: {e}")
        if "Duplicate entry" in str(e):
            return jsonify({'success': False, 'error': 'この支払い方法は既に登録されています'}), 409
        return jsonify({'success': False, 'error': 'サーバーエラーが発生しました'}), 500