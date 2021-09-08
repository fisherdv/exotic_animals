from my_blog.moduls.database import db
from .auth import User

assoc_post_tags = db.Table(
    "post_tags",
    db.metadata,
    db.Column("tag_id", db.ForeignKey("tags.id", ondelete="CASCADE")),
    db.Column("post_id", db.ForeignKey("posts.id", ondelete="CASCADE")),
)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    user = db.relationship("User", backref="posts")
    tags = db.relationship(
        "Tags", secondary=assoc_post_tags, back_populates="posts")

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.title}[{self.id}]"


class Tags(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)

    posts = db.relationship(
        "Post", secondary=assoc_post_tags, back_populates="tags")
