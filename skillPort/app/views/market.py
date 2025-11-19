from flask import Blueprint, render_template, request, session, abort, redirect, url_for, jsonify, current_app,flash
from app.db import fetch_query, execute_query, create_user
import datetime
import uuid
import os
import math 
from werkzeug.utils import secure_filename

market_bp = Blueprint('market', __name__, url_prefix='/market')

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
            l.sales_status,
            l.product_upload_user AS seller_name,
            i.image_path
        FROM 
            listing_tbl l
        LEFT JOIN 
            listing_images_tbl i ON l.product_id = i.product_id AND i.is_thumbnail = 1
        WHERE 1=1 AND sales_status = 'S'
    """
    params = []

    # --- 検索/フィルタリング条件の構築 ---
    if keyword:
        sql_products += " AND l.product_name LIKE %s"
        params.append(f"%{keyword}%\n")
    # ... (その他のフィルタリング条件の構築ロジックが続く) ...
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
    # ------------------------------------

    all_products = fetch_query(sql_products, tuple(params))
    if all_products is None:
        all_products = [] 
    
    sql_categories = "SELECT DISTINCT product_category AS id, product_category AS name FROM listing_tbl WHERE product_category IS NOT NULL AND product_category != '' ORDER BY product_category;"
    all_categories = fetch_query(sql_categories)
    if all_categories is None:
        all_categories = [] 
        
    return render_template('market/market.html', all_products=all_products, all_categories=all_categories)

# =========================================================================
# Route 18: ヘッダー検索実行 (GET)
# =========================================================================
@market_bp.route('/header_search', methods=["GET"])
def header_search():
    query = request.args.get('headersearch')
    results, search_query = perform_search(query)
    
    return render_template('search/search_results.html', 
                            search_results=results, 
                            search_query=search_query)

# Route 19: マーケット内検索実行 (GET)
@market_bp.route('/market_search', methods=["GET"])
def market_search():
    query = request.args.get('keyword') # [已修正] 匹配 market.html
    results, search_query = perform_search(query)
    
    return render_template('search/search_results.html', 
                            search_results=results, 
                            search_query=search_query)

# 検索の共通ロジック
def perform_search(query):
    if not query:
        return [], ""

    search_term = f"%{query}%"
    sql = """
        SELECT 
            l.*, 
            l.product_upload_user AS seller_name,
            i.image_path
        FROM 
            listing_tbl l
        LEFT JOIN 
            listing_images_tbl i ON l.product_id = i.product_id AND i.is_thumbnail = 1
        WHERE 
            l.product_name LIKE %s
        ORDER BY
            l.listing_date DESC
    """
    results = fetch_query(sql, (search_term,))
    if results is None:
        results = []
        
    return results, query


# =========================================================================
# 【III. 商品 CRUD / 管理関連 (Route 2, 3, 4, 5, 6, 7, 8, 14)】
# =========================================================================
# =========================================================================
# Route 2: 商品详情页面 (GET) - 商品の詳細表示とコメント取得
# =========================================================================
@market_bp.route('/product/<product_id>', methods=["GET"])
def product_detail(product_id):
    
    # ⭐ 修复点：在 SQL 中获取 u.id 并命名为 seller_id
    sql_product = "SELECT l.*, i.image_path, u.id AS seller_id, u.user_name AS seller_name, u.profile_icon AS seller_icon, u.user_tags AS seller_tags FROM listing_tbl l LEFT JOIN listing_images_tbl i ON l.product_id = i.product_id AND i.is_thumbnail = 1 LEFT JOIN user_tbl u ON l.product_upload_user = u.user_name WHERE l.product_id = %s"
    product_info = fetch_query(sql_product, (product_id,), fetch_one=True)
    if not product_info: abort(404)

    # ⭐ 修复点：直接从 product_info 获取 seller_id
    seller_id = product_info.get('seller_id')
    
    # --- 省略 uploader_sql 查询和 uploader_id 变量（因为 seller_id 已经获取，uploader_id 冗余） ---
    
    sql_images = "SELECT image_path FROM listing_images_tbl WHERE product_id = %s AND is_thumbnail = 0 ORDER BY uploaded_at"
    other_images = fetch_query(sql_images, (product_id,))
    if other_images is None: other_images = []
        
    thumbnail_sql = "SELECT image_path FROM listing_images_tbl WHERE product_id = %s AND is_thumbnail = 1"
    thumbnail_img = fetch_query(thumbnail_sql, (product_id,), fetch_one=True)
    thumbnail_img = thumbnail_img['image_path'] if thumbnail_img else None
    
    # 移除冗余的 uploader_sql 部分，但为了兼容性，可以保留 uploader_id 变量并赋值
    # uploader_id = seller_id 

    # [新增：获取此商品的评论]
    sql_comments = """
        SELECT 
            c.comment_text, c.comment_date,
            u.user_name, u.profile_icon
        FROM 
            product_comment_tbl c
        JOIN 
            user_tbl u ON c.user_id = u.id
        WHERE 
            c.product_id = %s AND c.parent_comment_id IS NULL
        ORDER BY 
            c.comment_date DESC
    """
    comments = fetch_query(sql_comments, (product_id,))
    if comments is None: comments = []
    
    # ⭐ 获取卖家的平均评价和总数
    seller_rating_info = {'average_rating': None, 'rating_count': 0}
    if seller_id: # 此时 seller_id 保证有效
        sql_rating_stats = """
            SELECT 
                ROUND(AVG(rating), 1) AS average_rating, 
                COUNT(id) AS rating_count
            FROM 
                seller_ratings_tbl
            WHERE 
                seller_id = %s
        """
        stats = fetch_query(sql_rating_stats, (seller_id,), fetch_one=True)
        if stats and stats['rating_count'] > 0:
            seller_rating_info['average_rating'] = stats['average_rating']
            seller_rating_info['rating_count'] = stats['rating_count']
            
    # uploader_id 变量若仍被模板依赖，则需要赋值。否则可移除。
    uploader_id = seller_id # 确保 uploader_id 变量也可用
    
    return render_template(
        'market/product_detail.html', 
        info=product_info, 
        other_images=other_images, 
        thumbnail_img=thumbnail_img, 
        uploader_id=uploader_id,
        comments=comments,
        # !修正点
        seller_rating_info=seller_rating_info
    )

# =========================================================================
# Route 3: 商品新規作成ページ (GET)
# =========================================================================
@market_bp.route('/create', methods=["GET"])
def create_product_page():
    if 'user_id' not in session: return redirect(url_for('auth.login')) 
    return render_template('market/product_create.html')

# =========================================================================
# Route 4: 商品編集ページ (GET)
# =========================================================================
@market_bp.route('/product/<product_id>/edit', methods=["GET"])
def edit_product_page(product_id):
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    user_name = session.get('user_name')
    
    sql_product = "SELECT * FROM listing_tbl WHERE product_id = %s AND product_upload_user = %s"
    product_data = fetch_query(sql_product, (product_id, user_name), fetch_one=True)
    
    if not product_data: abort(404) 

    return render_template('market/product_detail_edit.html', product=product_data)

# =========================================================================
# Route 5: 商品新規作成アクション (POST)
# =========================================================================
@market_bp.route('/create_action', methods=["POST"])
def create_product_action():
    if 'user_id' not in session: abort(403)
    user_name = session.get('user_name')
    # ... (データのバリデーションとデータベース挿入ロジック) ...
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
        # ID生成ロジック
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
        
        # 商品情報挿入
        sql_insert = "INSERT INTO listing_tbl (product_id, product_name, product_price, shipping_area, product_category, product_condition, product_description, listing_status, listing_date, sales_status, update_date, product_upload_user) VALUES (%s, %s, %s, %s, %s, %s, %s, 1, %s, 'S', %s, %s)"
        current_time = datetime.datetime.now()
        params = (product_id, product_name, price, shipping_area, category, condition, description, current_time, current_time, user_name)
        if not execute_query(sql_insert, params): raise Exception("データベースの挿入に失敗しました")
        
        # 画像アップロードと登録
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

# =========================================================================
# Route 6: 商品更新アクション (POST)
# =========================================================================
@market_bp.route('/product/<product_id>/update', methods=["POST"])
def update_product_action(product_id):
    if 'user_id' not in session: abort(403)
    user_name = session.get('user_name')
    
    product = fetch_query("SELECT product_id FROM listing_tbl WHERE product_id = %s AND product_upload_user = %s", (product_id, user_name), fetch_one=True)
    if not product: abort(403)

    # ... (データのバリデーションとデータベース更新ロジック) ...
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
        # 商品情報更新
        sql_update = "UPDATE listing_tbl SET product_name = %s, product_price = %s, product_description = %s, product_category = %s, product_condition = %s, shipping_area = %s, update_date = %s WHERE product_id = %s AND product_upload_user = %s"
        params = (product_name, price, description, category, condition, shipping_area, datetime.datetime.now(), product_id, user_name)
        if not execute_query(sql_update, params): raise Exception("データベースの更新に失敗しました")
        
        # 画像処理
        files = request.files.getlist('images')
        if files and files[0].filename: 
            # 既存画像削除
            execute_query("DELETE FROM listing_images_tbl WHERE product_id = %s", (product_id,))
            
            # 新規画像アップロードと登録
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
        print(f"データベース更新エラー: {e}")
        return "サーバーエラー、商品更新に失敗しました。", 500
    
    return redirect(url_for('market.manage_products_page'))

# =========================================================================
# Route 7: 商品削除アクション (GET)
# =========================================================================
@market_bp.route('/product/<product_id>/delete', methods=["GET"])
def delete_product(product_id):
    if 'user_id' not in session: abort(403)
    user_name = session.get('user_name')
    
    product = fetch_query("SELECT product_id FROM listing_tbl WHERE product_id = %s AND product_upload_user = %s", (product_id, user_name), fetch_one=True)
    if not product: abort(403)

    try:
        # 関連する画像と商品情報を削除
        execute_query("DELETE FROM listing_images_tbl WHERE product_id = %s", (product_id,))
        execute_query("DELETE FROM listing_tbl WHERE product_id = %s", (product_id,))
    except Exception as e:
        print(f"データベース削除エラー: {e}")
        return "サーバーエラー、商品削除に失敗しました。", 500

    return redirect(url_for('market.manage_products_page'))

# =========================================================================
# Route 8: 出品商品管理ページ (GET)
# =========================================================================
@market_bp.route('/manage', methods=["GET"])
def manage_products_page():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    user_name = session.get('user_name')
    if not user_name: return redirect(url_for('auth.login'))

    sql = "SELECT l.product_price, l.product_id, l.product_name, l.sales_status, i.image_path FROM listing_tbl l LEFT JOIN listing_images_tbl i ON l.product_id = i.product_id AND i.is_thumbnail = 1 WHERE l.product_upload_user = %s ORDER BY l.listing_date DESC"
    my_products = fetch_query(sql, (user_name,))
    
    return render_template('market/product_management.html', my_products=my_products)

# =========================================================================
# Route 14: お気に入り登録アクション (POST)
# =========================================================================
@market_bp.route('add_favorite/<product_id>', methods=['POST'])
def video_like(product_id):
    print("FAV RUN")
    
    if 'user_id' in session:
        user_id = session['user_id']
        print("USER IN")
        try:
            sql_check = "SELECT * FROM liked_products_tbl WHERE user_id=%s AND product_id=%s"
            existing = fetch_query(sql_check, (user_id, product_id), fetch_one=True)
            print(existing)
            if existing:
                return jsonify({'success': False, 'error': 'すでにお気に入り登録済みです'})
            else:
                sql_insert = "INSERT INTO liked_products_tbl (user_id, product_id) VALUES (%s, %s)"
                add_like = execute_query(sql_insert, (user_id, product_id))
                if add_like:
                    return jsonify({'success': True, 'message': 'お気に入り登録完了'})
                else:
                    raise Exception("いいね登録失敗")
                
        except Exception as e:
            print(f"お気に入り登録エラー: {e}")
            return jsonify({'success': False, 'error': 'データベースエラー'}), 500
    else:
        return jsonify({'success': False, 'error': 'ログインしていません'}), 401
        
# =========================================================================
# Route 17: AJAX：商品コメント投稿 (POST)
# =========================================================================
@market_bp.route('/product/post_comment', methods=['POST'])
def post_product_comment():
    """
    [新機能] 
    商品の公開コメントを product_comment_tbl に保存する。
    """
    
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'コメントするには、ログインが必要です。'}), 401
    
    user_id = session['user_id']
    
    data = request.json
    product_id = data.get('product_id')
    comment_text = data.get('comment_text')

    if not product_id or not comment_text:
        return jsonify({'success': False, 'error': 'コメントが空です'}), 400

    try:
        sql_insert = """
            INSERT INTO product_comment_tbl 
            (product_id, user_id, comment_text) 
            VALUES (%s, %s, %s)
        """
        success = execute_query(sql_insert, (product_id, user_id, comment_text)) 
        
        if not success:
            raise Exception("データベースの挿入に失敗しました")
            
        sql_new_comment = """
            SELECT 
                c.comment_text, c.comment_date,
                u.user_name, u.profile_icon
            FROM 
                product_comment_tbl c
            JOIN 
                user_tbl u ON c.user_id = u.id
            WHERE 
                c.user_id = %s AND c.product_id = %s
            ORDER BY 
                c.comment_date DESC
            LIMIT 1
        """
        new_comment_data = fetch_query(sql_new_comment, (user_id, product_id), fetch_one=True)

        return jsonify({'success': True, 'comment': new_comment_data})

    except Exception as e:
        print(f"商品コメントの送信エラー: {e}")
        return jsonify({'success': False, 'error': 'サーバーエラーが発生しました'}), 500


# =========================================================================
# 【IV. 注文/購入/決済関連 (Route 9, 10, 11, 12, 13)】
# =========================================================================
# =========================================================================
# Route 9: 注文確認/チェックアウトページ (GET)
# =========================================================================
@market_bp.route('/product/<product_id>/checkout', methods=["GET"])
def checkout_page(product_id):
    if 'user_id' not in session: 
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    # 商品情報取得
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
        
    # ユーザー住所情報取得
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
    
    # 支払い方法情報取得
    sql_payment_methods = """
        SELECT card_num, bank_name, bank_account_num, account_type 
        FROM payment_tbl 
        WHERE user_id = %s
    """
    payment_methods = fetch_query(sql_payment_methods, (user_id,))
    
    return render_template('order/checkout.html', product=product_info, address=user_address, payment_methods=payment_methods)

# Route 10: 購入アクション (POST) - 注文と商品ステータス更新
@market_bp.route('/product/<product_id>/purchase', methods=["POST"])
def purchase_action(product_id):
    
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'ユーザーがログインしていません'}), 401
    
    purchaser_id = session['user_id']

    try:
        # 商品情報の確認
        product = fetch_query(
            "SELECT product_price, product_upload_user FROM listing_tbl WHERE product_id = %s AND sales_status = 'S'", 
            (product_id,), 
            fetch_one=True
        )
        
        if not product:
            return jsonify({'success': False, 'error': '商品が存在しないか、売り切れです'}), 404

        # 出品者IDの取得
        seller_name = product['product_upload_user']
        seller = fetch_query("SELECT id FROM user_tbl WHERE user_name = %s", (seller_name,), fetch_one=True)
        
        if not seller:
            return jsonify({'success': False, 'error': '出品者のアカウントが見つかりません'}), 500
        
        seller_id = seller['id']
        
        # 利益と手数料の計算
        price = product['product_price']
        commission = int(price * 0.10)
        profit = price - commission
        
        # 注文の作成
        sql_insert_order = """
            INSERT INTO market_order_tbl 
            (purchaser_id, seller_id, transaction_status, total_amount, sales_profit, shipping_cost, total_commission, shipping_status, transaction_startdate, transaction_completeddate)
            VALUES (%s, %s, '進行中', %s, %s, 0, %s, '発送待', %s, %s)
        """
        current_time = datetime.datetime.now()
        params_order = (purchaser_id, seller_id, price, profit, commission, current_time, current_time)
        
        if not execute_query(sql_insert_order, params_order):
            raise Exception("注文の作成に失敗しました")

        # 商品ステータスの更新（売り切れに）
        sql_update_listing = "UPDATE listing_tbl SET sales_status = 'C', update_date = %s WHERE product_id = %s"
        if not execute_query(sql_update_listing, (current_time, product_id)):
            raise Exception("商品ステータスの更新に失敗しました")
            
        return jsonify({'success': True, 'redirect_url': url_for('market.purchase_history_page')})

    except Exception as e:
        print(f"購入処理エラー: {e}")
        return jsonify({'success': False, 'error': 'サーバー内部エラー'}), 500

# =========================================================================
# Route 11: 購入履歴ページ (GET)
# =========================================================================
@market_bp.route('/manage/purchases', methods=["GET"])
def purchase_history_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    purchaser_id = session['user_id']
    
    sql_complex = """
        SELECT 
            o.id AS order_id, 
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

