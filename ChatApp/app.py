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
# TODO:メッセージ一覧ページの表示
@app.route('/channels/<channel_id>/messages', methods=['GET'])
def messages_view():
    #
    return 'message view'

# TODO:メッセージの投稿
@app.route('/channels/<channel_id>/messages', methods=['POST'])
def create_message():
    return 'create message'

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
