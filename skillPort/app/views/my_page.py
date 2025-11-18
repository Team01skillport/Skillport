from flask import Blueprint, render_template, request, make_response, session, redirect, url_for, jsonify
from app.db import fetch_query, create_user

my_page_bp = Blueprint('my_page', __name__, url_prefix='/my_page')

@my_page_bp.route('/top', methods=["GET"])
def my_page_top():
    return render_template('my_page/mp_menu.html')

@my_page_bp.route('/view_history', methods=["GET"])
def my_page_history():
    user_id = session['user_id']
    view_sql = "SELECT v.id, v.video_title, v.video_upload_date, v.video_description_section, v.thumbnail_path FROM video_tbl v LEFT JOIN video_view_tbl vv ON v.id = vv.video_id LEFT JOIN user_tbl u ON vv.user_id = u.id WHERE u.id = %s;"
    viewed_videos = fetch_query(view_sql, (user_id,), fetch_one=False)
    return render_template('my_page/mp_view_history.html', viewed_videos=viewed_videos)

# @my_page_bp.route('/bank_account_register', methods=["GET"])
# def bank_account_register():
#     return render_template('my_page/mp_bank_account_register.html')

@my_page_bp.route('/likes_list', methods=["GET"])
def likes_list():
    user_id = session['user_id']
    like_sql = "SELECT v.id, v.video_title, v.video_upload_date, v.video_description_section, v.thumbnail_path FROM video_tbl v LEFT JOIN video_like_tbl vl ON v.id = vl.video_id LEFT JOIN user_tbl u ON vl.user_id = u.id WHERE u.id = %s ORDER BY vl.video_like_date DESC;"
    liked_videos = fetch_query(like_sql, (user_id,), fetch_one=False)
    return render_template('my_page/mp_likes.html', liked_videos=liked_videos)

# @my_page_bp.route('/sales_list', methods=["GET"])
# def sales_list():
#     return render_template('my_page/mp_sales.html')

# @my_page_bp.route('/membership_list', methods=["GET"])
# def membership_List():
#     return render_template('my_page/mp_membership.html')

@my_page_bp.route('/favorites_list', methods=["GET"])
def favorites_list():
    user_id = session['user_id']
    print(user_id)
    fav_sql = "SELECT l.*, li.image_path FROM listing_tbl l LEFT JOIN liked_products_tbl lp ON l.product_id = lp.product_id LEFT JOIN listing_images_tbl li ON l.product_id = li.product_id LEFT JOIN user_tbl u ON lp.user_id = u.id WHERE u.id = %s;"
    fav_data = fetch_query(fav_sql, (user_id,), False)
    return render_template('my_page/mp_favorites.html', fav_data=fav_data)

@my_page_bp.route('/password_reset', methods=["GET"])
def password_reset():
    mode = request.form.get("mode", "normal")
    return render_template('my_page/mp_password_reset.html', mode=mode)

@my_page_bp.route('/password_reset/process', methods=["POST"])
def password_reset_process():
    currPass = request.form.get("currentPassword")
    newPass = request.form.get("newPassword")
    conNewPass = request.form.get("confirmNewPassword")
    user_id = session['user_id']
    errmsg = None
    passcheck_sql = "SELECT password FROM user_tbl WHERE id = %s;"
    passcheck_data = fetch_query(passcheck_sql, (user_id,), True)
    passcheck_data = passcheck_data['password']
    print(passcheck_data)
    print(currPass)
    print(newPass)
    print(conNewPass)
    if passcheck_data == currPass:
        print("1st check")
        if newPass == conNewPass:
            print("2nd check")
            newpass_sql = "UPDATE user_tbl SET password = %s WHERE id = %s;"
            user_pass = create_user(newpass_sql, (newPass, user_id))
            print(user_pass)
            errmsg = None
            succmsg = "パスワードリセット成功"
            return render_template('my_page/mp_password_reset_success.html', succmsg=succmsg)
        else:
            errmsg = "パスワードと再入力のパスワードが一致していません"
    else:
        errmsg = "現在のパスワードが間違っています"
    return render_template('my_page/mp_password_reset_process.html', errmsg=errmsg)

