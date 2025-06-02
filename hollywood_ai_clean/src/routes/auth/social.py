from flask import Blueprint, redirect, url_for, session, request, jsonify
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_login import login_user, current_user
from src.models.auth.user import User
from src.main import db
import os

# Configurações para Google OAuth
google_bp = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_CLIENT_ID", "seu-client-id-google"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", "seu-client-secret-google"),
    scope=["profile", "email"],
    redirect_to="social.google_callback"
)

# Configurações para Facebook OAuth
facebook_bp = make_facebook_blueprint(
    client_id=os.environ.get("FACEBOOK_CLIENT_ID", "seu-client-id-facebook"),
    client_secret=os.environ.get("FACEBOOK_CLIENT_SECRET", "seu-client-secret-facebook"),
    scope=["email"],
    redirect_to="social.facebook_callback"
)

social_bp = Blueprint('social', __name__)

@social_bp.route('/login/google')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    return redirect(url_for('social.google_callback'))

@social_bp.route('/callback/google')
def google_callback():
    if not google.authorized:
        return redirect(url_for('auth.login'))
    
    resp = google.get('/oauth2/v2/userinfo')
    if resp.ok:
        google_info = resp.json()
        google_id = google_info['id']
        email = google_info.get('email')
        name = google_info.get('name')
        
        # Verifica se o usuário já existe
        user = User.query.filter_by(google_id=google_id).first()
        if not user:
            # Verifica se existe um usuário com o mesmo email
            user = User.query.filter_by(email=email).first()
            if user:
                # Atualiza o usuário existente com o google_id
                user.google_id = google_id
            else:
                # Cria um novo usuário
                user = User(
                    name=name,
                    email=email,
                    google_id=google_id
                )
                db.session.add(user)
            
            db.session.commit()
        
        login_user(user)
        return redirect(url_for('main.index'))
    
    return redirect(url_for('auth.login'))

@social_bp.route('/login/facebook')
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for('facebook.login'))
    return redirect(url_for('social.facebook_callback'))

@social_bp.route('/callback/facebook')
def facebook_callback():
    if not facebook.authorized:
        return redirect(url_for('auth.login'))
    
    resp = facebook.get('/me?fields=id,name,email')
    if resp.ok:
        facebook_info = resp.json()
        facebook_id = facebook_info['id']
        email = facebook_info.get('email')
        name = facebook_info.get('name')
        
        # Verifica se o usuário já existe
        user = User.query.filter_by(facebook_id=facebook_id).first()
        if not user:
            # Verifica se existe um usuário com o mesmo email
            user = User.query.filter_by(email=email).first()
            if user:
                # Atualiza o usuário existente com o facebook_id
                user.facebook_id = facebook_id
            else:
                # Cria um novo usuário
                user = User(
                    name=name,
                    email=email,
                    facebook_id=facebook_id
                )
                db.session.add(user)
            
            db.session.commit()
        
        login_user(user)
        return redirect(url_for('main.index'))
    
    return redirect(url_for('auth.login'))

# API endpoints para autenticação social
@social_bp.route('/api/auth/login/google')
def api_google_login():
    return redirect(url_for('google.login'))

@social_bp.route('/api/auth/login/facebook')
def api_facebook_login():
    return redirect(url_for('facebook.login'))

@social_bp.route('/api/auth/callback/google')
def api_google_callback():
    if not google.authorized:
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    resp = google.get('/oauth2/v2/userinfo')
    if resp.ok:
        google_info = resp.json()
        google_id = google_info['id']
        email = google_info.get('email')
        name = google_info.get('name')
        
        # Verifica se o usuário já existe
        user = User.query.filter_by(google_id=google_id).first()
        if not user:
            # Verifica se existe um usuário com o mesmo email
            user = User.query.filter_by(email=email).first()
            if user:
                # Atualiza o usuário existente com o google_id
                user.google_id = google_id
            else:
                # Cria um novo usuário
                user = User(
                    name=name,
                    email=email,
                    google_id=google_id
                )
                db.session.add(user)
            
            db.session.commit()
        
        login_user(user)
        return jsonify({'success': True, 'user': {'id': user.id, 'name': user.name, 'email': user.email}})
    
    return jsonify({'success': False, 'message': 'Falha na autenticação'}), 401

@social_bp.route('/api/auth/callback/facebook')
def api_facebook_callback():
    if not facebook.authorized:
        return jsonify({'success': False, 'message': 'Não autorizado'}), 401
    
    resp = facebook.get('/me?fields=id,name,email')
    if resp.ok:
        facebook_info = resp.json()
        facebook_id = facebook_info['id']
        email = facebook_info.get('email')
        name = facebook_info.get('name')
        
        # Verifica se o usuário já existe
        user = User.query.filter_by(facebook_id=facebook_id).first()
        if not user:
            # Verifica se existe um usuário com o mesmo email
            user = User.query.filter_by(email=email).first()
            if user:
                # Atualiza o usuário existente com o facebook_id
                user.facebook_id = facebook_id
            else:
                # Cria um novo usuário
                user = User(
                    name=name,
                    email=email,
                    facebook_id=facebook_id
                )
                db.session.add(user)
            
            db.session.commit()
        
        login_user(user)
        return jsonify({'success': True, 'user': {'id': user.id, 'name': user.name, 'email': user.email}})
    
    return jsonify({'success': False, 'message': 'Falha na autenticação'}), 401
