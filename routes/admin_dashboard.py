from flask import Blueprint, render_template
from models import Quote

admin_dashboard_bp = Blueprint("admin_dashboard", __name__, url_prefix="/admin")

# ✅ 대시보드 메인
@admin_dashboard_bp.route("/")
def dashboard():
    return render_template("admin/dashboard.html")

# ✅ 견적 목록: DB에서 전체 견적 불러오기
@admin_dashboard_bp.route("/quotes")
def admin_quotes():
    quotes = Quote.query.order_by(Quote.created_at.desc()).all()
    return render_template("admin/quotes.html", quotes=quotes)

# ✅ 예약 목록
@admin_dashboard_bp.route("/reservations")
def admin_reservations():
    return render_template("admin/reservations.html")

# ✅ 예약 상세 페이지
@admin_dashboard_bp.route("/reservations/<reservation_id>")
def reservation_detail(reservation_id):
    return render_template("admin/reservation_detail.html", reservation_id=reservation_id)
