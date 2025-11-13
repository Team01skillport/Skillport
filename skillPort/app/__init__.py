from flask import Flask, render_template, session
from app.db import fetch_query, create_user
import math

def create_app():
    app = Flask(__name__,
                static_folder='static', 
                template_folder='templates')
    
    app.config.from_object('config.Config')

    from.views import auth, market, account, community, my_page, search, category, lesson_video, payment
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(market.market_bp)
    app.register_blueprint(account.account_bp)
    app.register_blueprint(community.community_bp)
    app.register_blueprint(my_page.my_page_bp)
    app.register_blueprint(search.search_bp)
    app.register_blueprint(category.category_bp)
    app.register_blueprint(lesson_video.lesson_video_bp)
    app.register_blueprint(payment.payment_bp)

    @app.route('/', methods=["GET"])
    def index():
        print("HEHSOHOHDSO")
        popular_sql = "SELECT v.id AS video_id, v.video_title, v.video_description_section, v.video_upload_date, u.user_name, v.video_popularity_index, v.thumbnail_path FROM video_tbl v INNER JOIN user_tbl u ON v.video_uploader_id = u.id ORDER BY v.video_popularity_index DESC LIMIT 6; "
        popular_videos = fetch_query(popular_sql, None, False)
        
        def video_reindex():
            video_sql = "SELECT v.id, v.video_public_status, v.video_popularity_index, COUNT(vv.id) AS view_count, COUNT(vl.id) AS like_count FROM video_tbl v LEFT JOIN video_view_tbl vv ON v.id = vv.video_id LEFT JOIN video_like_tbl vl ON v.id = vl.video_id WHERE v.video_public_status = 1 GROUP BY v.id ORDER BY v.video_popularity_index DESC;"
            video_data = fetch_query(video_sql, None, False)
                
            max_views = max(video['view_count'] for video in video_data) or 1
            max_likes = max(video['like_count'] for video in video_data) or 1

            for video in video_data:
                view_score = math.log1p(video['view_count']) / math.log1p(max_views)
                like_score = math.log1p(video['like_count']) / math.log1p(max_likes)

                popularity = round(
                    0.2 * video['video_public_status'] +
                    0.3 * view_score +
                    0.5 * like_score,
                    4
                )
                popularity_sql = "UPDATE video_tbl SET video_popularity_index = %s WHERE id = %s;"
                popularity_update = create_user(popularity_sql, (popularity, video['id'],))
            
            msg = "reindex complete"
            return msg
        video_reindex()
        return render_template('index/index.html', popvids=popular_videos)
    
    return app