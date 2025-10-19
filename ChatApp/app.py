from flask import Flask, session, redirect, url_for
from datetime import timedelta
import os
import uuid


# 定数定義
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)


@app.route("/", methods=["GET"])
def index():
    """ルートページのリダイレクト処理

    ユーザーのログイン状態に応じて遷移先を切り替える。
    - 未ログインの場合はログインページ(login_view)へリダイレクト。
    - ログイン済みの場合はチャンネル一覧ページ(channels_view)へリダイレクト。

    Returns:
        flask.Response: リダイレクト先のレスポンスオブジェクト。
    """
    # NOTE: sessionからuser_idを取得します。
    #       user_idがNoneの場合は、未ログインです。
    #       ログイン済みの場合のみ表示させたいページには、必ずこの処理を追加してください。
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))
    return redirect(url_for("channels_view"))


# TODO(はるか): signup_view関数の実装
@app.route("/signup", methods=["GET"])
def signup_view():
    pass


# TODO(はるか): signup関数の実装
@app.route("/signup", methods=["POST"])
def signup():
    pass


# TODO(はるか): login_view関数の実装
@app.route("/login", methods=["GET"])
def login_view():
    pass


# TODO(はるか): login関数の実装
@app.route("/login", methods=["POST"])
def login():
    pass


# TODO(はるか): logout関数の実装
@app.route("/logout", methods=["GET"])
def logout():
    pass


# TODO(うっちーさん): チャンネル用の関数定義


# TODO(rootさん): メッセージ用の関数定義


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
