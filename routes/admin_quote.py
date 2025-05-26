from flask import Blueprint, render_template
from models import Quote

quote_bp = Blueprint("quote", __name__, url_prefix="/admin")

@quote_bp.route("/quotes")
def quote_list():
    quotes = Quote.query.order_by(Quote.created_at.desc()).all()
    return render_template("admin/quote_list.html", quotes=quotes)

__all__ = ['quote_bp']
