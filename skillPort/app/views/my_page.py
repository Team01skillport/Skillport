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

@my_page_bp.route('/likes_list', methods=["GET"])
def likes_list():
    return render_template('my_page/mp_likes.html')

@my_page_bp.route('/sales_list', methods=["GET"])
def sales_list():
    return render_template('my_page/mp_sales.html')

@my_page_bp.route('/membership_list', methods=["GET"])
def membership_List():
    return render_template('my_page/mp_membership.html')

@my_page_bp.route('/favorites_list', methods=["GET"])
def favorites_list():
    return render_template('my_page/mp_favorites.html')

@my_page_bp.route('/password_reset', methods=["GET"])
def password_reset():
    return render_template('my_page/mp_password_reset.html')

@my_page_bp.route('/payment_history', methods=["GET"])
def payment_history():
    return render_template('my_page/mp_payment_history.html')

@my_page_bp.route('/card_list', methods=["GET"])
def card_list():
    return render_template('my_page/mp_cards.html')

@my_page_bp.route('/customer_support', methods=["GET"])
def customer_support():
    return render_template('my_page/mp_support.html')

@my_page_bp.route('/notifications', methods=["GET"])
def notifications():
    return render_template('my_page/mp_notifications.html')

@my_page_bp.route('/delete_account', methods=["GET"])
def delete_account():
    return render_template('my_page/mp_delete_account.html')