from my_blog.moduls.database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False, unique=True)

    def __str__(self):
        return f"{self.username}[{self.id}]"
