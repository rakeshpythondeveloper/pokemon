from flask import Blueprint,render_template,jsonify,redirect,request,current_app
from deyyam.forms.forms import RegistrationForm
from flask_login import current_user,login_required
import os
from deyyam.extensions.db import db
from deyyam.models import LIKE_SE,Pokemon
from werkzeug.utils import secure_filename


user_bp=Blueprint("user",__name__)

profile_pics_folder='static/profile_pics'

@user_bp.route("/profile")
def profile():
    filename=None
    form=RegistrationForm()
    if current_user.is_authenticated:
        user_id=current_user.id
        profile_image=form.profile_image.data
        user_pokemons=Pokemon.query.filter_by(user_id=user_id).all()
        filename=None
        if profile_image:
            filename=f"{user_id}.png"
            profile_image_path=os.path.join(profile_pics_folder,filename)
            profile_image.save(profile_image_path)
            current_user.profile_image=filename
            db.session.commit()
        else:
            filename=f"{user_id}.png"
            current_user.profile_image=filename
            db.session.commit()
    total_likes=LIKE_SE.query.join(Pokemon).filter(Pokemon.user_id==current_user.id).count()
    return render_template("profile.html",profile_image_url=filename,total_likes=total_likes,user_pokemons=user_pokemons)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@user_bp.route('/upload_profile_image', methods=['POST'])
@login_required
def upload_profile_image():
    try:
        if 'profile_image' not in request.files:
            return jsonify({'success': False, 'message': 'No file part'}), 400
        
        file = request.files['profile_image']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No selected file'}), 400   
        if file:
            filename = secure_filename(f"{current_user.id}.png")
            file_path = os.path.join(current_app.root_path, 'static', 'profile_pics', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(file.read())
            current_user.profile_image = filename
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'File uploaded successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to upload profile image'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500