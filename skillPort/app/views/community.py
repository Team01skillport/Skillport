from flask import Blueprint, render_template, request, make_response, session
from app.db import fetch_query

community_bp = Blueprint('community', __name__, url_prefix='/community')

@community_bp.route('/community/top', methods=["GET"])
def community_top():
    sql = "select p.*, u.id AS user_id, u.user_name, u.profile_icon from post_tbl p INNER JOIN user_tbl u ON p.user_id = u.id ORDER BY post_update_date ASC;"
    all_posts = fetch_query(sql)
    
    if 'user_id' in session:
        user_id = session['user_id']
    return render_template('community/community.html', all_posts=all_posts, user_id=user_id)