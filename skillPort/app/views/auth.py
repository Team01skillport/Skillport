from flask import Blueprint, render_template, request, make_response, session
import mysql.connector

# Blueprintオブジェクトを作成
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# /auth/loginにアクセスされた際の処理を記述
@auth_bp.route('/login', methods=["GET"])
def login_form():

    return render_template('auth/login.html')

@auth_bp.route('/login_success', methods=["POST"])
def login_check():
    con = mysql.connector.connect(
    host="localhost",
    user = "root",
    passwd = "",
    db = "skillport_db"
    )
    
    username = request.form.get("userId")
    password = request.form.get("password")

    print(username)
    print(password)
    
    sql = "SELECT id FROM user_tbl WHERE user_name = '"+username+"' AND password = '"+password+"';"
    cur = con.cursor(dictionary=True)
    cur.execute(sql)
    user_info = cur.fetchone()
    print(user_info)
    if user_info == None:
        print("USER NOT FOUND")
        return render_template('auth/login.html')
    return render_template('index/index.html')

@auth_bp.route('/profile', methods=["GET"])
def view_profile():
    return render_template('profile/profile.html')