from flask import Flask
from models import db
from routes.admin_quote import admin_quote_bp
import os

def create_app():
    app = Flask(__name__, template_folder='templates')
    db_path = os.path.join("/tmp", "database.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(admin_quote_bp)
    return app

app = create_app()
