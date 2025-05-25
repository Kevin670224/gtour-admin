from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Quote, db
from datetime import datetime, timedelta

admin_quote_bp = Blueprint("admin_quote", __name__, url_prefix="/admin")

# ✅ 견적 목록
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

# ✅ 견적 상세 보기
@admin_quote_bp.route("/quotes/<int:quote_id>")
def quote_detail(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    return render_template("admin/quote_detail.html", quote=quote)

# ✅ 견적서 작성 폼
@admin_quote_bp.route("/quotes/<int:quote_id>/write", methods=["GET", "POST"])
def create_estimate(quote_id):
    print(f"✅ create_estimate 함수 실행됨! quote_id: {quote_id}")  # 👉 로그로 경로 진입 여부 확인용
    quote = Quote.query.get_or_404(quote_id)

    if request.method == "POST":
        # 견적 상태를 "견적작성중" 또는 "발송완료"로 변경
        quote.status = "견적작성중"
        db.session.commit()
        flash("견적서가 저장되었습니다.", "success")
        return redirect(url_for("admin_quote.quote_detail", quote_id=quote.id))

    return render_template("admin/quote_estimate_write.html", quote=quote)
