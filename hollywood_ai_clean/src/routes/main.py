from flask import Blueprint, render_template
from flask_login import login_required, current_user

# Blueprint para as páginas principais
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página inicial da aplicação."""
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard do usuário, exibindo vídeos e tarefas."""
    return render_template('dashboard.html', user=current_user)

@main_bp.route('/edit/<video_id>')
@login_required
def edit_video(video_id):
    """Página de edição de vídeo específico."""
    return render_template('edit.html', video_id=video_id)
