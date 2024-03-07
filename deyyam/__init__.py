from flask import Flask
from deyyam.extensions.db import db
from deyyam.routes import auth,poker,main,user
from deyyam.extensions.migrate import migrate
from deyyam.extensions.login_manager import login_manager
from deyyam.models.models import User 

def blueprints(app):
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(main.main_bp)
    app.register_blueprint(poker.poker_bp)  
    app.register_blueprint(user.user_bp)
    
def load_config(app):    
    app.config['SECRET_KEY'] = "secret-key"
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://avnadmin:AVNS_0ucIPNKYt527QqAQ-Rr@mysql-a5559c2-rakeshdeveloper23-d4e6.a.aivencloud.com:28488/defaultdb"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def create_app():
    server=Flask(__name__)
    blueprints(server)
    load_config(server)
    db.init_app(server)
    migrate.init_app(server,db)
    login_manager.init_app(server)
   
    
    with server.app_context():
        db.create_all()
    @login_manager.user_loader 
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    return server