# =========================================================================
# Route 12: AJAX：支払い方法追加 (POST)
# =========================================================================
@market_bp.route('/checkout/add_payment', methods=["POST"])
def checkout_add_payment():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'ログインしていません'}), 401
    
    user_id = session['user_id']
    data = request.json
    payment_type = data.get('payment_type')
    
    try:
        # クレジットカードの追加ロジック
        if payment_type == 'credit':
            # ... (データ処理とDB挿入) ...
            card_num_raw = data.get('card_num')
            card_exp_raw = data.get('card_expiration')

            if not card_num_raw or not card_exp_raw:
                return jsonify({'success': False, 'error': 'カード番号と有効期限は必須です'}), 400
                
            card_num = card_num_raw.replace(' ', '')
            card_name = data.get('card_name')
            card_exp = card_exp_raw.replace('/', '') 

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

        # 銀行口座の追加ロジック
        elif payment_type == 'bank':
            # ... (データ処理とDB挿入) ...
            bank_name = data.get('bank_name')
            acc_type = data.get('account_type')
            acc_num = data.get('bank_account_num')
            acc_name = data.get('acc_holder_name')
            
            if not all([bank_name, acc_type, acc_num, acc_name]):
                return jsonify({'success': False, 'error': '銀行口座情報が不完全です'}), 400

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

