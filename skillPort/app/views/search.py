from flask import Blueprint, render_template, request, make_response, session

# Blueprintオブジェクトを作成
search_bp = Blueprint('search', __name__, url_prefix='/search')

# ヘッダーでの検索機能
@search_bp.route('/header_search', methods=["GET"])
def header_search():
    search_word = request.args.get("headersearch")
    if not search_word:
        print("NO TEXT")
        return render_template("index/index.html")
        
    return render_template('search/header_search_result.html', search_word=search_word)