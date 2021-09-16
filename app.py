from flask import Flask
from flask_migrate import Migrate
from my_blog.moduls.database import db
from my_blog.moduls.auth import login_manager
from my_blog.routers.blog import bp_blog

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["UPLOAD_FOLDER"] = "uploads"

db.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

app.register_blueprint(bp_blog, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
