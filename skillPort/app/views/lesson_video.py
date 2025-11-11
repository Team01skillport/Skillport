from flask import Blueprint, render_template, abort
from app.db import fetch_query  # market.py と同じように、DBヘルパーをインポートします

# 1. 'lesson_video' という名前でBlueprintを作成します
# URLの接頭辞 (prefix) は /lesson_video になります
lesson_video_bp = Blueprint('lesson_video', __name__, url_prefix='/lesson_video')

# 2. 動画再生ページのルートを定義します
# market.py の product_detail と同じように、URLに <int:video_id> を含めます
@lesson_video_bp.route('play_video//<int:video_id>')
def video_player(video_id):

    sql = """
    SELECT * FROM video_tbl v
    LEFT JOIN user_tbl u
    ON v.video_uploader_id = u.id
    WHERE v.id = %s;
    """  
    # fetch_query を使ってクエリを実行します。SQLインジェクション対策のため、
    # video_idはパラメータとして渡します。 (video_id,) のカンマを忘れないでください。
    video_data = fetch_query(sql, (video_id,), fetch_one=True)
    print(video_id)
    print(video_data)

    # もし動画が見つからなかった場合（結果が空の場合）、404エラーを表示します
    if not video_data:
        abort(404, "指定された動画は見つかりませんでした。")
        
    if video_data['profile_icon'] == None:
        video_data['profile_icon'] = "/icons/default_icon.png"
    
    # 4. 取得した動画データ (video) をテンプレートに渡します
    return render_template('lesson_video/video_player.html', video = video_data)