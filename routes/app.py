from flask import Blueprint, render_template

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/")
def admin_home():
    return render_template("admin/dashboard.html")