# =========================================================================
# Route 13: AJAX：住所更新 (POST)
# =========================================================================
@market_bp.route('/checkout/update_address', methods=["POST"])
def update_address_action():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'ユーザーがログインしていません'}), 401
    
    user_id = session['user_id']
    data = request.json 
    
    zip_code = data.get('zip_code')
    prefecture = data.get('prefecture')
    address1 = data.get('address1')
    address2 = data.get('address2')
    
    if not all([zip_code, prefecture, address1]):
        return jsonify({'success': False, 'error': '必須の住所情報が不完全です'}), 400

    try:
        sql_update = """
            UPDATE user_tbl 
            SET zip_code = %s, prefecture = %s, address1 = %s, address2 = %s
            WHERE id = %s
        """
        params = (zip_code, prefecture, address1, address2, user_id)
        
        if execute_query(sql_update, params):
            updated_data = {
                'zip_code': zip_code,
                'prefecture': prefecture,
                'address1': address1,
                'address2': address2
            }
            return jsonify({'success': True, 'message': '住所が正常に更新されました', 'updated_data': updated_data})
        else:
            raise Exception("データベースの更新に失敗しました")

    except Exception as e:
        print(f"住所更新エラー: {e}")
        return jsonify({'success': False, 'error': '住所の更新中にエラーが発生しました'}), 500

