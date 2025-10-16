# ==========================================================
# Filename      : config.py
# Descriptions  : 設定ファイル
# ==========================================================
import os

class Config:
    # Flaskのセッション機能や特定の拡張機能で暗号化キーとして使用される
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key_py24'
