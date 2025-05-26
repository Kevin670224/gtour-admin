from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class Quote(db.Model):
    __tablename__ = "quotes"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

    adults = db.Column(db.Integer)
    children = db.Column(db.Integer)
    infants = db.Column(db.Integer)

    country = db.Column(db.String(100))
    region = db.Column(db.String(100))
    product = db.Column(db.String(100))

    travel_start = db.Column(db.String(20))
    travel_end = db.Column(db.String(20))

    flight_status = db.Column(db.String(50))
    departure_flight = db.Column(db.String(100))
    return_flight = db.Column(db.String(100))
    departure_time = db.Column(db.String(50))
    return_time = db.Column(db.String(50))

    resort_status = db.Column(db.String(50))
    resort_name = db.Column(db.String(100))
    resort_styles = db.Column(db.String(200))

    extra_request = db.Column(db.Text)
    status = db.Column(db.String(50), default="견적요청")
