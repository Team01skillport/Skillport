from flask import Blueprint, render_template, request, make_response, session
from app.db import fetch_query

search_bp = Blueprint('search', __name__, url_prefix='/search')

# ヘッダーでの検索機能
@search_bp.route('/header_search', methods=["GET"])
def header_search():
    search_word = request.args.get("headersearch")
    
    sql = "SELECT v.id AS video_id, v.*, u.* FROM video_tbl v LEFT JOIN user_tbl u ON v.video_uploader_id=u.id WHERE video_title LIKE '%"+search_word+"%';"
    search_results = fetch_query(sql,params=None,fetch_one=False)
    print(search_results)
    return render_template('search/header_search_result.html', search_word=search_word, search_results=search_results)
    
@search_bp.route('/market_search', methods=["GET"])
def market_search():
    keyword = request.args.get("market_search")
    sql = "SELECT * FROM listing_tbl WHERE product_name OR product_category LIKE '%"+keyword+"%';"
    search_results = fetch_query(sql)
    return render_template('search/market_search_result.html', search_results=search_results)