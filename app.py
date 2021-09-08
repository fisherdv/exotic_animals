from flask import Flask
from my_blog.moduls.database import db
from my_blog.routers.blog import bp_blog
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(bp_blog, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
