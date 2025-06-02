// Funcionalidades principais do Hollywood AI
document.addEventListener('DOMContentLoaded', function() {
    // Elementos da interface
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('file-input');
    const selectFileBtn = document.getElementById('select-file-btn');
    const promptInput = document.getElementById('prompt-input');
    const editBtn = document.getElementById('edit-btn');
    const taskList = document.getElementById('task-list');
    
    // Variáveis de estado
    let currentVideoId = null;
    let tasks = [];
    
    // Inicialização
    init();
    
    function init() {
        // Configurar eventos de upload
        setupUploadEvents();
        
        // Carregar tarefas existentes
        loadTasks();
        
        // Configurar atualização periódica
        setInterval(updateTasksStatus, 5000);
    }
    
    function setupUploadEvents() {
        // Evento de clique no botão de seleção de arquivo
        selectFileBtn.addEventListener('click', function() {
            fileInput.click();
        });
        
        // Evento de seleção de arquivo
        fileInput.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                handleFileUpload(e.target.files[0]);
            }
        });
        
        // Eventos de drag and drop
        dropzone.addEventListener('dragover', function(e) {
            e.preventDefault();
            dropzone.classList.add('dragover');
        });
        
        dropzone.addEventListener('dragleave', function() {
            dropzone.classList.remove('dragover');
        });
        
        dropzone.addEventListener('drop', function(e) {
            e.preventDefault();
            dropzone.classList.remove('dragover');
            
            if (e.dataTransfer.files.length > 0) {
                handleFileUpload(e.dataTransfer.files[0]);
            }
        });
        
        // Evento de clique no botão de edição
        editBtn.addEventListener('click', function() {
            if (currentVideoId && promptInput.value.trim() !== '') {
                sendEditRequest(currentVideoId, promptInput.value.trim());
            }
        });
    }
    
    function handleFileUpload(file) {
        // Verificar se é um arquivo de vídeo
        if (!file.type.startsWith('video/')) {
            showNotification('Erro', 'Por favor, selecione um arquivo de vídeo válido.');
            return;
        }
        
        // Verificar tamanho do arquivo (limite de 100MB)
        if (file.size > 100 * 1024 * 1024) {
            showNotification('Erro', 'O arquivo é muito grande. O tamanho máximo é 100MB.');
            return;
        }
        
        // Criar FormData para envio
        const formData = new FormData();
        formData.append('video', file);
        
        // Mostrar indicador de carregamento
        dropzone.innerHTML = '<div class="upload-icon"><i class="fas fa-spinner fa-spin"></i></div><div class="upload-text">Enviando vídeo...</div>';
        
        // Enviar arquivo para o servidor
        fetch('/api/upload', {
            method: 'POST',
            body: formData,
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Atualizar interface após upload bem-sucedido
                currentVideoId = data.video.id;
                
                // Atualizar dropzone
                dropzone.innerHTML = `
                    <div class="upload-icon"><i class="fas fa-check-circle"></i></div>
                    <div class="upload-text">Vídeo enviado com sucesso: ${data.video.original_filename}</div>
                    <button class="upload-btn" id="new-upload-btn">Enviar outro vídeo</button>
                `;
                
                // Configurar botão para novo upload
                document.getElementById('new-upload-btn').addEventListener('click', function() {
                    resetUploadArea();
                });
                
                // Habilitar campo de prompt e botão de edição
                promptInput.disabled = false;
                editBtn.disabled = false;
                
                // Adicionar à lista de tarefas
                addTaskToList({
                    id: data.video.id,
                    name: data.video.original_filename,
                    status: 'Pronto para editar',
                    progress: 0,
                    hasDownload: false
                });
                
                showNotification('Sucesso', 'Vídeo enviado com sucesso!');
            } else {
                resetUploadArea();
                showNotification('Erro', data.message || 'Erro ao enviar o vídeo.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            resetUploadArea();
            showNotification('Erro', 'Ocorreu um erro ao enviar o vídeo. Por favor, tente novamente.');
        });
    }
    
    function resetUploadArea() {
        dropzone.innerHTML = `
            <div class="upload-icon"><i class="fas fa-film"></i></div>
            <div class="upload-text">Arraste e solte seu vídeo aqui ou clique para selecionar</div>
            <button class="upload-btn" id="select-file-btn">Selecionar Vídeo</button>
        `;
        
        // Reconfigurar botão de seleção
        document.getElementById('select-file-btn').addEventListener('click', function() {
            fileInput.click();
        });
        
        // Resetar campo de arquivo
        fileInput.value = '';
        
        // Desabilitar campo de prompt e botão de edição
        promptInput.disabled = true;
        promptInput.value = '';
        editBtn.disabled = true;
        
        // Resetar ID do vídeo atual
        currentVideoId = null;
    }
    
    function sendEditRequest(videoId, prompt) {
        // Desabilitar campo de prompt e botão durante o processamento
        promptInput.disabled = true;
        editBtn.disabled = true;
        
        fetch(`/api/videos/${videoId}/edit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: prompt }),
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Atualizar status na lista de tarefas
                updateTaskStatus(videoId, 'Processando', 10);
                
                // Resetar área de upload para novo vídeo
                resetUploadArea();
                
                showNotification('Sucesso', 'Solicitação de edição enviada com sucesso!');
            } else {
                // Reabilitar campo de prompt e botão
                promptInput.disabled = false;
                editBtn.disabled = false;
                
                showNotification('Erro', data.message || 'Erro ao enviar solicitação de edição.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            
            // Reabilitar campo de prompt e botão
            promptInput.disabled = false;
            editBtn.disabled = false;
            
            showNotification('Erro', 'Ocorreu um erro ao enviar a solicitação de edição. Por favor, tente novamente.');
        });
    }
    
    function loadTasks() {
        // Carregar tarefas do usuário do servidor
        fetch('/api/videos', {
            method: 'GET',
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.videos) {
                // Limpar lista atual
                taskList.innerHTML = '';
                tasks = [];
                
                // Adicionar cada vídeo à lista
                data.videos.forEach(video => {
                    const task = {
                        id: video.id,
                        name: video.original_filename,
                        status: video.status === 'completed' ? 'Concluído' : 'Processando',
                        progress: video.status === 'completed' ? 100 : 50,
                        hasDownload: video.edited,
                        downloadUrl: video.download_url
                    };
                    
                    addTaskToList(task);
                    tasks.push(task);
                });
                
                // Se não houver tarefas, mostrar mensagem
                if (tasks.length === 0) {
                    taskList.innerHTML = '<li class="task-item">Nenhuma tarefa encontrada.</li>';
                }
            }
        })
        .catch(error => {
            console.error('Erro ao carregar tarefas:', error);
        });
    }
    
    function addTaskToList(task) {
        // Verificar se a tarefa já existe na lista
        const existingTaskIndex = tasks.findIndex(t => t.id === task.id);
        if (existingTaskIndex !== -1) {
            // Atualizar tarefa existente
            tasks[existingTaskIndex] = { ...tasks[existingTaskIndex], ...task };
        } else {
            // Adicionar nova tarefa
            tasks.push(task);
        }
        
        // Atualizar a visualização da lista
        updateTaskListView();
    }
    
    function updateTaskStatus(taskId, status, progress) {
        const taskIndex = tasks.findIndex(t => t.id === taskId);
        if (taskIndex !== -1) {
            tasks[taskIndex].status = status;
            tasks[taskIndex].progress = progress;
            updateTaskListView();
        }
    }
    
    function updateTasksStatus() {
        // Atualizar status de tarefas em processamento
        const processingTasks = tasks.filter(task => task.status === 'Processando');
        
        processingTasks.forEach(task => {
            fetch(`/api/videos/${task.id}/status`, {
                method: 'GET',
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Mapear status do servidor para interface
                    let status = 'Processando';
                    let hasDownload = false;
                    
                    if (data.status === 'completed') {
                        status = 'Concluído';
                        hasDownload = true;
                    } else if (data.status === 'failed') {
                        status = 'Falha';
                    }
                    
                    // Atualizar tarefa na lista
                    updateTaskStatus(task.id, status, data.progress);
                    
                    // Se concluído, atualizar opção de download
                    if (status === 'Concluído') {
                        const taskIndex = tasks.findIndex(t => t.id === task.id);
                        if (taskIndex !== -1) {
                            tasks[taskIndex].hasDownload = true;
                            
                            // Obter URL de download
                            fetch(`/api/videos/${task.id}/download`, {
                                method: 'GET',
                                credentials: 'same-origin'
                            })
                            .then(response => response.json())
                            .then(downloadData => {
                                if (downloadData.success) {
                                    tasks[taskIndex].downloadUrl = downloadData.download_url;
                                    updateTaskListView();
                                }
                            });
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Erro ao atualizar status:', error);
            });
        });
    }
    
    function updateTaskListView() {
        // Limpar lista atual
        taskList.innerHTML = '';
        
        // Adicionar cada tarefa à lista
        tasks.forEach(task => {
            const taskItem = document.createElement('li');
            taskItem.className = 'task-item';
            
            taskItem.innerHTML = `
                <div class="task-name">${task.name}</div>
                <div class="task-status">${task.status}</div>
                <div class="task-progress">
                    <div class="progress-bar" style="width: ${task.progress}%"></div>
                </div>
                <div class="task-actions">
                    ${task.hasDownload ? `<a href="${task.downloadUrl}" class="task-btn">Download</a>` : ''}
                </div>
            `;
            
            taskList.appendChild(taskItem);
        });
        
        // Se não houver tarefas, mostrar mensagem
        if (tasks.length === 0) {
            taskList.innerHTML = '<li class="task-item">Nenhuma tarefa encontrada.</li>';
        }
    }
    
    function showNotification(title, message) {
        // Implementação simples de notificação
        alert(`${title}: ${message}`);
        
        // Em uma implementação real, seria melhor usar um sistema de notificações mais elegante
    }
});
