from flask_login import UserMixin
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    create_engine,
    Integer,
    String,
    ForeignKey,
    Text,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, joinedload
from werkzeug.security import generate_password_hash, check_password_hash

from test_data_content import post_lira_content, post_fly_eater_content, post_flying_fish_content

engine = create_engine("sqlite:///test.db")
metadata = MetaData(bind=engine)
session_factory = sessionmaker(bind=engine)
Base = declarative_base(bind=engine, metadata=metadata)
Session = scoped_session(session_factory)


assoc_post_tags = Table(
    "post_tags",
    metadata,
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE")),
    Column("post_id", ForeignKey("posts.id", ondelete="CASCADE")),
)


class Files(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    path = Column(String(256), nullable=False)


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(256), nullable=False, unique=True)
    password_hash = Column(String(100), nullable=False)

    def __str__(self):
        return f"{self.username}[{self.id}]"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    file_id = Column(Integer, ForeignKey("files.id"))
    content = Column(Text)

    user = relationship("User", backref="posts")
    tags = relationship("Tags", secondary=assoc_post_tags, back_populates="posts")

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.title}[{self.id}]"


class Tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True, nullable=False)

    posts = relationship("Post", secondary=assoc_post_tags, back_populates="tags")


def create_users():
    with Session() as session:
        user = User(username="admin")
        user.set_password("admin")
        session.add(user)
        session.commit()


def create_tags():
    with Session() as session:
        tag_birds = Tags(name="Птицы")
        tag_fish = Tags(name="Рыбы")
        tag_dogs = Tags(name="Собаки")
        session.add(tag_birds)
        session.add(tag_fish)
        session.add(tag_dogs)
        session.commit()


def create_posts():
    with Session() as session:
        user = session.query(User).filter(User.username.is_("admin")).one_or_none()
        if not user:
            return
        tag_birds = session.query(Tags).filter_by(name="Птицы").one_or_none()
        tag_fish = session.query(Tags).filter_by(name="Рыбы").one_or_none()

        post_lira = Post(user_id=user.id, title="Макао Лира", content=post_lira_content, file_id=1)
        post_fly_eater = Post(
            user_id=user.id,
            title="Королевский венценосный мухоед",
            content=post_fly_eater_content,
            file_id=2,
        )
        post_flying_fish = Post(
            user_id=user.id, title="Летучая рыба", content=post_flying_fish_content, file_id=3
        )
        post_fish = Post(user_id=user.id, title="Судак", content="content")

        post_lira.tags.append(tag_birds)
        post_fly_eater.tags.append(tag_birds)

        post_flying_fish.tags = [tag_birds, tag_fish]

        post_fish.tags.append(tag_fish)

        session.add(post_lira)
        session.add(post_flying_fish)
        session.add(post_fly_eater)
        session.add(post_fish)
        session.commit()


def get_data():
    with Session() as session:
        user = session.query(User).filter(User.username.is_("admin")).one_or_none()
        print(f"Посты пользователя {user}")
        print(user.posts)
        print(f"Посты в которых количество тегов >= 2")
        posts = (
            session.query(Post)
            .join(Tags, Post.tags)
            .group_by(Post.id)
            .having(func.count(Post.id) >= 2)
            .all()
        )
        print(posts)


def create_files():
    with Session() as session:
        session.add(Files(path="5947105410838670489"))
        session.add(Files(path="8248503583728734229"))
        session.add(Files(path="3636630980591593186"))
        session.commit()


if __name__ == "__main__":
    metadata.create_all()
    create_files()
    create_users()
    create_tags()
    create_posts()
    get_data()
