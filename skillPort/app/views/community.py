from flask import Blueprint, render_template, request, make_response, session, redirect, url_for, current_app
from app.db import fetch_query, create_user
from werkzeug.utils import secure_filename
import os

community_bp = Blueprint('community', __name__, url_prefix='/community')

@community_bp.route('/community/top', methods=["GET"])
def community_top():
    # フィード投稿の取得
    sql = "select p.*, u.id AS user_id, u.user_name, u.profile_icon from post_tbl p INNER JOIN user_tbl u ON p.user_id = u.id ORDER BY post_update_date DESC;"
    all_posts = fetch_query(sql)
    
    # おすすめ商品 (マーケットからランダムに3件取得)
    sql_recommended_products = """
        SELECT 
            l.product_id, 
            l.product_name, 
            l.product_price, 
            l.product_description,
            i.image_path
        FROM 
            listing_tbl l
        LEFT JOIN 
            listing_images_tbl i ON l.product_id = i.product_id AND i.is_thumbnail = 1
        WHERE 
            l.listing_status = 1 AND l.sales_status = 'S'
        ORDER BY 
            RAND()
        LIMIT 3
    """
    recommended_products = fetch_query(sql_recommended_products)
    
    sql = "select * FROM video_tbl ORDER"
    try:
        user_id = session['user_id']
    except:
        user_id = "guest"
        
    return render_template(
        'community/community.html', 
        all_posts=all_posts, 
        user_id=user_id,
        recommended_products=recommended_products # 新しく追加
    )

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
            # 【注意】ファイルパスの修正: 'static' フォルダ内を指すように変更
            # 投稿メディアは 'static/media/posts' に保存されていると仮定し、
            # community.htmlの表示に合わせてファイルパスを調整します。
            media_posts_folder = os.path.join(current_app.root_path, "static", "media", "posts")
            os.makedirs(media_posts_folder, exist_ok=True)
            file_path = os.path.join(media_posts_folder, filename)
            file.save(file_path)
            post_media = f"{filename}" # テンプレートで 'media/posts/' と結合するためファイル名のみ保存
        else:
            post_media = None
        
        sql = "INSERT INTO post_tbl (user_id, post_text, post_media) VALUES (%s, %s, %s);" 
        uploaded_post = create_user(sql, (user_id, up_post_text, post_media))
        print(uploaded_post)
        return redirect(url_for('community.community_top', all_posts=all_posts))
    else:
        return redirect(url_for('auth.login'))