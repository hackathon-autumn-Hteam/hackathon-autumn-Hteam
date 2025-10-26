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
#チャンネル一覧ページの表示
@app.route('/channels', methods = ['GET'])
def channels_view():
    user_id = session.get('user_id')             #最初はセッションを抜いて作成するのが吉 今ログインしているユーザーのIDをセッションから取り出す
    if user_id is None:
        return redirect(url_for('login_view'))
    else:
        channels = Channel.get_all()
        channels.reverse()                      #チャンネルの順番を新しい順にする DB側→ORDER BYで設定？
        return render_template('channels.html' , channels=channels,user_id=user_id)     #今後変動の可能性あり　変数としてchannels(全チャンネルの一覧)とuid（ログイン中のユーザID）をHTMLに渡す


#チャンネルの作成
@app.route('/channels', methods = ['POST'])
def create_channel():
    user_id = session.get('user_id')
    if user_id is None:                             
        return redirect(url_for('login_view'))
    
    channel_name = request.form.get('channel_name')   #formのタイトルと　191さんと合わせる必要あり
    channel = Channel.find_by_name(channel_name)
    if  channel == None:
        description = request.form.get('description')
        Channel.create(user_id, channel_name, description)
        return redirect(url_for('channels_view'))
    else:
        error = '既に同じ名前のチャンネルが存在しています'  #error効いていない　薄い色になっている 今はformを閉じてしまう（不親切）
        return redirect(url_for('channels_view'))
    
    #もしdescをNOT NULLなら、ちゃんとこれも定義しないといけない


#チャンネルの更新
@app.route('/channels/<channel_id>', methods = ['PUT'])
def update_channel(channel_id):                   
    user_id = session.get('user_id')
    if user_id is None:                             
        return redirect(url_for('login_view'))
    
    channel = Channel.find_by_channel_id(channel_id)
     
    if channel['user_id'] != user_id:
        flash('チャンネルは作成者のみ更新が可能です')   #テンプレート側との調整　確認する（保留）
    else:  
        channel_name = request.form.get('channel_name')
        description = request.form.get('description') 
    
        Channel.update(user_id, channel_name, description, channel_id)
    return redirect(f'/channel/{channel_id}/messages')    


#チャンネルの削除
@app.route('/channels/<channel_id>', methods = ['DELETE'])
def delete_channel(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view')) 
    
    channel = Channel.find_by_channel_id(channel_id)
    
    if channel['user_id'] != user_id:
        flash('チャンネルは作成者のみ削除が可能です')   #テンプレート側との調整　確認する（保留）
    else:
        Channel.delete(channel_id)
    return redirect('channels_view')


# TODO(rootさん): メッセージ用の関数定義
# TODO:メッセージ一覧ページの表示
@app.route('/channels/<channel_id>/messages', methods=['GET'])
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
        channel, 型 dict : 選択したチャンネル情報(channel_id,channel_name,discription)
        messages, 型 list : 選択したチェンネルのメッセージ情報(message_id,user_id,user_name,prefecture_name,message_txt,created_at)

    """
    # ユーザーがログインしているかを確認
    user_id = session.get('user_id') #sessionの情報はどこで定義されているのだろう？
    if user_id is None: # ログインしていない場合は、ログインページのURLへ自動転送
        return redirect(url_for('login_view'))
    
    # 該当するchannel_idのチャンネル情報を取得(mchannel_id、channel_name、description)
    channel = Channel.find_by_chanenl_id(channel_id) 

    # 該当するchannel_idのmessages情報を全て取得(message_id, user_id, user_name, prefecture_name, message_txt, created_at)
    messages = Message.get_all(channel_id)

    # メッセージページ,ユーザーID, channel情報, メッセージ情報を返す
    return render_template('messages.html', user_id=user_id, channel=channel, messages=messages)

# TODO:メッセージの投稿
@app.route('/channels/<channel_id>/messages', methods=['POST'])
def create_message():
    # ログイン状態の確認
    # メッセージの取得
    # メッセージが空白でない場合は、セッセージをDBに追加
    # メッセージが空白の場合は、メッセージが空白であることをモーダルで表示

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
    app.run(host="0.0.0.0", debug=True,port=5001)  #port=5001を追記　消すこと！！！
    
