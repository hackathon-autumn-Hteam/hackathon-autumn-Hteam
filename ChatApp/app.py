from flask import Flask, request, session, redirect, url_for, render_template, flash 
from datetime import timedelta
import os
import uuid

from models import User, Channel, Message


# 定数定義
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)


# TODO(はるか): ログイン・サインアップ用の関数定義


# TODO(うっちーさん): チャンネル用の関数定義


# TODO(rootさん): メッセージ用の関数定義
# TODO:メッセージ一覧ページの表示
@app.route('/channels/<channel_id>/messages', methods=['GET'])
def messages_view():
    # ユーザーがログインしているかを確認
    user_id = session.get(user_id)
    if user_id is None:
        return redirect(url_for('login_view'))
    
    # channel_idのチャンネル名を取得(DBから)
    channel_name = Channel.find_by_cid(channel_id)

    # channel_idのメッセージを全て取得(DBから)
    messages = Message.get_all(channel_id)

    # user_id,チャンネル名,channel_idのmessage,メッセージページを返す
    return render_template('messages.html', messages=messages, channel_name=channel_name, user_id=user_id)

# TODO:メッセージの投稿
@app.route('/channels/<channel_id>/messages', methods=['POST'])
def create_message():
    return 'send message'

# TODO:メッセージの編集
@app.route('/channels/<channel_id>/messages/<message_id>', methods=['PUT'])
def update_message():
    return 'update message'

# TODO:メッセージの削除(追加機能)
@app.route('/channels/<channel_id>/messages/<message_id>', methods=['DELETE'])
def delete_message():
    return 'delete message'

# TODO:メッセージにお花(いいね)を押す(追加機能)
@app.route('/channels/<channel_id>/messages/<message_id>/flowers', methods=['POST'])
def send_flower():
    return 'send flower'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
