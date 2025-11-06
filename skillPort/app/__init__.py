# ==========================================================
# Filename      : app/__init__.py
# Descriptions  : Application Factory
# ==========================================================
from flask import Flask, render_template, session

def create_app():
    # Flaskアプリケーションのインスタンスを作成
    # __name__をappパッケージのパスに設定
    app = Flask(__name__,
                static_folder='static', 
                template_folder='templates')
    
    # config.pyから設定を読み込む
    app.config.from_object('config.Config')

    # --- Blueprintの登録 ---
    # viewsパッケージからproductsとauthのBlueprintをインポート
    # （）
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


    # --- トップページのルートをここで定義 ---
    @app.route('/', methods=["GET"])
    def index():
        return render_template('index/index.html')
    
    return app