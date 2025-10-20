from flask import Flask, request, session, redirect, url_for, render_template, flash
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
        flask.Response: リダイレクト先のHTTPレスポンス。
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
    return render_template("auth/signup.html")  # TODO: フロント側との調整


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
# チャンネル一覧ページの表示
@app.route('/channels', methods=['GET'])
def channels_view():
    # 最初はセッションを抜いて作成するのが吉 今ログインしているユーザーのIDをセッションから取り出す
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    else:
        channels = Channels.get_all()
        channels.reverse()  # チャンネルの順番を新しい順にする DB側→ORDER BYで設定？
        # 今後変動の可能性あり　変数としてchannels(全チャンネルの一覧)とuid（ログイン中のユーザID）をHTMLに渡す
        return render_template('channels.html', channels=channels, user_id=user_id)


# チャンネルの作成
@app.route('/channels', methods=['POST'])
def create_channel():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))

    channel_name = request.form.get(
        'channel_name')  # formのタイトルと　191さんと合わせる必要あり
    channel = Channel.find_by_name(channel_name)
    if channel == None:
        description = request.form.get('description')
        Channel.create(user_id, channel_name, description)
        return redirect(url_for('channels_view'))
    else:
        error = '既に同じ名前のチャンネルが存在しています'  # error効いていない　薄い色になっている 今はformを閉じてしまう（不親切）
        return redirect(url_for('channels_view'))

    # もしdescをNOT NULLなら、ちゃんとこれも定義しないといけない


# チャンネルの更新
@app.route('/channels/<channel_id>', methods=['PUT'])
def update_channel(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))

    channel = Channel.find_by_channel_id(channel_id)

    if channel['user_id'] != user_id:
        flash('チャンネルは作成者のみ更新が可能です')  # テンプレート側との調整　確認する（保留）
    else:
        channel_name = request.form.get('channel_name')
        description = request.form.get('description')

        Channel.update(user_id, channel_name, description, channel_id)
    return redirect(f'/channel/{channel_id}/messages')


# チャンネルの削除
@app.route('/channels/<channel_id>', methods=['DELETE'])
def delete_channel(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))

    channel = Channel.find_by_channel_id(channel_id)

    if channel['user_id'] != user_id:
        flash('チャンネルは作成者のみ削除が可能です')  # テンプレート側との調整　確認する（保留）
    else:
        Channel.delete(channel_id)
    return redirect('channels_view')


# TODO(rootさん): メッセージ用の関数定義


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)  # port=5001を追記　消すこと！！！
