from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import sys

# Configuração do caminho do sistema
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Inicialização do SQLAlchemy
db = SQLAlchemy()

# Inicialização do LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    
    # Configuração do banco de dados
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'hollywood-ai-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
    
    # Inicialização das extensões
    db.init_app(app)
    login_manager.init_app(app)
     # Importação do modelo User para o login_manager
    from src.models.auth.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    # Registro dos blueprints
    from src.routes.auth.local import auth_bp, init_auth_routes
    from src.routes.auth.social import social_bp, google_bp, facebook_bp
    from src.routes.video import video_bp
    from src.routes.main import main_bp

    # Inicializar rotas de autenticação
    init_auth_routes(db, User)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(social_bp, url_prefix='/auth/social')
    app.register_blueprint(google_bp, url_prefix='/auth/google')
    app.register_blueprint(facebook_bp, url_prefix='/auth/facebook')
    app.register_blueprint(video_bp)
    app.register_blueprint(main_bp)
    
    # Criação das tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    return app

# Aplicação principal
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
