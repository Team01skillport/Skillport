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

# !=======================カード追加部分=========================================
# =========================================================
# 核心功能：卡列表 (GET - 读取数据)
# =========================================================
@my_page_bp.route('/card_list', methods=["GET"])
def card_list():
    user_id = session.get('user_id')
    if not user_id:
        # 如果未登录，重定向到登录页
        return redirect(url_for('login')) 
    
    # SQL: 从 payment_tbl 中获取用户的信用卡信息
    card_fetch_sql = "SELECT card_num, card_name, card_expiration FROM payment_tbl WHERE user_id = %s AND account_type = 'クレジット';"
    card_data_raw = fetch_query(card_fetch_sql, (user_id,), fetch_one=True)
    
    card_data = None
    if card_data_raw:
        # 处理数据格式以适应前端显示 (mp_cards.html)
        card_number = card_data_raw.get('card_num', '')
        card_name = card_data_raw.get('card_name', '')
        card_expiration_db = card_data_raw.get('card_expiration', '') # 假设 DB 存储为 MMYY
        
        # 将 MMYY 格式分割为 MM 和 YYYY
        expiry_mm = card_expiration_db[:2] if len(card_expiration_db) >= 4 else ''
        expiry_yy = card_expiration_db[2:] if len(card_expiration_db) >= 4 else ''
        
        card_data = {
            'card_number': card_number,
            # card_number_display 用于在列表页显示 '**** **** **** 1234'
            'card_number_display': '**** **** **** ' + (card_number[-4:] if len(card_number) > 4 else card_number),
            'holder_name': card_name,
            'expiry_month': expiry_mm, 
            'expiry_year': ('20' + expiry_yy) if expiry_yy else '', # 传给模板的是四位数年份
        }
        
    return render_template('my_page/mp_cards.html', card_data=card_data)


# =========================================================
# 核心功能：保存/更新卡片 (POST - UPSERT)
# (已适配您提供的表单字段名和 MMYY 存储格式)
# =========================================================
@my_page_bp.route('/save_card_info', methods=["POST"])
def save_card_info():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'ユーザーはログインしていません。'}), 401

    # 使用用户提供的表单字段名
    card_number = request.form.get('cardNumber').replace(' ', '').replace('-', '') # 清理卡号
    holder_name = request.form.get('cardHolderName')
    expiry_month = request.form.get('expiryMonth')
    expiry_year = request.form.get('expiryYear')
    
    # 保持用户原有的 DB 存储格式: MMYY
    expiry_mm_yy = expiry_month + expiry_year[-2:] # 取年份后两位

    # 1. 检查记录是否存在 (使用 AS record_count)
    count_sql = "SELECT COUNT(*) AS record_count FROM payment_tbl WHERE user_id = %s AND account_type = 'クレジット';"
    count_result = fetch_query(count_sql, (user_id,), fetch_one=True)
    card_exists = count_result.get('record_count', 0) > 0
    
    if card_exists:
        # 存在记录，则更新 (UPDATE)
        update_sql = """
            UPDATE payment_tbl SET 
                card_num = %s, card_name = %s, card_expiration = %s, card_block = 0 
            WHERE user_id = %s AND account_type = 'クレジット';
        """
        params = (card_number, holder_name, expiry_mm_yy, user_id)
        
    else:
        # 不存在记录，则插入 (INSERT)
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


# =========================================================
# 核心功能：信用卡信息删除路由 (POST - DELETE)
# (新增功能，用于处理来自 mp_cards.html 的删除请求)
# =========================================================
@my_page_bp.route('/delete_card_info', methods=["POST"])
def delete_card_info():
    # 1. 检查用户是否登录
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'ユーザーはログインしていません。'}), 401

    # 2. SQL DELETE 语句：删除当前用户的信用卡记录
    delete_sql = "DELETE FROM payment_tbl WHERE user_id = %s AND account_type = 'クレジット';"
    
    try:
        # 3. 执行删除操作
        create_user(delete_sql, (user_id,))
        
        # 4. 删除成功，返回 JSON 响应
        return jsonify({'success': True, 'message': 'クレジットカード情報が正常に削除されました。'})
        
    except Exception as e:
        # 5. 删除失败，打印错误并返回 JSON 错误响应
        print(f"Error deleting card info: {e}")
        return jsonify({'success': False, 'message': '削除中に予期せぬエラーが発生しました。'}), 500

# !=======================カード追加部分終わり=========================================

@my_page_bp.route('/customer_support', methods=["GET"])
def customer_support():
    return render_template('my_page/mp_support.html')

@my_page_bp.route('/customer_support/sent', methods=["POST"])
def customer_support_sent():
    name = request.form.get("name")
    email = request.form.get("email")
    category = request.form.get("category")
    contents = request.form.get("details")
    user_id = session['user_id']
    sql = "INSERT INTO support_tbl (name, email, category, content, inquiry_user_id) VALUES (%s, %s, %s, %s, %s)"
    create_user(sql, (name, email, category, contents, user_id,))

    print(name)
    print(email)
    print(category)
    print(contents)

    redirect(url_for('my_page/mp_support.html'))
    return render_template('my_page/mp_cs_form_sent.html', succmsg="フォーム送信ができました。返事はメールでご確認ください。")

@my_page_bp.route('/notifications', methods=["GET"])
def notifications():
    return render_template('my_page/mp_notifications.html')

@my_page_bp.route('/delete_account', methods=["GET"])
def delete_account():
    return render_template('my_page/mp_delete_account.html')
    
@my_page_bp.route('/delete_account/process', methods=["POST"])
def delete_account_process():
    user_id = session['user_id']
    email = request.form.get("email")
    password = request.form.get("password")
    confirmPassword = request.form.get("confirmPassword")
    if password == confirmPassword:
        check_sql = "SELECT id, mail, password FROM user_tbl WHERE id = %s"
        check_data = fetch_query(check_sql,(user_id,), True)
        if check_data['password'] == password and check_data['mail'] == email:
            erase_user_id = check_data['id']            
            return render_template('my_page/mp_delete_account_process.html', user_id = erase_user_id)
        else:
            errmsg = "パスワードかメールが一致していません"
            return render_template('my_page/mp_delete_account_retry.html', errmsg=errmsg)
    else:
        errmsg = "パスワードと確認用パスワードが一致していません"
        return render_template('my_page/mp_delete_account_retry.html', errmsg=errmsg)
    
@my_page_bp.route('/delete_account/success', methods=["POST"])
def delete_account_success():
    user_id = request.form.get("user_id")
    erase_sql = "UPDATE user_tbl SET password = NULL WHERE id = %s;"
    create_user(erase_sql,(user_id,))
    session.pop('user_id', None)
    session.pop('user_name', None)

    return render_template('my_page/mp_delete_account_success.html', user_id=user_id)