from flask import render_template, redirect, request, Blueprint
from deyyam.forms.forms import RegistrationForm, loginForm
from deyyam.extensions.db import db
from deyyam.models.models import users
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = loginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
           
            return redirect('/main')
        else:
          
            return "Invalid username or password. Please try again."
    return render_template("login.html", form=form)

@auth_bp.route("/registration", methods=["GET", "POST"])
def reg():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password == confirm_password:
            hashed_password = generate_password_hash(password)
            new_user = users(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
        else:
            return "Passwords do not match. Please try again."
    return render_template("reg.html", form=form)

