from flask import Blueprint, render_template, request, make_response, session
from app.db import fetch_query, create_user

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
        up_post_text = request.form.get("post_text")
        post_media = request.form.get("upload_media")
        print(up_post_text)
        print(post_media)
        if post_media == "":
            post_media = None
            sql = "INSERT INTO post_tbl (user_id, post_text) VALUES ("+ str(user_id)+", '"+up_post_text+"');" 
        else:
            sql = "INSERT INTO post_tbl (user_id, post_text, post_media) VALUES ("+ str(user_id)+", '"+up_post_text+"', '"+post_media+"');" 
        uploaded_post = create_user(sql)
        errmsg = ""
        print(uploaded_post)
    else:
        errmsg = "投稿するのにアカウントが必要です"
        
    return render_template('community/community.html', all_posts=all_posts, errmsg=errmsg)
    
    