from flask import Blueprint, render_template, request, make_response, session

# Blueprintオブジェクトを作成
my_page_bp = Blueprint('my_page', __name__, url_prefix='/my_page')

@my_page_bp.route('/top', methods=["GET"])
def my_page_top():
    return render_template('my_page/mp_menu.html')

@my_page_bp.route('/view_history', methods=["GET"])
def my_page_history():
    return render_template('my_page/mp_view_history.html')

@my_page_bp.route('/bank_account_register', methods=["GET"])
def bank_account_register():
    return render_template('my_page/mp_bank_account_register.html')
