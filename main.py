from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ 모델 정의
# -----------------------------
class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    quote_no = db.Column(db.String(20), unique=True, nullable=False)
    reservation_no = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    manager = db.Column(db.String(50))
    destination = db.Column(db.String(100))
    product_name = db.Column(db.String(100))
    departure_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    total_people = db.Column(db.Integer)
    status = db.Column(db.String(20), default='pending')
    memo = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    flight_status = db.Column(db.String(50))
    departure_time = db.Column(db.String(20))
    return_time = db.Column(db.String(20))
    adult = db.Column(db.Integer)
    child = db.Column(db.Integer)
    infant = db.Column(db.Integer)
    resort_status = db.Column(db.String(50))
    resort_styles = db.Column(db.String(100))
    resort_name = db.Column(db.String(100))
    resort_request = db.Column(db.Text)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        now_str = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        self.quote_no = f"Q{now_str}{str(uuid.uuid4().hex)[:4].upper()}"
        self.reservation_no = f"R{now_str}{str(uuid.uuid4().hex)[:4].upper()}"


class Quote(db.Model):
    __tablename__ = 'quotes'

    id = db.Column(db.Integer, primary_key=True)
    quote_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    country = db.Column(db.String(50))
    region = db.Column(db.String(50))
    product = db.Column(db.String(100))
    product_name = db.Column(db.String(100))
    travel_period = db.Column(db.String(50))
    adult_count = db.Column(db.Integer)
    child_count = db.Column(db.Integer)
    infant_count = db.Column(db.Integer)
    flight_status = db.Column(db.String(50))
    flight_detail = db.Column(db.String(100))
    resort_status = db.Column(db.String(50))
    resort_name = db.Column(db.String(100))
    resort_style = db.Column(db.String(100))
    requirements = db.Column(db.Text)
    status = db.Column(db.String(50), default="견적요청")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ✅ quote 라우트 불러오기
from routes.quote import quote_bp
app.register_blueprint(quote_bp)

# ✅ Flask 앱 실행
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
