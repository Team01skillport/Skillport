from flask import Blueprint, render_template, abort, session
from app.db import fetch_query, create_user

# 1. 'lesson_video' という名前でBlueprintを作成します
# URLの接頭辞 (prefix) は /lesson_video になります
lesson_video_bp = Blueprint('lesson_video', __name__, url_prefix='/lesson_video')

# 2. 動画再生ページのルートを定義します
# market.py の product_detail と同じように、URLに <int:video_id> を含めます
@lesson_video_bp.route('play_video//<int:video_id>')
def video_player(video_id):

    sql = """
    SELECT *, v.id AS video_id FROM video_tbl v
    LEFT JOIN user_tbl u
    ON v.video_uploader_id = u.id
    WHERE v.id = %s;
    """  

    video_data = fetch_query(sql, (video_id,), fetch_one=True)
    print(video_data)

    if not video_data:
        abort(404, "指定された動画は見つかりませんでした。")
        
    if video_data['profile_icon'] == None:
        video_data['profile_icon'] = "/icons/default_icon.png"
    
    comment_sql = "SELECT * FROM video_tbl v LEFT JOIN video_comment_tbl vc ON v.id = vc.video_id LEFT JOIN user_tbl u ON vc.commentor_id = u.id WHERE v.id = %s"
    comment_data = fetch_query(comment_sql, (video_id,), fetch_one=False)
    
    view_sql = "SELECT v.*, COUNT(vv.id) AS view_count FROM video_tbl v LEFT JOIN video_view_tbl vv on v.id = vv.video_id WHERE v.id = %s GROUP BY v.id ORDER BY view_count DESC;"
    view_data = fetch_query(view_sql, (video_id,), fetch_one=True)
    
    rec_sql = f"SELECT * FROM video_tbl WHERE video_category LIKE '%{video_data['video_category']}%';"
    rec_data = fetch_query(rec_sql, params=None, fetch_one=False)
    
    if 'user_id' in session:
        user_id = session['user_id']
        sql_check = "SELECT * FROM video_view_tbl WHERE user_id = %s AND video_id = %s"
        viewed = fetch_query(sql_check, params=(user_id, video_id), fetch_one=True)
        if not viewed:
            sql_insert = "INSERT INTO video_view_tbl (user_id, video_id) VALUES (%s, %s)"
            create_user(sql_insert, params=(user_id, video_id))
    
    
    return render_template('lesson_video/video_player.html', video = video_data, comments=comment_data, rec_vids=rec_data, views=view_data)

@lesson_video_bp.route('like_video/<int:video_id>', methods=['POST'])
def video_like(video_id):
    print("LIKE RUN")
    
    if 'user_id' in session:
        user_id = session['user_id']
        print("USER IN")
        try:
            sql_check = "SELECT * FROM video_like_tbl WHERE user_id=%s AND video_id=%s"
            existing = fetch_query(sql_check, (user_id, video_id), fetch_one=True)
            print(existing)
            if existing:
                return None
            else:
                sql_insert = "INSERT INTO video_like_tbl (user_id, video_id) VALUES (%s, %s)"
                add_like = create_user(sql_insert, (user_id, video_id))
                print(add_like)
                succmsg = "いいね登録完了"
                return succmsg
                
        except:
            errmsg = "ログインしていません"
            return errmsg
        
        