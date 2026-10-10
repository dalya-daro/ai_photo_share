from datetime import datetime
from pathlib import Path

from flask import Flask, render_template
from peewee import AutoField, CharField, DateTimeField, ForeignKeyField, Model, SqliteDatabase


PROJECT_DIRECTORY = Path(__file__).resolve().parent
database = SqliteDatabase(PROJECT_DIRECTORY / "photo_share.db")


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    id = AutoField()
    username = CharField(max_length=80, unique=True)
    email = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)


class Post(BaseModel):
    id = AutoField()
    image = CharField(max_length=255, unique=True)
    caption = CharField(max_length=500)
    user = ForeignKeyField(User, backref="posts")
    created_at = DateTimeField(default=datetime.now)


app = Flask(__name__)


@app.before_request
def connect_database():
    database.connect(reuse_if_open=True)


@app.teardown_appcontext
def close_database(exception=None):
    if not database.is_closed():
        database.close()


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
