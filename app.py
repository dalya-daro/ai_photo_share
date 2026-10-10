from datetime import datetime
import os
from pathlib import Path
from uuid import uuid4

from flask import Flask, flash, redirect, render_template, send_from_directory, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from peewee import (
    AutoField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegrityError,
    Model,
    SqliteDatabase,
)
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf.file import FileField, FileRequired
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


PROJECT_DIRECTORY = Path(__file__).resolve().parent
POST_UPLOAD_DIRECTORY = PROJECT_DIRECTORY / "uploads" / "posts"
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
database = SqliteDatabase(PROJECT_DIRECTORY / "photo_share.db")


class BaseModel(Model):
    class Meta:
        database = database


class User(UserMixin, BaseModel):
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
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

if not app.config["SECRET_KEY"]:
    raise RuntimeError("Set the SECRET_KEY environment variable before starting the app.")

csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(check_deliverability=False), Length(max=255)],
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class PostForm(FlaskForm):
    image = FileField("Image", validators=[FileRequired()])
    caption = StringField("Caption", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Post")


def initialize_database():
    database.connect(reuse_if_open=True)
    database.create_tables([User, Post], safe=True)
    database.close()


def create_upload_directory():
    POST_UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


def build_image_filename(original_filename):
    safe_filename = secure_filename(original_filename)
    extension = Path(safe_filename).suffix.lower().lstrip(".")

    if not safe_filename or extension not in ALLOWED_IMAGE_EXTENSIONS:
        return None

    stem = Path(safe_filename).stem[:200]
    return f"{uuid4().hex}_{stem}.{extension}"


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get_or_none(User.id == int(user_id))
    except ValueError:
        return None


initialize_database()
create_upload_directory()


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


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(error):
    return "Uploaded file is too large. The maximum size is 5 MB.", 413


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()

        if User.get_or_none(User.username == username):
            form.username.errors.append("That username is already taken.")
        elif User.get_or_none(User.email == email):
            form.email.errors.append("That email address is already registered.")
        else:
            try:
                user = User.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(form.password.data),
                )
            except IntegrityError:
                flash("That username or email address is already registered.", "error")
            else:
                login_user(user)
                flash("Registration complete.", "success")
                return redirect(url_for("index"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_or_none(User.username == form.username.data.strip())
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("You are now logged in.", "success")
            return redirect(url_for("index"))

        flash("Invalid username or password.", "error")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are now logged out.", "success")
    return redirect(url_for("index"))


@app.route("/posts")
@login_required
def post_list():
    posts = Post.select(Post, User).join(User).order_by(Post.created_at.desc())
    return render_template("posts/list.html", posts=posts)


@app.route("/posts/new", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        filename = build_image_filename(form.image.data.filename)
        if filename is None:
            form.image.errors.append("Choose a PNG, JPG, JPEG, or GIF image.")
        else:
            image_path = POST_UPLOAD_DIRECTORY / filename
            form.image.data.save(image_path)
            try:
                Post.create(
                    image=filename,
                    caption=form.caption.data.strip(),
                    user=current_user,
                )
            except IntegrityError:
                image_path.unlink(missing_ok=True)
                form.image.errors.append("Could not save the image. Please try again.")
            else:
                flash("Post created.", "success")
                return redirect(url_for("post_list"))

    return render_template("posts/new.html", form=form)


@app.route("/uploads/posts/<filename>")
@login_required
def uploaded_post_image(filename):
    return send_from_directory(POST_UPLOAD_DIRECTORY, filename)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
