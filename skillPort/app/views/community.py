from flask import Blueprint, render_template, request, make_response, session, redirect, url_for, current_app
from app.db import fetch_query, create_user
from werkzeug.utils import secure_filename
import os

community_bp = Blueprint('community', __name__, url_prefix='/community')

@community_bp.route('/community/top', methods=["GET"])
def community_top():
    sql = "select p.*, u.id AS user_id, u.user_name, u.profile_icon from post_tbl p INNER JOIN user_tbl u ON p.user_id = u.id ORDER BY post_update_date DESC;"
    all_posts = fetch_query(sql)
    
    sql = "select * FROM video_tbl ORDER"
    try:
        user_id = session['user_id']
    except:
        user_id = "guest"
    return render_template('community/community.html', all_posts=all_posts, user_id=user_id)

@community_bp.route('/community/upload_post', methods=["POST"])
def upload_post():
    sql = "select p.*, u.id AS user_id, u.user_name, u.profile_icon from post_tbl p INNER JOIN user_tbl u ON p.user_id = u.id ORDER BY post_update_date DESC;"
    all_posts = fetch_query(sql)
    if 'user_id' in session:
        user_id = session['user_id']
        up_post_text = request.form.get("post_text", "").strip()
        post_media = request.form.get("upload_media", "None").strip()
            
        file = request.files.get("upload_media")
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, "static")
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            post_media = f"/media/posts/{filename}"
        else:
            post_media = None
        
        sql = "INSERT INTO post_tbl (user_id, post_text, post_media) VALUES (%s, %s, %s);" 
        uploaded_post = create_user(sql, (user_id, up_post_text, post_media))
        print(uploaded_post)
        return redirect(url_for('community.community_top', all_posts=all_posts))
    else:
        return redirect(url_for('auth.login'))
        
    
