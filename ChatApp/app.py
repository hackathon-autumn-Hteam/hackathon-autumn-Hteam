from flask import Flask, request, session, redirect, url_for, render_template, flash
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os
import uuid
import hashlib

from models import User, Channel, Message, Prefecture, SupportMessage,  Mypage
from util.assets import bundle_css_files

jst = ZoneInfo("Asia/Tokyo")

# 定数定義
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

# 複数のCSSファイルを1つにまとめて圧縮（バンドル）する処理を実行。
bundle_css_files(app)


@app.route("/", methods=["GET"])
def index():
    """ルートページのリダイレクト処理

    Returns:
        flask.Response: リダイレクト先のHTTPレスポンス。
            - 未ログイン: ログインページ(login_view)へリダイレクト。
            - ログイン済み: チャンネル一覧ページ(channels_view)へリダイレクト。
    """
    # NOTE: sessionからuser_idを取得します。
    #       user_idがNoneの場合は、未ログインです。
    #       ログイン済みの場合のみ表示させたいページには、必ずこの処理を追加してください。
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))

    return redirect(url_for("channels_view"))


@app.route("/signup", methods=["GET"])
def signup_view():
    """サインアップページの表示

    Returns:
        flask.Response: サインアップページを描画したHTTPレスポンス。
    """
    prefectures = Prefecture.get_all()
    return render_template("auth/signup.html", prefectures=prefectures)


@app.route("/signup", methods=["POST"])
def signup():
    """サインアップ処理

    Returns:
        flask.Response: リダイレクト先のHTTPレスポンス。
            - 入力不備や登録エラー時: サインアップページ(signup_view)へのリダイレクト。
            - 登録成功時: チャンネル一覧ページ(channels_view)へのリダイレクト。
    """
    # 入力値の取得
    user_name = request.form.get("user_name")
    email = request.form.get("email")
    password = request.form.get("password")
    password_confirmation = request.form.get("password_confirmation")
    prefecture_id = request.form.get("prefecture_id")

    # 入力チェック
    if user_name == "":
        flash("名前を入力してください")
        return redirect(url_for("signup_view"))

    if email == "":
        flash("メールアドレスを入力してください")
        return redirect(url_for("signup_view"))

    if password != password_confirmation:
        flash("パスワードが一致しません")
        return redirect(url_for("signup_view"))

    if prefecture_id == "":
        flash("都道府県を選択してください")
        return redirect(url_for("signup_view"))

    # DBからユーザーを取得
    registered_user = User.find_by_email(email)
    if registered_user:
        flash("ユーザーを登録できませんでした")
        return redirect(url_for("signup_view"))

    # ユーザー登録
    user_id = uuid.uuid4()
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    User.create(user_id, user_name, email, password, prefecture_id)

    # ログイン済みとしてユーザーIDをセッションに保持
    session["user_id"] = user_id

    # 追加機能：新規登録してログインした時間帯の励ましメッセージを決める・セッションに保存
    hour = datetime.now(jst).hour

    support_message = SupportMessage.get_random_by_hour(hour)
    session["support_message"] = support_message

    session["support_message_hour"] = hour

    return redirect(url_for("channels_view"))


@app.route("/login", methods=["GET"])
def login_view():
    """ログインページの表示

    Returns:
        flask.Response: ログインページを描画したHTTPレスポンス。
    """
    return render_template("auth/login.html")


@app.route("/login", methods=["POST"])
def login():
    """ログイン処理

    Returns:
        flask.Response: リダイレクト先のHTTPレスポンス。
            - 入力不備や認証失敗時: ログインページ(login_view)へのリダイレクト。
            - 認証成功時: チャンネル一覧ページ(channels_view)へのリダイレクト。
    """
    # 入力値の取得
    email = request.form.get("email")
    password = request.form.get("password")

    # 入力チェック
    if email == "":
        flash("メールアドレスを入力してください")
        return redirect(url_for("login_view"))

    if password == "":
        flash("パスワードを入力してください")
        return redirect(url_for("login_view"))

    # DBからユーザーを取得
    user = User.find_by_email(email)
    if user is None:
        flash("メールアドレスが確認できませんでした")
        return redirect(url_for("login_view"))

    # パスワード照合
    hash_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    if user["password"] != hash_password:
        flash("ログインできませんでした")
        return redirect(url_for("login_view"))

    # 認証成功
    session["user_id"] = user["user_id"]

    # 追加機能：ログインした時間帯の励ましメッセージを決める・セッションに保存
    hour = datetime.now(jst).hour

    support_message = SupportMessage.get_random_by_hour(hour)
    session["support_message"] = support_message

    session["support_message_hour"] = hour

    return redirect(url_for("channels_view"))


