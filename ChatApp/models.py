import pymysql
from util.DB import DB
from flask import abort


# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()


# TODO(はるか): ユーザークラスを定義
class User:
    @classmethod
    def create(cls, user_id, user_name, email, password, prefecture_id):
        pass


# TODO(うっちーさん): チャンネルクラスを定義
class Channel:
    # Channelsテーブルから該当するチャンネルIDの全データ(チャンネル名, ユーザーID,チャンネル名, チャンネルの詳細)を抽出
    @classmethod
    def find_by_channel_id(cls, channel_id):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT * FROM channels WHERE id=%s;"
               cur.execute(sql, (channel_id,))
               channel = cur.fetchone()
               return channel
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


# TODO(rootさん): メッセージクラスを定義
class Message:
    # TODO: 全てのメッセージを取得
    # 選択したチャンネルのメッセージID,ユーザーID,ユーザー名,都道府県名,メッセージ,投稿日時を抽出
    @classmethod
    def get_all(cls, channel_id):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = """
                   SELECT message_id,u.user_id, u.user_name, p.prefecture_name, message_txt, created_at 
                   FROM messages AS m 
                   INNER JOIN users AS u ON m.user_id = u.user_id
                   JOIN prefectures AS p ON u.prefecture_id = p.prefecture_id 
                   WHERE channel_id = %s 
                   ORDER BY id ASC;
               """
               cur.execute(sql, (channel_id,))
               messages = cur.fetchall()
               return messages
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)
    # TODO: メッセージの作成
    # TODO: メッセージの変更
    # TODO: メッセージの削除(追加機能)


# TODO(はるか): 都道府県クラスを定義
class Prefecture:
    pass
