from flask import Blueprint, render_template, request, make_response, session, redirect, url_for, flash
import mysql.connector

# Blueprintオブジェクトを作成
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",

        # 自分のMySQLのユーザー名とパスワードを指定してくだいさい
        user="root",
        passwd="",
        db="skillport_db"
    )

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get("userId")
        password = request.form.get("password")

        con = get_db_connection()
        cur = con.cursor(dictionary=True)

        sql = "SELECT id, user_name FROM user_tbl WHERE user_name = %s AND password = %s"
        cur.execute(sql, (username, password))
        user_info = cur.fetchone()
        
        cur.close()
        con.close()
        
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