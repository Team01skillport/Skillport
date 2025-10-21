from flask import Blueprint, render_template, request, make_response, session

# Blueprintオブジェクトを作成
market_bp = Blueprint('market', __name__, url_prefix='/market')

@market_bp.route('/market/top', methods=["GET"])
def market_top():
    return render_template('market/market.html')