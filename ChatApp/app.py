from flask import Flask, request, session, redirect, url_for, render_template, flash
from datetime import timedelta
import os
import uuid
import hashlib

from models import User, Channel, Message


# 定数定義
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)


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
    return render_template("auth/signup.html")


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
    # TODO(はるか): フロント側との調整(パスワードの確認フォームを用意するか)
    password_confirmation = request.form.get("password_confirmation")
    prefecture_id = request.form.get("prefecture_id")

    # 入力チェック
    if user_name == "":
        flash("名前を入力してください。")  # TODO(はるか): フロント側との調整
        return redirect(url_for("signup_view"))

    if email == "":
        flash("メールアドレスを入力してください。")  # TODO(はるか): フロント側との調整
        return redirect(url_for("signup_view"))

    if password != password_confirmation:
        flash("パスワードが一致しません。")  # TODO(はるか): フロント側との調整
        return redirect(url_for("signup_view"))

    if prefecture_id == "":
        flash("都道府県を選択してください。")  # TODO(はるか): フロント側との調整
        return redirect(url_for("signup_view"))

    # DBからユーザーを取得
    registered_user = User.find_by_email(email)
    if registered_user:
        flash("ユーザーを登録できませんでした。")  # TODO(はるか): フロント側との調整
        return redirect(url_for("signup_view"))

    # ユーザー登録
    user_id = uuid.uuid4()
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    User.create(user_id, user_name, email, password, prefecture_id)

    # ログイン済みとしてユーザーIDをセッションに保持
    session["user_id"] = user_id
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
        flash("メールアドレスを入力してください。")  # TODO(はるか): フロント側との調整
        return redirect(url_for("login_view"))

    if password == "":
        flash("パスワードを入力してください。")  # TODO(はるか): フロント側との調整
        return redirect(url_for("login_view"))

    # DBからユーザーを取得
    user = User.find_by_email(email)
    if user is None:
        flash(
            "メールアドレスまたはパスワードが間違っています。"
        )  # TODO(はるか): フロント側との調整
        return redirect(url_for("login_view"))

    # パスワード照合
    hash_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    if user.password != hash_password:
        flash(
            "メールアドレスまたはパスワードが間違っています。"
        )  # TODO(はるか): フロント側との調整
        return redirect(url_for("login_view"))

    # 認証成功
    session["user_id"] = user.user_id
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
        channels.reverse()  # チャンネルの順番を新しい順にする DB側→ORDER BYで設定？
        return render_template(
            "channels.html", channels=channels, user_id=user_id
        )  # 今後変動の可能性あり　変数としてchannels(全チャンネルの一覧)とuid（ログイン中のユーザID）をHTMLに渡す


# チャンネルの作成
@app.route("/channels", methods=["POST"])
def create_channel():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("login_view"))

    channel_name = request.form.get(
        "channel_name"
    )  # formのタイトルと　191さんと合わせる必要あり
    channel = Channel.find_by_name(channel_name)
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


# TODO(rootさん): メッセージ用の関数定義
# TODO:メッセージ一覧ページの表示
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
        messages, 型 list : 選択したチェンネルのメッセージ情報(message_id,user_id,user_name,prefecture_name,message_txt,created_at)

    """
    # ユーザーがログインしているかを確認
    user_id = session.get("user_id")  # sessionの情報はどこで定義されているのだろう？
    if user_id is None:  # ログインしていない場合は、ログインページのURLへ自動転送
        return redirect(url_for("login_view"))

    # 該当するchannel_idのチャンネル情報を取得(channel_id、channel_name、description)
    channel = Channel.find_by_channel_id(channel_id)

    # 該当するchannel_idのmessages情報を全て取得(message_id, user_id, user_name, prefecture_name, message_txt, created_at)
    messages = Message.get_all(channel_id)

    # メッセージ作成欄に「メッセージを入力してください」と表示
    flash("メッセージを入力してください")

    # メッセージページ,ユーザーID, channel情報, メッセージ情報を返す
    return render_template(
        "messages.html", user_id=user_id, channel=channel, messages=messages
    )


# TODO:メッセージの投稿
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
    # ログイン状態の確認
    user_id = session.get("user_id")
    if user_id is None: # ログインしていない場合は、ログインページのURLへ自動転送
        return redirect(url_for("login_view"))

    # メッセージの取得
    message_txt = request.form.get("message_txt")

    if message_txt: # メッセージが空白でない場合は、セッセージをDBに追加
        Message.create(user_id, channel_id, message_txt)
    else: # メッセージが空白の場合は、メッセージが空白であることをモーダルで表示
        flash("メッセージが空白です")

    # 選択したチャンネルのメッセージページにリダイレクト
    return redirect("/channels/{channel_id}/messages".format(channel_id = channel_id))

# TODO:メッセージの編集
@app.route("/channels/<channel_id>/messages/<message_id>", methods=["PUT"])
def update_message(channel_id,message_id):
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
    # ログイン状態の確認
    user_id = session.get("user_id")
    if user_id is None: # ログインしていない場合は、ログインページのURLへ自動転送
        return redirect(url_for("login_view"))

    # massagesテーブルから該当するメッセージIDの行を抽出(message_id, user_id, channel_id, message_txt, created_at)
    message = Channel.find_by_message_id(message_id)

    if message["user_id"] != user_id: # メッセージの作成者かどうかを確認
        flash("メッセージは作成者のみ更新が可能です")
    else:
        message_txt = request.form.get("message_txt")
        if message_txt: # メッセージが空白でない場合は、セッセージをDBに追加
            Message.update(message_id, message_txt)
        else:
            flash("メッセージが空白です")

    # 選択したチャンネルのメッセージページにリダイレクト
    return redirect("/channels/{channel_id}/messages".format(channel_id = channel_id))

# TODO:メッセージの削除(追加機能)
@app.route("/channels/<channel_id>/messages/<message_id>", methods=["DELETE"])
def delete_message(channel_id,message_id):
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

    # ログイン状態の確認
    user_id = session.get("user_id")
    if user_id is None: # ログインしていない場合は、ログインページのURLへ自動転送
        return redirect(url_for("login_view"))

    # massagesテーブルから該当するメッセージIDの行を抽出(message_id, user_id, channel_id, message_txt, created_at)
    message = Channel.find_by_message_id(message_id)

    if message["user_id"] != user_id: # メッセージの作成者かどうかを確認
        flash("メッセージは作成者のみが削除できます")
    else:
        if message_id:
            Message.delete(message_id)

    # 選択したチャンネルのメッセージページにリダイレクト
    return redirect("/channels/{channel_id}/messages".format(channel_id = channel_id))

# TODO:メッセージにお花(いいね)を押す(追加機能)
@app.route("/channels/<channel_id>/messages/<message_id>/flowers", methods=["POST"])
def send_flower():
    return "send flower"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
