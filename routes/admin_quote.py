from flask import Blueprint, render_template
from models import Quote

admin_quote_bp = Blueprint("admin_quote", __name__, url_prefix="/admin/quotes")

@admin_quote_bp.route("/")
def quote_list():
    quotes = Quote.query.order_by(Quote.created_at.desc()).all()
    return render_template("admin/quote_list.html", quotes=quotes)
