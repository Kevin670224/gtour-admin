from flask import Flask, render_template, redirect
from models import db
import os

def create_app():
    app = Flask(__name__, template_folder='templates')

    # ✅ 세션 오류 방지를 위한 SECRET_KEY 설정
    app.config['SECRET_KEY'] = 'guide4u-secret-key'

    # ✅ DB 경로 설정 및 instance 폴더 자동 생성
    base_dir = os.path.abspath(os.path.dirname(__file__))
    instance_dir = os.path.join(base_dir, "instance")
    os.makedirs(instance_dir, exist_ok=True)  # ✅ 폴더가 없으면 생성
    db_path = os.path.join(instance_dir, "database.db")

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ✅ DB 초기화 및 자동 생성
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # ✅ 블루프린트 등록
    from routes.admin_reservation import admin_reservation_bp
    from routes.admin_dashboard import admin_dashboard_bp
    from routes.quote import quote_bp
    from routes.admin_quote import admin_quote_bp
    from routes.api_product import api_product_bp

    app.register_blueprint(admin_reservation_bp)
    app.register_blueprint(admin_dashboard_bp)
    app.register_blueprint(quote_bp)
    app.register_blueprint(admin_quote_bp)
    app.register_blueprint(api_product_bp)

    # ✅ 메인 페이지 리디렉션
    @app.route("/")
    def home():
        return redirect("/admin")

    @app.route("/admin")
    def admin_home():
        return render_template("admin/dashboard.html")

    return app

# ✅ Flask 실행용 엔트리포인트
app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
