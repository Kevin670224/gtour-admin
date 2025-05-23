from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Product

admin_product_bp = Blueprint("admin_product", __name__, url_prefix="/admin/products")

@admin_product_bp.route("/create", methods=["GET", "POST"])
def create_product():
    if request.method == "POST":
        country = request.form.get("country")
        region = request.form.get("region")
        name = request.form.get("name")

        if not country or not region or not name:
            flash("모든 항목을 입력해 주세요.", "danger")
            return render_template("admin/product_create.html")

        new_product = Product(country=country, region=region, name=name)
        db.session.add(new_product)
        db.session.commit()
        flash("✅ 상품이 성공적으로 등록되었습니다!", "success")
        return redirect(url_for("admin_product.create_product"))

    return render_template("admin/product_create.html")