@my_page_bp.route('/payment_history', methods=["GET"])
def payment_history():
    return render_template('my_page/mp_payment_history.html')

# 核心功能：卡列表 (GET - 读取数据)
@my_page_bp.route('/card_list', methods=["GET"])
def card_list():
    user_id = session.get('user_id')
    
    # 从 payment_tbl 中查询用户的 'クレジット' 记录
    card_sql = "SELECT card_num, card_name, card_expiration FROM payment_tbl WHERE user_id = %s AND account_type = 'クレジット';"
    card_data_raw = fetch_query(card_sql, (user_id,), fetch_one=True)
    
    card_data = None
    if card_data_raw:
        # 转换数据格式以匹配 mp_cards.html 模板的 Jinja2 变量
        expiry_mm = card_data_raw['card_expiration'][:2] if card_data_raw['card_expiration'] else ''
        expiry_yy_short = card_data_raw['card_expiration'][2:] if card_data_raw['card_expiration'] else ''
        
        card_data = {
            'card_number': card_data_raw['card_num'],
            'holder_name': card_data_raw['card_name'],
            'expiry_month': expiry_mm, 
            'expiry_year': '20' + expiry_yy_short, 
            'security_code': '',
        }

    return render_template('my_page/mp_cards.html', card_data=card_data)

# 核心功能：保存/更新卡片 (POST)
@my_page_bp.route('/save_card_info', methods=["POST"])
def save_card_info():
    user_id = session.get('user_id') 
    
    card_number = request.form.get('cardNumber')
    holder_name = request.form.get('cardHolderName')
    expiry_month = request.form.get('expiryMonth')
    expiry_year = request.form.get('expiryYear')
    
    # 1. 构造 card_expiration (payment_tbl 格式为 MMYY，所以取 YYYY 的后两位)
    expiry_mm_yy = expiry_month + expiry_year[-2:]
    
    # 2. 检查该用户是否已存在 'クレジット' 类型的记录
    # 🚨 修正：为 COUNT(*) 添加别名 AS record_count，解决 KeyError
    check_sql = "SELECT COUNT(*) AS record_count FROM payment_tbl WHERE user_id = %s AND account_type = 'クレジット';"
    
    # 🚨 修正：使用新的别名 'record_count'
    check_result = fetch_query(check_sql, (user_id,), fetch_one=True)
    
    # 检查 fetch_query 返回结果是否有效，然后检查别名
    card_exists = check_result and check_result.get('record_count', 0) > 0
    
    if card_exists:
        # 3. 存在记录，则更新 (UPDATE)
        update_sql = """
            UPDATE payment_tbl SET 
                card_num = %s, card_name = %s, card_expiration = %s, card_block = 0 
            WHERE user_id = %s AND account_type = 'クレジット';
        """
        params = (card_number, holder_name, expiry_mm_yy, user_id)
        
    else:
        # 4. 不存在记录，则插入 (INSERT)
        update_sql = """
            INSERT INTO payment_tbl 
                (user_id, card_num, card_name, card_expiration, account_type, card_block, monthly_sales, total_sales, withdrawal) 
            VALUES 
                (%s, %s, %s, %s, 'クレジット', 0, 0, 0, 0);
        """
        params = (user_id, card_number, holder_name, expiry_mm_yy)
        
    try:
        create_user(update_sql, params) 
        return jsonify({'success': True, 'message': 'クレジットカード情報が正常に保存されました。'})
    except Exception as e:
        print(f"Error saving card info: {e}")
        return jsonify({'success': False, 'message': '保存中に予期せぬエラーが発生しました。詳細はサーバーログを確認してください。', 'error': str(e)}), 500


@my_page_bp.route('/customer_support', methods=["GET"])
def customer_support():
    return render_template('my_page/mp_support.html')

@my_page_bp.route('/notifications', methods=["GET"])
def notifications():
    return render_template('my_page/mp_notifications.html')

@my_page_bp.route('/delete_account', methods=["GET"])
def delete_account():
    return render_template('my_page/mp_delete_account.html')