# =========================================================================
# 【V. 取引メッセージ/取引完了関連 (Route 15, 16, 20, 21, 22)】
# =========================================================================
# =========================================================================
# Route 15: 取引详细页面 (GET) - 注文情報、出品者、商品、メッセージの表示
# =========================================================================
@market_bp.route('/transaction/<order_id>', methods=["GET"])
def transaction_detail(order_id):
    """
    取引詳細ページをレンダリングする。
    注文、商品、出品者、チャット履歴、そして評価済みであればその情報を取得する。
    """
    
    if 'user_id' not in session:
        flash("このページを表示するには、ログインが必要です。", "warning") 
        return redirect(url_for('auth.login', next=request.url))
    
    user_id = session['user_id']
    
    # 注文情報の取得
    sql_order = """
        SELECT * FROM market_order_tbl 
        WHERE id = %s AND (purchaser_id = %s OR seller_id = %s)
    """
    order_info = fetch_query(sql_order, (order_id, user_id, user_id), fetch_one=True)
    
    if not order_info:
        abort(404) 

    # 出品者情報の取得
    sql_seller = """
        SELECT user_name, profile_icon, user_tags
        FROM user_tbl 
        WHERE id = %s
    """
    seller_info = fetch_query(sql_seller, (order_info['seller_id'],), fetch_one=True)

    # 商品情報の取得 (暫定的に価格と出品者で紐付け)
    sql_product = """
        SELECT 
            l.product_id, l.product_name, l.product_price, l.shipping_area, 
            l.product_condition, l.listing_date, i.image_path
        FROM 
            listing_tbl l
        JOIN 
            user_tbl u ON l.product_upload_user = u.user_name
        LEFT JOIN
            listing_images_tbl i ON l.product_id = i.product_id AND i.is_thumbnail = 1
        WHERE 
            u.id = %s AND l.product_price = %s
        LIMIT 1
    """
    product_info = fetch_query(sql_product, 
                            (order_info['seller_id'], order_info['total_amount']), 
                            fetch_one=True)

    # メッセージ履歴の取得
    sql_messages = """
        SELECT * FROM order_message_tbl 
        WHERE transaction_id = %s
        ORDER BY order_message_date ASC
    """
    messages = fetch_query(sql_messages, (order_id,))
    if messages is None:
        messages = []
        
    # ⭐ 【追加予定】評価情報の取得 (次で追加)
    rated_info = None
    if order_info['transaction_status'] == '取引完了' and order_info['purchaser_id'] == user_id:
        sql_rating = """
            SELECT rating, comment
            FROM seller_ratings_tbl
            WHERE order_id = %s AND rater_user_id = %s 
            LIMIT 1
        """
        rated_info = fetch_query(sql_rating, (order_id, user_id), fetch_one=True)
        
    return render_template('order/transaction_detail.html',
                            order=order_info,
                            product=product_info,
                            seller=seller_info,
                            messages=messages,
                            rated_info=rated_info) # ⭐ rated_info をテンプレートに渡す

