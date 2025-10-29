from flask import Blueprint, render_template, request, make_response, session, redirect, url_for, flash
from app.db import fetch_query

# Blueprintオブジェクトを作成
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get("userId")
        password = request.form.get("password")

        sql = "SELECT id, user_name FROM user_tbl WHERE user_name = '"+username+"' AND password = '"+password+"';"
        user_info = fetch_query(sql, True)
        
        if user_info:
            session['user_id'] = user_info['id']
            session['user_name'] = user_info['user_name']
            
            return redirect(url_for('auth.view_profile'))
        else:
            errmsg = "ユーザーIDまたはパスワードが正しくありません。"
            return render_template('auth/login.html', errmsg=errmsg)

    if 'user_id' in session:
        return redirect(url_for('auth.view_profile'))
        
    return render_template('auth/login.html', errmsg="")

@auth_bp.route('/profile', methods=["GET"])
def view_profile():
    if 'user_id' in session:
        return render_template('profile/profile.html', user_name=session['user_name'])
    else:
        return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('auth.login'))