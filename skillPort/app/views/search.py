from flask import Blueprint, render_template, request, make_response, session

# Blueprintオブジェクトを作成
search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/header_search', methods=["GET"])
def header_search():
    errtbl = {}
    search_word = request.args.get("headersearch")
    if not search_word:
        errtbl["empty"] = "検索する文字を入力をしてください"
    print(search_word)
    return render_template('search/header_search_result.html', search_word=search_word)