# =========================================================================
# Route 16: AJAX：取引メッセージ送信 (POST)
# =========================================================================
@market_bp.route('/transaction/post_message', methods=['POST'])
def post_message():
    """
    取引画面からのメッセージをデータベースに保存する。
    """
    
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'ログインしていません'}), 401
    
    user_id = session['user_id']
    
    data = request.json
    order_id = data.get('order_id')
    message_text = data.get('message_text')

    if not order_id or not message_text:
        return jsonify({'success': False, 'error': 'メッセージが空です'}), 400

    try:
        # 注文の存在と権限を確認
        sql_check = "SELECT 1 FROM market_order_tbl WHERE id = %s AND (purchaser_id = %s OR seller_id = %s)"
        order = fetch_query(sql_check, (order_id, user_id, user_id), fetch_one=True)
        
        if not order:
            return jsonify({'success': False, 'error': '権限がありません'}), 403

        # メッセージ挿入
        sql_insert = """
            INSERT INTO order_message_tbl 
            (transaction_id, order_message_user_id, order_message_text) 
            VALUES (%s, %s, %s)
        """
        success = execute_query(sql_insert, (order_id, user_id, message_text)) 
        
        if not success:
            raise Exception("データベースの挿入に失敗しました")

        return jsonify({
            'success': True, 
            'message': {
                'order_message_user_id': user_id,
                'order_message_text': message_text
            }
        })

    except Exception as e:
        print(f"メッセージの送信エラー: {e}")
        return jsonify({'success': False, 'error': 'サーバーエラーが発生しました'}), 500

