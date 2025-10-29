from flask import Blueprint, render_template, request, make_response, session
from app.db import fetch_query

category_bp = Blueprint('category', __name__, url_prefix='/category')

@category_bp.route('/_list', methods=["GET"])
def category_list():
    cat_name = request.args.get("name")
    print(cat_name)
    return render_template('lesson_video/lecture_video_list.html', cat_name=cat_name)
