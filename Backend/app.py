print("THIS app.py IS RUNNING")
from flask import Flask, render_template, request, redirect, session, url_for, flash
from extensions import db
from werkzeug.security import check_password_hash, generate_password_hash

#.\venv\Scripts\Activate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

import models 
from models import User, Drive

with app.app_context():
    db.create_all()
    models.create_admin()

@app.route("/")
def home():
    return "Placement Portal Backend Running"

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        if user.role == "company" and not user.is_approved:
            return "Wait for admin approval"
        session["user_id"] = user.id
        session["role"] = user.role

        if user.role == "admin":
            return redirect("/admin")
        elif user.role == "student":
            return redirect("/student")
        elif user.role == "company":
            return redirect("/company")
    return "Invalid email or password"

@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return "Unauthorized access"
    return "Welcome Admin"

@app.route("/admin/companies")
def view_pending_companies():
    if "role" not in session or session["role"] != "admin":
        return "Unauthorized"
    pending = User.query.filter_by(role="company", is_approved=False).all()
    return render_template("admin_companies.html", companies=pending)

@app.route("/admin/approve_company/<int:user_id>")
def approve_company(user_id):
    if "role" not in session or session["role"] != "admin":
        return "Unauthorized"
    company = User.query.get(user_id)
    if company and company.role == "company":
        company.is_approved = True
        db.session.commit()
    return redirect("/admin/companies")

@app.route("/student")
def student_dashboard():
    if session.get("role") != "student":
        return "Unauthorized access"
    return render_template("student_dashboard.html")

@app.route("/company")
def company_dashboard():
    if "role" not in session or session["role"] != "company":
        return "Unauthorized"

    return render_template("company_dashboard.html")

@app.route("/company/create-drive", methods=["GET", "POST"])
def create_drive():
    if "role" not in session or session["role"] != "company":
        return "Unauthorized"

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        eligibility = request.form.get("eligibility")

        drive = Drive(
            company_id=session["user_id"],
            title=title,
            description=description,
            eligibility=eligibility,
            is_approved=False
        )

        db.session.add(drive)
        db.session.commit()

        return "Drive created. Waiting for admin approval."
    return render_template("create_drive.html")

@app.route("/student/register", methods =["GET","POST"])
def student_register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return"User already exists"
        
        new_student = User( email=email,password=generate_password_hash(password), role="student")
        db.session.add(new_student)
        db.session.commit()

        return redirect("/login")

    return render_template("student_register.html")

@app.route("/company/register", methods=["GET","POST"])
def company_register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        existing = User.query.filter_by(email=email).first()
        if existing :
            return "Email already registered"
        
        company = User(
            email=email,
            password = generate_password_hash(password),
            role="company",
            is_approved=False
        )
        db.session.add(company)
        db.session.commit()
        return "Company registered. Wait for admin approval"
    return render_template("company_register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

if __name__ == "__main__":
    app.run(debug=True)