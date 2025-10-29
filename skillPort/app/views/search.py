from flask import Blueprint, render_template, request, make_response, session
from app.db import fetch_query

search_bp = Blueprint('search', __name__, url_prefix='/search')

# ヘッダーでの検索機能
@search_bp.route('/header_search', methods=["GET"])
def header_search():
    search_word = request.args.get("headersearch")
    
    sql = "SELECT * FROM video_tbl WHERE video_title LIKE '%"+search_word+"%';"
    search_results = fetch_query(sql)
    print(search_results[0])
    return render_template('search/header_search_result.html', search_word=search_word, search_results=search_results)
    