from flask import Flask, render_template
from models import db
from routes.app import admin_bp
from routes.admin_quote import admin_quote_bp

def create_app():
    app = Flask(__name__, template_folder='templates')

    # ✅ DB 경로 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ✅ DB 초기화
    db.init_app(app)

    # ✅ 블루프린트 등록
    app.register_blueprint(admin_bp)
    app.register_blueprint(admin_quote_bp)

    return app

# ✅ Render 배포용 실행 조건
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
