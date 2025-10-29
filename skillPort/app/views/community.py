from flask import Blueprint, render_template, request, make_response, session
from app.db import fetch_query

community_bp = Blueprint('community', __name__, url_prefix='/community')

@community_bp.route('/community/top', methods=["GET"])
def community_top():
    return render_template('community/community.html')