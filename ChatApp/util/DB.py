import os
import pymysql
from pymysqlpool.pool import Pool


class DB:
    @classmethod
    def init_db_pool(cls):
        pool = Pool(
            # データベースホスト
            host=os.getenv("DB_HOST"),
            # データベースユーザー
            user=os.getenv("DB_USER"),
            # データベースパスワード
            password=os.getenv("DB_PASSWORD"),
            # データベース名
            database=os.getenv("DB_DATABASE"),
            # 最大コネクション数
            max_size=5,
            # 文字コード
            charset="utf8mb4",
            # カーソルクラス（辞書型でフェッチ）
            cursorclass=pymysql.cursors.DictCursor,
        )
        # コネクションプールの初期化
        pool.init()
        return pool
