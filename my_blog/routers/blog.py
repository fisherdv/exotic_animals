import os
from flask import render_template, Blueprint, request, current_app, redirect, url_for, send_from_directory
from sqlalchemy.orm import session
from my_blog.models.blog import Post, Files
from my_blog.models.blog import Post
from my_blog.moduls.database import db
from werkzeug.utils import secure_filename
from datetime import datetime


bp_blog = Blueprint("blog", __name__)


@bp_blog.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@bp_blog.route('/<int:id>')
def post(id: int):
    post = Post.query.get(id)
    return render_template('post.html', post=post)


@bp_blog.route('/edit', methods=['POST', 'GET'])
@bp_blog.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id: int = None):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        file_id = request.form['file_id']        
        if 'image' in request.files:            
            image = request.files['image']
            if image:
                filename = secure_filename(image.filename)
                hash_filename = str(abs(hash(str(datetime)+filename)))
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], hash_filename))
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
            post = Post(
                title=title,
                content=content,
                file_id=file_id,
                user_id=1
            )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.edit', id=post.id))
    else:
        post = Post.query.get(id) if id else None
        return render_template('edit.html', post=post)


@bp_blog.route('/uploads/<int:id>')
def uploaded_file(id:int):
    file = Files.query.get(id)    
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], file.path)