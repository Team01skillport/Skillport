from flask import Blueprint, render_template, abort
from app.db import fetch_query  # market.py と同じように、DBヘルパーをインポートします

# 1. 'lesson_video' という名前でBlueprintを作成します
# URLの接頭辞 (prefix) は /lesson_video になります
lesson_video_bp = Blueprint('lesson_video', __name__, url_prefix='/lesson_video')

# 2. 動画再生ページのルートを定義します
# market.py の product_detail と同じように、URLに <int:video_id> を含めます
@lesson_video_bp.route('/<int:video_id>')
def video_player(video_id):
    """
    指定されたIDの動画データをデータベースから取得し、
    プレイヤーテンプレートに渡して表示します。
    """
    # 3. データベースに投げるSQLクエリを作成します
    # video_tbl (v) と user_tbl (u) を結合して、動画情報と投稿者名を取得します
    sql = """
        SELECT
            v.id,
            v.video_title,
            v.video_description_section,
            v.view_count,
            v.like_count,
            v.comment_count,
            v.file_path,
            v.video_upload_date,
            u.user_name AS uploader_name,
            u.profile_icon AS uploader_icon
        FROM
            video_tbl v
        JOIN
            user_tbl u ON v.video_uploader_id = u.id
        WHERE
            v.id = %s
    """
    # fetch_query を使ってクエリを実行します。SQLインジェクション対策のため、
    # video_idはパラメータとして渡します。 (video_id,) のカンマを忘れないでください。
    video_data = fetch_query(sql, (video_id,))

    # もし動画が見つからなかった場合（結果が空の場合）、404エラーを表示します
    if not video_data:
        abort(404, "指定された動画は見つかりませんでした。")
        
    # fetch_query はリストを返すので、最初の要素を取得します
    video = video_data[0]
    
    # 4. 取得した動画データ (video) をテンプレートに渡します
    return render_template('lesson_video/video_player.html', video=video)