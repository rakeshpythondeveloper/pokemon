from deyyam.oper.oper import fetch_pokemon_by_id,update_pokemon_data
from flask import request,Blueprint,render_template,redirect,abort
from flask_login import current_user
from deyyam.models.models import Pokemon,LIKE_SE
from deyyam.forms.forms import MyForm
from deyyam.extensions.db import db
from deyyam.oper.oper import user_details
from flask_login import login_required


main_bp=Blueprint("main",__name__)

@main_bp .route("/",methods=["GET","POST"])
def index():
    return render_template("home.html")

@main_bp.route("/main", methods=["GET", "POST"])
def bondex():
    user_details1 =None
    user_id=current_user.id
    
    if request.method == "POST":
        search_term = request.form.get("search_term")
        details = Pokemon.query.filter(Pokemon.name.ilike(f'%{search_term}%')).all()
        user_details1 = user_details("username")
    else:
        details=Pokemon.query.all()
    
    pokemons= Pokemon.query.all()
    for pokemon in pokemons:
        like=LIKE_SE.query.filter_by(user_id=user_id,pokemon_id=pokemon.id)
        if like:
            pokemon.liked =True
        else:
            pokemon.liked =False
    
    return render_template("index.html", details=details,user_details1=user_details1,pokemons=pokemons)

@main_bp.route("/like")
@login_required
def like_pokemon():
    poke_id = request.args.get("id")
    if not poke_id:
        return "No id found", 400
    try:
        poke_id = int(poke_id)
    except ValueError:
        return "Invalid id", 400

    user_id = current_user.id
    like = LIKE_SE.query.filter_by(user_id=user_id, pokemon_id=poke_id).first()

    if like:
        db.session.delete(like)
    else:
        like = LIKE_SE(user_id=user_id, pokemon_id=poke_id)
        db.session.add(like)

    db.session.commit()

    return "Liked", 200


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
def delete_pokemon_data(pokemon_id):
    pokemon = fetch_pokemon_by_id(pokemon_id)
    if pokemon.user_id != current_user.id:
        abort(403)  
    likes = LIKE_SE.query.filter_by(pokemon_id=pokemon_id).all()
    for like in likes:
        db.session.delete(like)
    db.session.delete(pokemon)
    db.session.commit()
    
    
    
    return redirect("/main")