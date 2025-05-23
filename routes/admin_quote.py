from flask import Blueprint, render_template, request
from models import Quote
from datetime import datetime, timedelta

admin_quote_bp = Blueprint("admin_quote", __name__, url_prefix="/admin")

@admin_quote_bp.route("/quotes")
def admin_quotes():
    status = request.args.get("status", "")
    keyword = request.args.get("keyword", "")
    date = request.args.get("date", "")

    # 🔍 기본 검색 쿼리: 삭제된 견적은 제외
    query = Quote.query.filter(Quote.status != "견적삭제 (휴지통)")

    if status:
        query = query.filter(Quote.status == status)

    if keyword:
        query = query.filter(Quote.customer_name.contains(keyword))

    if date:
        try:
            selected_date = datetime.strptime(date, "%Y-%m-%d").date()
            next_date = selected_date + timedelta(days=1)
            query = query.filter(
                Quote.created_at >= selected_date,
                Quote.created_at < next_date
            )
        except:
            pass

    quotes = query.order_by(Quote.created_at.desc()).all()

    # ✅ 결과가 없을 경우 → 휴지통 상태에서 동일 조건으로 다시 검색
    if not quotes:
        trash_query = Quote.query.filter(Quote.status == "견적삭제 (휴지통)")

        if keyword:
            trash_query = trash_query.filter(Quote.customer_name.contains(keyword))

        if date:
            try:
                selected_date = datetime.strptime(date, "%Y-%m-%d").date()
                next_date = selected_date + timedelta(days=1)
                trash_query = trash_query.filter(
                    Quote.created_at >= selected_date,
                    Quote.created_at < next_date
                )
            except:
                pass

        quotes = trash_query.order_by(Quote.created_at.desc()).all()

    return render_template("admin/quotes.html", quotes=quotes)
