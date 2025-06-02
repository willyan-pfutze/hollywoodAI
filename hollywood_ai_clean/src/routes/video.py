from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_login import login_required, current_user
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
import subprocess

# Configurações para upload de vídeo
UPLOAD_FOLDER = 'src/static/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'mkv'}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB

# Verifica se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Blueprint para upload e processamento de vídeo
video_bp = Blueprint('video', __name__)

@video_bp.route('/api/upload', methods=['POST'])
@login_required
def upload_video():
    # Verifica se há arquivo na requisição
    if 'video' not in request.files:
        return jsonify({'success': False, 'message': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['video']
    
    # Verifica se o arquivo tem nome
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Nenhum arquivo selecionado'}), 400
    
    # Verifica se o arquivo é permitido
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Formato de arquivo não suportado'}), 400
    
    # Cria um nome único para o arquivo
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    
    # Cria o diretório de upload se não existir
    user_upload_folder = os.path.join(current_app.root_path, UPLOAD_FOLDER, str(current_user.id))
    os.makedirs(user_upload_folder, exist_ok=True)
    
    # Salva o arquivo
    file_path = os.path.join(user_upload_folder, unique_filename)
    file.save(file_path)
    
    # Aqui você pode adicionar o registro do vídeo no banco de dados
    # video = Video(user_id=current_user.id, filename=unique_filename, original_filename=filename, ...)
    # db.session.add(video)
    # db.session.commit()
    
    video_id = str(uuid.uuid4())
    
    return jsonify({
        'success': True, 
        'message': 'Vídeo enviado com sucesso',
        'video': {
            'id': video_id,
            'filename': unique_filename,
            'original_filename': filename,
            'upload_date': datetime.utcnow().isoformat(),
            'status': 'uploaded'
        }
    })

@video_bp.route('/api/videos/<video_id>/edit', methods=['POST'])
@login_required
def edit_video(video_id):
    # Recebe o prompt de edição
    data = request.get_json()
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({'success': False, 'message': 'Prompt de edição não fornecido'}), 400
    
    # Aqui você implementaria a lógica para processar o vídeo com base no prompt
    # Por exemplo, analisar o prompt para identificar comandos de corte, adição de texto, filtros, etc.
    # E então usar FFmpeg ou outra biblioteca para aplicar essas edições
    
    # Por enquanto, apenas simularemos o processamento
    task_id = str(uuid.uuid4())
    
    # Salvar o prompt e o ID da tarefa para referência futura
    task_file = os.path.join(current_app.root_path, UPLOAD_FOLDER, str(current_user.id), f"{video_id}_task.txt")
    with open(task_file, 'w') as f:
        f.write(f"Task ID: {task_id}\nPrompt: {prompt}\nStatus: processing\n")
    
    return jsonify({
        'success': True,
        'message': 'Solicitação de edição recebida',
        'task': {
            'id': task_id,
            'video_id': video_id,
            'prompt': prompt,
            'status': 'processing',
            'created_at': datetime.utcnow().isoformat()
        }
    })

@video_bp.route('/api/videos/<video_id>/status', methods=['GET'])
@login_required
def video_status(video_id):
    # Verificar se existe um arquivo de tarefa para este vídeo
    task_file = os.path.join(current_app.root_path, UPLOAD_FOLDER, str(current_user.id), f"{video_id}_task.txt")
    
    if os.path.exists(task_file):
        # Simular progresso baseado no tempo desde a criação do arquivo
        file_age = datetime.utcnow().timestamp() - os.path.getmtime(task_file)
        
        # Simular conclusão após 30 segundos
        if file_age > 30:
            # Atualizar o arquivo de tarefa para concluído
            with open(task_file, 'r') as f:
                lines = f.readlines()
            
            with open(task_file, 'w') as f:
                for line in lines:
                    if line.startswith('Status:'):
                        f.write('Status: completed\n')
                    else:
                        f.write(line)
            
            return jsonify({
                'success': True,
                'status': 'completed',
                'progress': 100,
                'message': 'Edição concluída com sucesso!'
            })
        else:
            # Calcular progresso baseado no tempo decorrido (0-100%)
            progress = min(int((file_age / 30) * 100), 99)
            
            return jsonify({
                'success': True,
                'status': 'processing',
                'progress': progress,
                'message': 'Processando edições...'
            })
    else:
        return jsonify({
            'success': False,
            'message': 'Tarefa não encontrada'
        }), 404

@video_bp.route('/api/videos/<video_id>/download', methods=['GET'])
@login_required
def download_video(video_id):
    # Verificar se o vídeo foi processado
    task_file = os.path.join(current_app.root_path, UPLOAD_FOLDER, str(current_user.id), f"{video_id}_task.txt")
    
    if not os.path.exists(task_file):
        return jsonify({
            'success': False,
            'message': 'Vídeo não encontrado'
        }), 404
    
    # Verificar status da tarefa
    with open(task_file, 'r') as f:
        content = f.read()
    
    if 'Status: completed' not in content:
        return jsonify({
            'success': False,
            'message': 'Vídeo ainda não foi processado completamente'
        }), 400
    
    # Em uma implementação real, você teria o vídeo editado salvo
    # Por enquanto, vamos simular fornecendo o caminho para o vídeo original
    
    # Encontrar o arquivo de vídeo original
    user_upload_folder = os.path.join(current_app.root_path, UPLOAD_FOLDER, str(current_user.id))
    video_files = [f for f in os.listdir(user_upload_folder) if f.endswith(tuple(ALLOWED_EXTENSIONS)) and not f.startswith('edited_')]
    
    if not video_files:
        return jsonify({
            'success': False,
            'message': 'Arquivo de vídeo não encontrado'
        }), 404
    
    # Criar um "vídeo editado" (na verdade, apenas uma cópia do original)
    original_video = os.path.join(user_upload_folder, video_files[0])
    edited_video_name = f"edited_{video_id}.mp4"
    edited_video_path = os.path.join(user_upload_folder, edited_video_name)
    
    # Verificar se o vídeo editado já existe
    if not os.path.exists(edited_video_path):
        # Copiar o vídeo original para simular edição
        with open(original_video, 'rb') as src, open(edited_video_path, 'wb') as dst:
            dst.write(src.read())
    
    # Fornecer URL para download
    download_url = f"/static/uploads/{current_user.id}/{edited_video_name}"
    
    return jsonify({
        'success': True,
        'download_url': download_url,
        'filename': 'video_editado.mp4'
    })

@video_bp.route('/api/videos', methods=['GET'])
@login_required
def list_videos():
    # Diretório de upload do usuário
    user_upload_folder = os.path.join(current_app.root_path, UPLOAD_FOLDER, str(current_user.id))
    
    # Verificar se o diretório existe
    if not os.path.exists(user_upload_folder):
        return jsonify({
            'success': True,
            'videos': []
        })
    
    # Listar arquivos de vídeo no diretório
    video_files = [f for f in os.listdir(user_upload_folder) if f.endswith(tuple(ALLOWED_EXTENSIONS)) and not f.startswith('edited_')]
    task_files = [f for f in os.listdir(user_upload_folder) if f.endswith('_task.txt')]
    
    videos = []
    
    for video_file in video_files:
        # Extrair ID do vídeo do nome do arquivo (assumindo formato uuid_filename)
        video_id = video_file.split('_')[0]
        
        # Verificar se existe um arquivo de tarefa para este vídeo
        task_file = next((f for f in task_files if f.startswith(video_id)), None)
        
        status = 'uploaded'
        edited = False
        
        if task_file:
            # Ler status da tarefa
            with open(os.path.join(user_upload_folder, task_file), 'r') as f:
                content = f.read()
                if 'Status: completed' in content:
                    status = 'completed'
                    edited = True
                elif 'Status: processing' in content:
                    status = 'processing'
        
        # Verificar se existe um vídeo editado
        edited_video = f"edited_{video_id}.mp4"
        download_url = None
        
        if os.path.exists(os.path.join(user_upload_folder, edited_video)):
            download_url = f"/static/uploads/{current_user.id}/{edited_video}"
        
        videos.append({
            'id': video_id,
            'original_filename': video_file.split('_', 1)[1],
            'upload_date': datetime.fromtimestamp(os.path.getctime(os.path.join(user_upload_folder, video_file))).isoformat(),
            'status': status,
            'edited': edited,
            'download_url': download_url
        })
    
    return jsonify({
        'success': True,
        'videos': videos
    })
