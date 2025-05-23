from flask import Flask, render_template, redirect
from models import db
import os

def create_app():
    app = Flask(__name__, template_folder='templates')

    # ✅ 경로 설정 (instance/database.db 사용)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "instance", "database.db")

    # ✅ DB 연결 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ✅ DB 초기화
    db.init_app(app)

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
    app.run(debug=True)
