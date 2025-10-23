from flask import Blueprint, render_template, request, make_response, session
import mysql.connector


# Blueprintオブジェクトを作成
search_bp = Blueprint('search', __name__, url_prefix='/search')

# ヘッダーでの検索機能
@search_bp.route('/header_search', methods=["GET"])
def header_search():
    search_word = request.args.get("headersearch")
    con = mysql.connector.connect(
   host="localhost",
    port = 8889,
    user = "root",
    passwd = "root",
    db = "skillport_db"
    )
    
    
    sql = "SELECT * FROM video_tbl WHERE video_title LIKE '%"+search_word+"%';"
    cur = con.cursor(dictionary=True)
    cur.execute(sql)
    search_results = cur.fetchall()
    print(search_results[0])
    return render_template('search/header_search_result.html', search_word=search_word, search_results=search_results)
    