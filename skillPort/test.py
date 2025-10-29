from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# MySQL接続関数
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",       # XAMPPのMySQLサーバー
        user="root",            # デフォルトユーザー
        password="",            # パスワード未設定なら空欄
        database="video_db"     # 作成済みのデータベース名
    )

@app.route('/lecture')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, file_name, drive_file_id, upload_date FROM videos")
    videos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('lecture_video.html', videos=videos)

if __name__ == '__main__':
    app.run(debug=True)