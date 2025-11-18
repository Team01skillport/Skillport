from flask import Blueprint, render_template, request, make_response, session, redirect, url_for
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

# @my_page_bp.route('/card_list', methods=["GET"])
# def card_list():
#     return render_template('my_page/mp_cards.html')

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