# =========================================================================
# Route 20: 取引完了アクション (POST)
# =========================================================================
@market_bp.route('/transaction/<order_id>/complete', methods=['POST'])
def complete_transaction(order_id):
    """
    取引を完了し、注文ステータスを更新し、評価ページにリダイレクトする。
    """
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'ログインしていません'}), 401
    
    user_id = session['user_id']
    
    # 1. 注文の存在と購入者であることを確認
    sql_check = "SELECT * FROM market_order_tbl WHERE id = %s AND purchaser_id = %s AND transaction_status != '取引完了'"
    order = fetch_query(sql_check, (order_id, user_id), fetch_one=True)
    
    if not order:
        flash("注文が見つからないか、既に完了しています。", "danger")
        return redirect(url_for('market.transaction_detail', order_id=order_id))
        
    try:
        # 2. 注文ステータスを「取引完了」に更新
        sql_update = """
            UPDATE market_order_tbl 
            SET transaction_status = '取引完了', shipping_status = '完了', transaction_completeddate = %s
            WHERE id = %s AND purchaser_id = %s
        """
        current_time = datetime.datetime.now()
        success = execute_query(sql_update, (current_time, order_id, user_id))
        
        if not success:
            raise Exception("データベースの更新に失敗しました")

        # 3. 評価ページにリダイレクト
        return redirect(url_for('market.rate_seller_page', order_id=order_id))

    except Exception as e:
        print(f"取引完了エラー: {e}")
        flash("取引完了処理中にエラーが発生しました。", "danger")
        return redirect(url_for('market.transaction_detail', order_id=order_id))

