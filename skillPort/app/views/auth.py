from flask import Blueprint, render_template, request, make_response, session, redirect, url_for, flash
from app.db import fetch_query

# Blueprintオブジェクトを作成
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get("userId")
        password = request.form.get("password")
        
        sql = "SELECT id, user_name FROM user_tbl WHERE user_name = '"+username+"' AND password = '"+password+"';"
        user_info = fetch_query(sql, params=None, fetch_one=True)
        print(user_info)
        if user_info:
            session['user_id'] = user_info['id']
            session['user_name'] = user_info['user_name']
            
            return redirect(url_for('auth.view_profile', user_id=session['user_id']))
        else:
            errmsg = "ユーザーIDまたはパスワードが正しくありません。"
            return render_template('auth/login.html', errmsg=errmsg)

    if 'user_id' in session:
        return redirect(url_for('auth.view_profile', user_id=session['user_id']))
        
    return render_template('auth/login.html', errmsg="")

@auth_bp.route('/profile/<user_id>', methods=["GET"])
def view_profile(user_id):
    sql = "SELECT * FROM user_tbl WHERE id = '"+str(user_id)+"';"
    user_info = fetch_query(sql, params=None, fetch_one=True)
    user_name = user_info['user_name']
    if user_info is None:
        return "ユーザーは存在しない"
    
    # ユーザーのアイコン取得
    user_icon = user_info['profile_icon']
    if user_icon == None:
        user_icon = "/icons/default_icon.png"
   
#    ユーザーの自己紹介文の取得
    try:
        introduction = user_info['introduction']
    except:
        introduction = ""
    
    # ユーザーの評価をとって、スターで表示する
    user_rating = int(user_info['user_rating'])
    
    rating_stars = []
    full_rating = 5
    if user_rating == 0:
        rating_stars.append("☆☆☆☆☆")
    else:
        for i in range(user_rating):
            rating_stars.append("★")
        if i < full_rating:
            for j in range(full_rating - i - 1):
                rating_stars.append("☆")
    
    # ユーザーのタグ文字列をとって、カンマに区切る
    try:
        user_tags = user_info['user_tags']
        tag = [tag.strip() for tag in user_tags.split(",")]
    except:
        tag = ""
        
    # ユーザーがアップした動画を表示する
    sql = "SELECT v.*, COUNT(vv.id) AS view_count FROM video_tbl v LEFT JOIN user_tbl u ON v.video_uploader_id = u.id LEFT JOIN video_view_tbl vv ON v.id = vv.video_id WHERE u.id = '"+str(user_id)+"';"
    user_videos = fetch_query(sql)
    if not user_videos:
        user_videos = []
    print(user_videos)
        

    
    # プロフィールでの投稿動画のタグを区切る
    # video_tag = []
    # for video in user_videos:
    #     try:
    #         video_tags = video['video_tag']
    #         video_tag.append([tag.strip() for tag in video_tags.split(",")])
    #     except:
    #         video_tag = ""
    
    # ユーザーがアップした投稿を表示する
    sql = "SELECT p.* FROM post_tbl p INNER JOIN user_tbl u ON p.user_id = u.id WHERE u.id = '"+str(user_id)+"' ORDER BY post_date DESC;"
    user_posts = fetch_query(sql)
    return render_template('profile/profile.html', user_name=user_name, user_info=user_info, user_icon=user_icon, introduction=introduction, tag=tag, rating_stars=rating_stars, user_videos=user_videos, user_posts=user_posts, novid_msg="このユーザーはまだ動画をアップしていません", nopost_msg="このユーザーはまだ投稿していません")


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('auth.login'))