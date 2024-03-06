from deyyam.oper.oper import fetch_pokemon_by_id,update_pokemon_data
import os
from PIL import Image
from io import BytesIO
import requests
from flask import request,Blueprint,render_template,redirect
from deyyam.models.models import Pokemon
from deyyam.forms.forms import MyForm
from deyyam.extensions.db import db
from deyyam.oper.oper import save_image

main_bp=Blueprint("main",__name__)

@main_bp .route("/",methods=["GET","POST"])
def index():
    return render_template("home.html")

@main_bp.route("/main", methods=["GET", "POST"])
def bondex():
    if request.method == "POST":
        search_term = request.form.get("search_term")
        details = Pokemon.query.filter(Pokemon.name.ilike(f'%{search_term}%')).all()
    else:
        details = Pokemon.query.all()
    
    return render_template("index.html", details=details)



@main_bp.route("/update/<int:pokemon_id>", methods=["GET", "POST"])
def update(pokemon_id):
    form = MyForm()
    existing_data = fetch_pokemon_by_id(pokemon_id)

    if request.method == "POST" and form.validate_on_submit():
        update_pokemon_data(pokemon_id, form)
        return redirect("/main")

    form.name.data = existing_data.name
    form.image_url.data = existing_data.image_url
    form.description.data = existing_data.description
    form.height.data = existing_data.height
    form.weight.data = existing_data.weight
    form.category.data = existing_data.category
    form.abilities.data = existing_data.abilities

    return render_template("update.html", form=form, existing_data=existing_data)


@main_bp.route("/delete/<int:pokemon_id>", methods=["POST"])
def delete(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    db.session.delete(pokemon)
    db.session.commit()
    return redirect("/main")