# Route 21: 出品者評価ページ (GET)
@market_bp.route('/transaction/<order_id>/rate', methods=["GET"])
def rate_seller_page(order_id):
    """
    出品者評価ページをレンダリングする。
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login', next=request.url))
    
    user_id = session['user_id']
    
    # 注文が完了済みで、かつ購入者であることを確認
    sql_order = """
        SELECT o.id, u.user_name AS seller_name, o.seller_id
        FROM market_order_tbl o
        JOIN user_tbl u ON o.seller_id = u.id
        WHERE o.id = %s AND o.purchaser_id = %s AND o.transaction_status = '取引完了'
    """
    order_info = fetch_query(sql_order, (order_id, user_id), fetch_one=True)
    
    if not order_info:
        flash("評価ページにアクセスできません。注文が見つからないか、未完了です。", "danger")
        return redirect(url_for('market.purchase_history_page'))

    # 既に評価済みでないかを確認
    sql_check_rating = "SELECT 1 FROM seller_ratings_tbl WHERE order_id = %s"
    if fetch_query(sql_check_rating, (order_id,), fetch_one=True):
        flash("この取引は既に評価済みです。", "info")
        return redirect(url_for('market.transaction_detail', order_id=order_id))
        
    return render_template('order/rate_seller.html', order=order_info)

# =========================================================================
# Route 22: 出品者評価アクション (POST)
# =========================================================================
@market_bp.route('/transaction/<order_id>/rate_action', methods=['POST'])
def rate_seller_action(order_id):
    """
    評価フォームを受け取り、seller_ratings_tbl に保存する。
    """
    if 'user_id' not in session: abort(401)
    user_id = session['user_id']
    
    # 注文が完了済みで、かつ購入者であることを確認
    sql_order = "SELECT id, seller_id FROM market_order_tbl WHERE id = %s AND purchaser_id = %s AND transaction_status = '取引完了'"
    order = fetch_query(sql_order, (order_id, user_id), fetch_one=True)
    
    if not order:
        flash("評価できる取引ではありません。", "danger")
        return redirect(url_for('market.purchase_history_page'))
        
    # 既に評価済みでないかを確認
    sql_check_rating = "SELECT 1 FROM seller_ratings_tbl WHERE order_id = %s"
    if fetch_query(sql_check_rating, (order_id,), fetch_one=True):
        flash("既に評価済みです。", "info")
        return redirect(url_for('market.transaction_detail', order_id=order_id))
        
    try:
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        
        if not rating or not (1 <= int(rating) <= 5):
            flash("評価スター数が無効です。", "danger")
            return redirect(url_for('market.rate_seller_page', order_id=order_id))
            
        # 評価をデータベースに挿入
        sql_insert = """
            INSERT INTO seller_ratings_tbl 
            (order_id, seller_id, rater_user_id, rating, comment, rating_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (order_id, order['seller_id'], user_id, int(rating), comment, datetime.datetime.now())
        
        if not execute_query(sql_insert, params):
            raise Exception("データベースの挿入に失敗しました")
            
        flash("出品者を評価しました。取引完了です。", "success")
        # !評価した後購入管理画面へ戻る
        return redirect(url_for('market.purchase_history_page'))

    except Exception as e:
        print(f"評価送信エラー: {e}")
        flash("評価の送信中にサーバーエラーが発生しました。", "danger")
        return redirect(url_for('market.rate_seller_page', order_id=order_id))