@app.route("/logout", methods=["GET"])
def logout():
    """ログアウト処理

    Returns:
        flask.Response: リダイレクト先のHTTPレスポンス。
            ログインページ(login_view)へのリダイレクト。
    """
    session.clear()
    return redirect(url_for("login_view"))


# TODO(うっちーさん): チャンネル用の関数定義
# チャンネル一覧ページの表示
@app.route("/channels", methods=["GET"])
def channels_view():
    # 最初はセッションを抜いて作成するのが吉 今ログインしているユーザーのIDをセッションから取り出す
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))
    else:
        channels = Channel.get_all()
        # channels.reverse()  # チャンネルの順番を新しい順にする DB側→ORDER BYで設定？

    # 追加機能「励ましのメッセージ」
    # 現在の時刻（日本時間）を取得する
    current_hour = datetime.now(jst).hour

    # 前回のメッセージを決めたときの時間を取得する
    last_hour = session.get("support_message_hour")

    # ログイン時と時間帯が変わっていたらchannels.viewに遷移したタイミングでメッセージを更新する
    if last_hour != current_hour:
        support_message = SupportMessage.get_random_by_hour(current_hour)
        session["support_message"] = support_message
        session["support_message_hour"] = current_hour
    # 時間が変わっていなければログイン時に決めた励ましメッセージをセッションから取得する
    else:
        support_message = session.get("support_message")

    return render_template(
        "channels.html",
        channels=channels,
        user_id=user_id,
        support_message=support_message,
    )


# チャンネルの作成
@app.route("/channels", methods=["POST"])
def create_channel():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))

    channel_name = request.form.get("channel_name")
    channel = Channel.find_by_channel_name(channel_name)
    if channel == None:
        description = request.form.get("description")
        Channel.create(user_id, channel_name, description)
        return redirect(url_for("channels_view"))
    else:
        error = "既に同じ名前のチャンネルが存在しています"  # error効いていない　薄い色になっている 今はformを閉じてしまう（不親切）
        return redirect(url_for("channels_view"))

    # もしdescをNOT NULLなら、ちゃんとこれも定義しないといけない


# チャンネルの更新
@app.route("/channels/<channel_id>", methods=["PUT"])
def update_channel(channel_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))

    channel = Channel.find_by_channel_id(channel_id)

    if channel["user_id"] != user_id:
        flash(
            "チャンネルは作成者のみ更新が可能です"
        )  # テンプレート側との調整　確認する（保留）
    else:
        channel_name = request.form.get("channel_name")
        description = request.form.get("description")

        Channel.update(user_id, channel_name, description, channel_id)
    return redirect(f"/channel/{channel_id}/messages")


# チャンネルの削除
@app.route("/channels/<channel_id>", methods=["DELETE"])
def delete_channel(channel_id):
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))

    channel = Channel.find_by_channel_id(channel_id)

    if channel["user_id"] != user_id:
        flash(
            "チャンネルは作成者のみ削除が可能です"
        )  # テンプレート側との調整　確認する（保留）
    else:
        Channel.delete(channel_id)
    return redirect("channels_view")


@app.route("/channels/<channel_id>/messages", methods=["GET"])
def messages_view(channel_id):
    """メッセージ一覧表示

    詳細説明
    1.ログイン状態を確認
    2.チャンネル情報を取得
    3.メッセージ情報を取得
    4.メッセージページ、チャンネル情報、メッセージ情報を返す

    Args:
        引数名 channel_id, 型 str : 選択したチャンネルのID

    Returns:
        messages.html : メッセージ一覧表示のページ
        user_id, 型 str : メッセージ一覧表示をリクエストしたユーザーのID
        channel, 型 dict : 選択したチャンネル情報(channel_id,channel_name,description)
        messages, 型 list : 選択したチェンネルのメッセージ情報(message_id,user_id,user_name,prefecture_name,message_text,created_at)

    """
    # ユーザーがログインしているかを確認
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))

    channel = Channel.find_by_channel_id(channel_id)
    messages = Message.get_all(channel_id)

    return render_template(
        "messages.html", user_id=user_id, channel=channel, messages=messages
    )


