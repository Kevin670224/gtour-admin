from flask import Flask, render_template, redirect
from models import db
import models

def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from routes.admin_reservation import admin_reservation_bp
    from routes.admin_dashboard import admin_dashboard_bp
    from routes.quote import quote_bp

    app.register_blueprint(admin_reservation_bp)
    app.register_blueprint(admin_dashboard_bp)
    app.register_blueprint(quote_bp)

    # 🔧 루트 경로 → /admin 으로 자동 이동
    @app.route("/")
    def home():
        return redirect("/admin")

    # 🔧 관리자 기본 라우트
    @app.route("/admin")
    def admin_home():
        return render_template("admin/dashboard.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
