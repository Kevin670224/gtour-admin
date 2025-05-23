from flask import Blueprint, render_template, request, redirect, flash
from models import db, Quote
from datetime import datetime

quote_bp = Blueprint('quote', __name__, url_prefix="/quote")

@quote_bp.route("/")
def show_quote_form():
    return render_template("quote_form.html")

@quote_bp.route("/submit", methods=["POST"])
def submit_quote():
    # ✅ 견적번호 생성 (예: Q20250523-001)
    today_str = datetime.today().strftime("%Y%m%d")
    today_quotes = Quote.query.filter(Quote.quote_number.like(f"Q{today_str}-%")).count() + 1
    quote_number = f"Q{today_str}-{str(today_quotes).zfill(3)}"

    # ✅ 여행기간 처리 (폼에서는 "~" 또는 " ~ " 기준으로 입력)
    travel_period = request.form.get("travel_period", "").split("~")
    start_date = travel_period[0].strip() if len(travel_period) > 0 else None
    end_date = travel_period[1].strip() if len(travel_period) > 1 else None

    # ✅ 새로운 Quote 객체 생성
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
