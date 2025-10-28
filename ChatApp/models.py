import pymysql
from util.DB import DB
from flask import abort

# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()


class User:
    @classmethod
    def create(cls, user_id, user_name, email, password, prefecture_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO users (user_id, user_name, email, password, prefecture_id) VALUES (%s, %s, %s, %s, %s);"
                cur.execute(sql, (user_id, user_name, email, password, prefecture_id))
                conn.commit()
        except pymysql.Error as e:
            print(
                f"ユーザーを登録できませんでした：{e}"
            )  # TODO(はるか): フロント側との調節(メッセージの内容)
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_email(cls, email):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE email=%s;"
                cur.execute(sql, (email,))
                user = cur.fetchone()
            return user
        except pymysql.Error as e:
            # TODO(はるか): フロント側との調節(メッセージの内容)
            print(f"メールアドレスが{email}のユーザーを取得できませんでした：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    # TODO(うっちーさん): チャンネルクラスを定義
    # チャンネル一覧ページの表示
    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM channels;"

                # データベース側で並び替えを指定するなら（app.pyのreverse()削除）
                # sql = SELECT * FROM ORDER BY channel_id DESC

                cur.execute(sql)
                channels = cur.fetchall()
                return channels
        except pymysql.Error as e:
            print(
                f"エラーが発生しました:{e}"
            )  # HTMLには表示されないもの　flash? 仕組み調べる
            abort(500)
        finally:
            db_pool.release(conn)


# チャンネルの作成
class Channel:
    @classmethod
    def create(cls, user_id, channel_name, description):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO channels(user_id, channel_name, description) VALUES (%s, %s, %s);"
                cur.execute(
                    sql,
                    (
                        user_id,
                        channel_name,
                        description,
                    ),
                )
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しました:{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    # チャンネルの更新
    """チャンネルIDの検索条件"""

    @classmethod
    def find_by_channel_id(cls, channel_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM channels WHERE channel_id=%s;"
                cur.execute(sql, (channel_id,))
                channel = cur.fetchone()
                return channel
        except pymysql.Error as e:
            print(f"エラーが発生しました:{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    """チャンネルの名前の検索条件"""

    @classmethod
    def find_by_channel_name(cls, channel_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM channels WHERE channel_name=%s;"
                cur.execute(sql, (channel_name,))
                channel = cur.fetchone()
                return channel
        except pymysql.Error as e:
            print(f"エラーが発生しました:{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update(cls, user_id, channel_name, description, channel_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE channels SET user_id=%s, channel_name=%s, description=%s WHERE channel_id=%s;"
                cur.execute(
                    sql,
                    (
                        user_id,
                        channel_name,
                        description,
                        channel_id,
                    ),
                )
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しました:{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    # チャンネルの削除
    @classmethod
    def delete(cls, channel_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM channels WHERE channel_id=%s;"
                cur.execute(sql, (channel_id))
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しました:{e}")
            abort(500)
        finally:
            db_pool.release(conn)


# TODO(rootさん): メッセージクラスを定義
class Message:
    # TODO: 全てのメッセージを取得
    # 選択したチャンネルのメッセージID,ユーザーID,ユーザー名,都道府県名,メッセージ,投稿日時を抽出
    @classmethod
    def get_all(cls, channel_id):
        conn = db_pool.get_conn()  # データベース接続プールからコネクションを取得
        try:
            with conn.cursor() as cur:  # カーソルオブジェクトを作成
                sql = """
                   SELECT message_id,u.user_id, u.user_name, p.prefecture_name, message_txt, created_at 
                   FROM messages AS m 
                   INNER JOIN users AS u ON m.user_id = u.user_id
                   INNER　JOIN prefectures AS p ON u.prefecture_id = p.prefecture_id 
                   WHERE channel_id = %s 
                   ORDER BY id ASC;
               """
                cur.execute(sql, (channel_id,))  # SQLを実行
                messages = cur.fetchall()  # 実行結果から全ての行を取得
                return messages
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    # TODO: メッセージの作成
    # TODO: メッセージの変更
    # TODO: メッセージの削除(追加機能)


# TODO(はるか): 都道府県クラスを定義
class Prefecture:
    pass
