from flask import Flask
from datetime import timedelta
import os
import uuid


# 定数定義
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)


if __name__ == "__main__":
    app.run()
