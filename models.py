from sqlalchemy import MetaData, Table, Column, create_engine, Integer, String, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, joinedload

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


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(256), nullable=False, unique=True)

    def __str__(self):
        return f"{self.username}[{self.id}]"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

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
        user = User(username="Drozdov")
        user2 = User(username="Anonim")
        session.add(user)
        session.add(user2)
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
        user = session.query(User).filter(User.username.is_("Drozdov")).one_or_none()
        if not user:
            return
        tag_birds = session.query(Tags).filter_by(name="Птицы").one_or_none()
        tag_fish = session.query(Tags).filter_by(name="Рыбы").one_or_none()

        post_lira = Post(user_id=user.id, title="Макао Лира")
        post_fly_eater = Post(user_id=user.id, title="Королевский венценосный мухоед")
        post_flying_fish = Post(user_id=user.id, title="Летучая рыба")
        post_fish = Post(user_id=user.id, title="Судак")

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
        user = session.query(User).filter(User.username.is_("Drozdov")).one_or_none()
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


if __name__ == "__main__":
    metadata.create_all()
    create_users()
    create_tags()
    create_posts()
    get_data()
