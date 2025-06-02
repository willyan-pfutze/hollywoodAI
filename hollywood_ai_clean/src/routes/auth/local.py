from flask import Blueprint, request, redirect, url_for, flash, render_template, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)
def init_auth_routes(db, User):
    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            user = User.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash('Credenciais inválidas. Por favor, tente novamente.')
        
        return render_template('auth/login.html')

    @auth_bp.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            
            user = User.query.filter_by(email=email).first()
            
            if user:
                flash('Email já cadastrado. Por favor, faça login.')
                return redirect(url_for('auth.login'))
            
            new_user = User(
                name=name,
                email=email,
                password=generate_password_hash(password)
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user)
            return redirect(url_for('main.index'))
        
        return render_template('auth/signup.html')

    @auth_bp.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('main.index'))

    # API endpoints para autenticação
    @auth_bp.route('/api/auth/login/local', methods=['POST'])
    def api_login_local():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'success': True, 'user': {'id': user.id, 'name': user.name, 'email': user.email}})
        else:
            return jsonify({'success': False, 'message': 'Credenciais inválidas'}), 401

    @auth_bp.route('/api/auth/signup/local', methods=['POST'])
    def api_signup_local():
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            return jsonify({'success': False, 'message': 'Email já cadastrado'}), 400
        
        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password)
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return jsonify({'success': True, 'user': {'id': new_user.id, 'name': new_user.name, 'email': new_user.email}})

    @auth_bp.route('/api/auth/status')
    def api_auth_status():
        if current_user.is_authenticated:
            return jsonify({
                'authenticated': True, 
                'user': {
                    'id': current_user.id, 
                    'name': current_user.name, 
                    'email': current_user.email
                }
            })
        else:
            return jsonify({'authenticated': False})