@app.route("/channels/<channel_id>/messages", methods=["POST"])
def create_message(channel_id):
    """メッセージの投稿

    詳細説明
    1.ログイン状態を確認
    2.追加するメッセージを取得
    3.メッセージテーブルにメッセージを追加

    Args:
        引数名 channel_id, 型 str : 選択したチャンネルのID
    """

    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))

    message_text = request.form.get("message_text")

    if message_text:
        Message.create(user_id, channel_id, message_text)
    else:
        flash("メッセージが空白です")

    return redirect(f"/channels/{channel_id}/messages")


@app.route("/channels/<channel_id>/messages/<message_id>", methods=["PUT"])
def update_message(channel_id, message_id):
    """メッセージの編集

    詳細説明
    1.ログイン状態を確認
    2.編集するメッセージの情報を取得
    3.編集権限の確認
    4.編集するメッセージの取得
    5.メッセージテーブルの更新

    Args:
        引数名 channel_id, 型 str : 選択したチャンネルID
        引数名 message_id, 型 str : 編集するメッセージID
    """

    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))

    message = Channel.find_by_message_id(message_id)

    if message["user_id"] != user_id:
        flash("メッセージは作成者のみ更新が可能です")
    else:
        message_text = request.form.get("message_text")
        if message_text:
            Message.update(message_id, message_text)
        else:
            flash("メッセージが空白です")

    return redirect(f"/channels/{channel_id}/messages")


# メッセージの削除(追加機能)
@app.route("/channels/<channel_id>/messages/<message_id>", methods=["DELETE"])
def delete_message(channel_id, message_id):
    """メッセージの削除

    詳細説明
    1.ログイン状態を確認
    2.削除するメッセージの情報を取得
    3.編集権限の確認
    4.該当するメッセージIDの行を削除

    Args:
        引数名 channel_id, 型 str : 選択したチャンネルID
        引数名 message_id, 型 str : 編集するメッセージID
    """

    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))

    message = Channel.find_by_message_id(message_id)

    if message["user_id"] != user_id:
        flash("メッセージは作成者のみが削除できます")
    else:
        if message_id:
            Message.delete(message_id)

    return redirect(f"/channels/{channel_id}/messages")


@app.route("/channels/<channel_id>/messages/<message_id>/flowers", methods=["POST"])
def send_flower(channel_id, message_id):
    """お花を送る処理

    Args:
        channel_id (int): チャンネルID
        message_id (int): メッセージID

    Returns:
        flask.Response: リダイレクト先のHTTPレスポンス。
            メッセージ一覧ページ(messages_view)へのリダイレクト。
    """
    Message.send_flower(message_id)
    return redirect(f"/channels/{channel_id}/messages")


@app.route("/mypage")
def mypage_view():
    """マイページの表示

    詳細説明
    1.ログイン状態を確認
    2.ユーザー情報と都道府県のDBを取得
    3.テンプレートのユーザー情報を更新

    Returns:
        mypage.html, user(ユーザー情報), prefectures(都道府県のリスト)
    """
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))
    else:
        user = Mypage.get_all(user_id)
        prefectures = Prefecture.get_all()
        return render_template(
            "mypage.html", user=user, prefectures=prefectures
        )


@app.route("/users/<user_id>/prefecture", methods=["POST"])
def update_user_prefecture(user_id):
    """都道府県情報の更新

    詳細説明
    1.ログイン状態を確認
    2.変更後の都道府県情報を取得
    3.ユーザーの都道府県情報を更新
    4.テンプレートのユーザー情報を更新

    Args:
        user_id : ユーザーID

    Returns:
        mypage.html, user(ユーザー情報), prefectures(都道府県のリスト)
    """
    if user_id is None:
        return redirect(url_for("login_view"))
    else:
        prefecture_id = request.form.get("prefecture_id")
        if prefecture_id:
            Mypage.update(user_id, prefecture_id)
            user = Mypage.get_all(user_id)
            prefectures = Prefecture.get_all()
            return render_template(
            "mypage.html", user=user, prefectures=prefectures
            )
        else:
            flash("都道府県が空白です")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
