from flask import Flask, render_template, request, session, redirect, url_for
from app.db import fetch_query 
import os

# (Blueprint)
from app.views.auth import auth_bp
from app.views.market import market_bp 
from app.views.community import community_bp
from app.views.category import category_bp
from app.views.search import search_bp
from app.views.account import account_bp
from app.views.lesson_video import lesson_video_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

app.register_blueprint(auth_bp)
app.register_blueprint(market_bp)
app.register_blueprint(community_bp)
app.register_blueprint(category_bp)
app.register_blueprint(search_bp)
app.register_blueprint(account_bp)
app.register_blueprint(lesson_video_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run(host = "localhost", port=5000)