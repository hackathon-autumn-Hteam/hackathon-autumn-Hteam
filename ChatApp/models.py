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
                cur.execute(sql, (user_id, user_name,
                            email, password, prefecture_id))
                conn.commit()
        except pymysql.Error as e:
            print(f"ユーザーを登録できませんでした：{e}")  # TODO(はるか): フロント側との調節(メッセージの内容)
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


# TODO(rootさん): メッセージクラスを定義


# TODO(はるか): 都道府県クラスを定義
class Prefecture:
    pass
