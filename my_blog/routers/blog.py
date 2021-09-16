import os
from flask import (
    render_template,
    Blueprint,
    request,
    current_app,
    redirect,
    url_for,
    send_from_directory,
)
from my_blog.models.blog import Post, Files, User
from my_blog.moduls.database import db
from werkzeug.utils import secure_filename
from datetime import datetime
from my_blog.moduls.auth import login_manager
from flask_login import login_required, login_user, logout_user

bp_blog = Blueprint("blog", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@bp_blog.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("blog.index"))


@bp_blog.route("/", methods=["post", "get"])
def index():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.session.query(User).filter(User.username == username).first()
        if user and user.check_password(password):
            login_user(user)
        else:
            message = "Неверный логин / пароль"
    posts = Post.query.all()
    return render_template("index.html", posts=posts, message=message)


@bp_blog.route("/<int:id>")
def post(id: int):
    post = Post.query.get(id)
    return render_template("post.html", post=post)


@bp_blog.route("/edit", methods=["POST", "GET"])
@bp_blog.route("/edit/<int:id>", methods=["POST", "GET"])
@login_required
def edit(id: int = None):
    if request.method == "POST":
        if request.form.get("delete"):
            Post.query.filter_by(id=id).delete()
            db.session.commit()
            return redirect(url_for("blog.index"))
        title = request.form["title"]
        content = request.form["content"]
        file_id = request.form["file_id"]
        if "image" in request.files:
            image = request.files["image"]
            if image:
                filename = secure_filename(image.filename)
                hash_filename = str(abs(hash(str(datetime) + filename)))
                image.save(os.path.join(current_app.config["UPLOAD_FOLDER"], hash_filename))
                file = Files(path=hash_filename)
                db.session.add(file)
                db.session.commit()
                file_id = file.id
        if id:
            post = Post.query.get(id)
            post.title = title
            post.content = content
            post.file_id = file_id
        else:
            post = Post(title=title, content=content, file_id=file_id, user_id=1)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("blog.edit", id=post.id))
    else:
        post = Post.query.get(id) if id else None
        return render_template("edit.html", post=post)


@bp_blog.route("/uploads/<int:id>")
def uploaded_file(id: int):
    file = Files.query.get(id)
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], file.path)
