from flask import Blueprint, render_template, abort, session, request, redirect, current_app, url_for
from app.db import fetch_query, create_user, connect_db
import os
from werkzeug.utils import secure_filename

lesson_video_bp = Blueprint('lesson_video', __name__, url_prefix='/lesson_video')

@lesson_video_bp.route('play_video//<int:video_id>')
def video_player(video_id):
    sql = """
    SELECT *, v.id AS video_id FROM video_tbl v
    LEFT JOIN user_tbl u
    ON v.video_uploader_id = u.id
    WHERE v.id = %s;
    """ 
    video_data = fetch_query(sql, (video_id,), fetch_one=True)
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
    if 'user_id' in session:
        user_id = session['user_id']
        try:
            sql_check = "SELECT * FROM video_like_tbl WHERE user_id=%s AND video_id=%s"
            existing = fetch_query(sql_check, (user_id, video_id), fetch_one=True)
            if existing:
                delete_sql = "DELETE FROM video_like_tbl WHERE user_id=%s AND video_id=%s"
                delete_like = create_user(delete_sql, (user_id, video_id))
                return None
            else:
                sql_insert = "INSERT INTO video_like_tbl (user_id, video_id) VALUES (%s, %s)"
                add_like = create_user(sql_insert, (user_id, video_id))
                succmsg = "いいね登録完了"
                return succmsg
                
        except:
            errmsg = "ログインしていません"
            return errmsg
        
@lesson_video_bp.route('video_upload', methods=['POST'])
def video_upload():
    user_id = session['user_id']
    video_file = request.files.get('video_file')
    thumbnail_file = request.files.get('thumbnail_file')
    title = request.form.get('video_title')
    description = request.form.get('video_description')
    category = request.form.get('upload_category')
    
    local_upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'video')
    
    local_thumb_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'video_thumbnail')
    
    upload_folder = '/uploads/video'
    os.makedirs(upload_folder, exist_ok=True)
    thumb_folder = '/uploads/video_thumbnail'
    os.makedirs(thumb_folder, exist_ok=True)
    
    video_path = None
    if video_file:
        filename = secure_filename(video_file.filename)
        local_video_path = os.path.join(local_upload_folder, filename)
        video_path = upload_folder + "/"+ filename
        video_file.save(local_video_path)

    thumbnail_path = None
    if thumbnail_file:
        filename = secure_filename(thumbnail_file.filename)
        local_thumbnail_path = os.path.join(local_thumb_folder, filename)
        thumbnail_path = thumb_folder + "/" + filename
        thumbnail_file.save(local_thumbnail_path)
        sql = """
    INSERT INTO video_tbl
    (video_title, video_description_section, video_category, file_path, thumbnail_path, video_uploader_id, video_public_status)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql, (title, description, category, video_path, thumbnail_path, user_id, 1))
    con.commit()
    new_video_id = cur.lastrowid
    cur.close()
    con.close()
    return redirect(url_for("lesson_video.video_player", video_id = new_video_id))
        