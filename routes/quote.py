from flask import Blueprint, render_template, request, redirect, flash
from models import db, Quote
from datetime import datetime

quote_bp = Blueprint('quote', __name__, url_prefix="/quote")

# ✅ 고객 맞춤 견적 요청 폼 표시
@quote_bp.route("/")
def show_quote_form():
    return render_template("quote_form.html")

# ✅ 고객 견적 요청 제출 처리
@quote_bp.route("/submit", methods=["POST"])
def submit_quote():
    today_str = datetime.today().strftime("%Y%m%d")
    today_quotes = Quote.query.filter(Quote.quote_number.like(f"Q{today_str}-%")).count() + 1
    quote_number = f"Q{today_str}-{str(today_quotes).zfill(3)}"

    travel_period = request.form.get("travel_period", "").split("~")
    start_date = travel_period[0].strip() if len(travel_period) > 0 else None
    end_date = travel_period[1].strip() if len(travel_period) > 1 else None

    new_quote = Quote(
        quote_number=quote_number,
        customer_name=request.form.get("customer_name"),
        phone=request.form.get("phone"),
        email=request.form.get("email"),

        country=request.form.get("country"),
        region=request.form.get("region"),
        product=request.form.get("product"),
        product_name=request.form.get("product_name"),
        destination=request.form.get("custom_destination"),

        travel_period=request.form.get("travel_period"),
        start_date=start_date,
        end_date=end_date,

        adult=int(request.form.get("adult") or 0),
        child=int(request.form.get("child") or 0),
        infant=int(request.form.get("infant") or 0),

        flight_status=request.form.get("flight_status"),
        flight_detail=request.form.get("flight_detail"),

        resort_status=request.form.get("resort_status"),
        resort_name=request.form.get("resort_name"),
        resort_style=", ".join(request.form.getlist("resort_style")),

        requirements=request.form.get("notes")
    )

    try:
        db.session.add(new_quote)
        db.session.commit()
        flash("✅ 맞춤 견적 요청이 성공적으로 접수되었습니다!", "success")
    except Exception as e:
        print("❌ 저장 오류:", e)
        flash("⚠️ 저장 중 오류가 발생했습니다.", "danger")

    return redirect("/quote")

# ✅ 관리자 견적 작성(수정) 폼
@quote_bp.route("/admin/quotes/<int:quote_id>/edit", methods=["GET", "POST"])
def edit_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)

    if request.method == "POST":
        quote.email = request.form.get("email")
        quote.product_name = request.form.get("product_name")
        quote.travel_period = request.form.get("travel_period")
        quote.flight_status = request.form.get("flight_status")
        quote.flight_detail = request.form.get("flight_detail")
        quote.resort_status = request.form.get("resort_status")
        quote.resort_style = ", ".join(request.form.getlist("resort_style"))
        quote.resort_name = request.form.get("resort_name")
        quote.requirements = request.form.get("requirements")
        quote.status = "상담중"  # 상태 자동 변경

        try:
            db.session.commit()
            flash("✅ 견적서가 성공적으로 저장되었습니다!", "success")
        except Exception as e:
            print("❌ 수정 오류:", e)
            flash("⚠️ 저장 중 오류가 발생했습니다.", "danger")

        return redirect(f"/quote/admin/quotes/{quote_id}/edit")

    return render_template("admin/quote_edit.html", quote=quote)
