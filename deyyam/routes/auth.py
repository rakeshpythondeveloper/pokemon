from flask import render_template, redirect, request, Blueprint
from deyyam.forms.forms import RegistrationForm, loginForm
from deyyam.extensions.db import db
from deyyam.models.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_login import current_user,login_user
from flask_bcrypt import Bcrypt
from deyyam.oper.oper import insert_user
bcrypt=Bcrypt()

auth_bp = Blueprint("auth", __name__)
profile_pics_folder='static/profile_pics'


@auth_bp.route("/registration", methods=["GET", "POST"])
def reg():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        profile_image=form.profile_image.data
        filename=None
        if profile_image:
            user_id=current_user.id
            filename=f"{user_id}.png"
            profile_image_path=os.path.join(profile_pics_folder,filename)
            profile_image.save(profile_image_path)
            current_user.profile_image=filename
            db.session.commit()
        if password == confirm_password:
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            insert_user(username, hashed_password,profile_image=filename)
            return redirect("/login")
        else:
            return "Passwords do not match. Please try again."
    return render_template("reg.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = loginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect('/main')
        else:
            return "Invalid username or password. Please try again."
    return render_template("login.html", form=form)