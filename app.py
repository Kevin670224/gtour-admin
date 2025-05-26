import os
from flask import Flask
from models import db
from routes.admin_quote import quote_bp

def create_app():
    app = Flask(__name__, template_folder='templates')

    # ✅ database.db를 프로젝트 루트에 생성
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "database.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.register_blueprint(quote_bp)

    @app.route("/")
    def home():
        return "<h1>Guide4U Flask App is running!</h1>"

    return app

app = create_app()
