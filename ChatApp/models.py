import pymysql
from util.DB import DB


# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()


# TODO(はるか): ユーザークラスを定義
class User:
    @classmethod
    def create(cls, user_id, user_name, email, password, prefecture_id):
        pass


# TODO(うっちーさん): チャンネルクラスを定義


# TODO(rootさん): メッセージクラスを定義


# TODO(はるか): 都道府県クラスを定義
class Prefecture:
    pass
