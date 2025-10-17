from flask import Flask
from datetime import timedelta
import os
import uuid


# 定数定義
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)


# TODO(はるか): ログイン・サインアップ用の関数定義


# TODO(うっちーさん): チャンネル用の関数定義


# TODO(rootさん): メッセージ用の関数定義


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
