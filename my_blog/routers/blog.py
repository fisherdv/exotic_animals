from flask import render_template, Blueprint
from my_blog.models.blog import Post

bp_blog = Blueprint("blog", __name__)


@bp_blog.route('/')
def index():
    return render_template('index.html')


@bp_blog.route('/<int:id>')
def post(id: int):
    print(Post.query.all())
    return render_template('post.html')


@bp_blog.route('/edit')
@bp_blog.route('/edit/<int:id>')
def edit(id: int = None):
    return render_template('edit.html')
