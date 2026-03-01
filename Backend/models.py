from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=True)

class Drive(db.Model):
    __tablename__ = "drives"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    eligibility = db.Column(db.String(100))
    is_approved = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(100))
    salary = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    company = db.relationship("User", backref="drives")

def create_admin():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(
            email ="admin@college.com",
            password = generate_password_hash("admin123"),role="admin")
        db.session.add(admin)
        db.session.commit()
        print("admin created", admin.email, admin.password)
    else:
        print("ℹAdmin already exists", admin.email, admin.password)