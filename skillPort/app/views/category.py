from flask import Blueprint, render_template, request, make_response, session

# Blueprintオブジェクトを作成
category_bp = Blueprint('category', __name__, url_prefix='/category')

# /auth/loginにアクセスされた際の処理を記述
@category_bp.route('/list', methods=["GET"])
def category_list():
    
    return render_template('category/category.html')
