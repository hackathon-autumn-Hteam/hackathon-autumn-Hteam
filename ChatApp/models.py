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
            print(f"ユーザーを登録できませんでした：{e}")
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
            print(f"メールアドレスが{email}のユーザーを取得できませんでした：{e}")
            abort(500)
        finally:
            db_pool.release(conn)


# チャンネルの作成
class Channel:
    # TODO(うっちーさん): チャンネルクラスを定義
    # チャンネル一覧ページの表示
    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                # sql = "SELECT * FROM channels;"

                # データベース側で並び替えを指定するなら（app.pyのreverse()削除）
                sql = "SELECT * FROM channels ORDER BY channel_id DESC;"

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


class Message:
    # 選択したチャンネルのメッセージID,ユーザーID,ユーザー名,都道府県名,メッセージ,投稿日時を抽出
    @classmethod
    def get_all(cls, channel_id):
        conn = db_pool.get_conn()  # データベース接続プールからコネクションを取得
        try:
            with conn.cursor() as cur:  # カーソルオブジェクトを作成
                sql = """
                   SELECT m.message_id, u.user_id, u.user_name, p.prefecture_name, m.message_text, m.created_at, m.like_flower_count
                   FROM messages AS m
                   INNER JOIN users AS u ON m.user_id = u.user_id
                   INNER JOIN prefectures AS p ON u.prefecture_id = p.prefecture_id
                   WHERE channel_id = %s
                   ORDER BY m.message_id ASC;
                """
                cur.execute(sql, (channel_id,))  # SQLを実行
                messages = cur.fetchall()  # 実行結果から全ての行を取得
                return messages
        except pymysql.Error as e:
            print(f"Message.get_allでエラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_message_id(cls, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM messages WHERE message_id=%s;"
                cur.execute(sql, (message_id,))
                message = cur.fetchone()
                return message
        except pymysql.Error as e:
            print(f"Message.find_by_message_isでエラーが発生しました:{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def create(cls, user_id, channel_id, message_text):
        conn = db_pool.get_conn()  # データベース接続プールからコネクションを取得
        try:
            with conn.cursor() as cur:  # カーソルオブジェクトを作成
                # messagesテーブルにユーザーID,チャンネルID,メッセージ詳細を挿入
                sql = "INSERT INTO messages(user_id, channel_id, message_text) VALUES(%s, %s, %s);"
                cur.execute(
                    sql,
                    (
                        user_id,
                        channel_id,
                        message_text,
                    ),
                )  # SQLを実行
                conn.commit()
        except pymysql.Error as e:
            print(f"Message.createでエラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update(cls, message_id, message_text):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:  # 該当するmessage_idのmessage_textを更新
                sql = "UPDATE messages SET message_text=%s WHERE message_id=%s;"
                cur.execute(sql, (message_text, message_id))  # SQLを実行
                conn.commit()
        except pymysql.Error as e:
            print(f"Message.updateでエラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def send_flower(cls, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE messages SET like_flower_count = like_flower_count + 1 WHERE message_id=%s;"
                cur.execute(sql, (message_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f"お花を送れませんでした：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    # TODO: メッセージの削除(追加機能)
    @classmethod
    def delete(cls, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM messages WHERE message_id=%s;"
                cur.execute(sql, (message_id))
                conn.commit()
        except pymysql.Error as e:
            print(f"Message.deleteでエラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)


class Mypage:
    # マイページの表示と更新
    # 該当するユーザーの情報取得
    @classmethod
    def get_all(cls, user_id):
        conn = db_pool.get_conn()  # データベース接続プールからコネクションを取得
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE user_id=%s;"
                cur.execute(sql, (user_id,))
                user = cur.fetchone()
            return user
        except pymysql.Error as e:
            print(f"ユーザーIDが{user_id}のユーザー情報を取得できませんでした：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update(cls, user_id, prefecture_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:  # 該当するuser_idのprefecture_idを更新
                sql = "UPDATE users SET prefecture_id=%s WHERE user_id=%s;"
                cur.execute(sql, (prefecture_id, user_id))  # SQLを実行
                conn.commit()
        except pymysql.Error as e:
            print(f"Mypage.updateでエラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

# 追加機能「励ましのメッセージ」
# ORDER BY RAND() 遅くなりがち（データが多い時注意）
class SupportMessage:
    @classmethod
    def get_random_by_hour(cls, hour: int):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                      SELECT support_message_text
                      FROM support_messages
                      WHERE hour = %s
                      ORDER BY RAND()
                      LIMIT 1;
                """
                cur.execute(sql, (hour,))
                support_messages = cur.fetchone()
                return (
                    support_messages["support_message_text"]
                    if support_messages
                    else None
                )
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

class Prefecture:
    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM prefectures;"
                cur.execute(sql)
                prefectures = cur.fetchall()
                return prefectures
        except pymysql.Error as e:
            print(f"都道府県の一覧を取得できませんでした:{e}")
            abort(500)
        finally:
            db_pool.release(conn)


# 追加機能「励ましのメッセージ」
# ORDER BY RAND() 遅くなりがち（データが多い時注意）
class SupportMessage:
    @classmethod
    def get_random_by_hour(cls, hour: int):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                      SELECT support_message_text
                      FROM support_messages
                      WHERE hour = %s
                      ORDER BY RAND()
                      LIMIT 1;
                """
                cur.execute(sql, (hour,))
                support_messages = cur.fetchone()
                return (
                    support_messages["support_message_text"]
                    if support_messages
                    else None
                )
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)
