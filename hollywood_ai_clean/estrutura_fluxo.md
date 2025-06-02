# Estrutura do Site e Fluxo de Usuários - Hollywood AI

## Estrutura do Site

### Páginas Principais:

1.  **`/` (Página Inicial / Upload):**
    *   **Header:** Logo (Caixa d'água Hollywood), Navegação (Login/Cadastro ou Perfil do Usuário/Logout).
    *   **Conteúdo Principal:**
        *   Área central para upload de vídeo (drag-and-drop e seleção de arquivo).
        *   Campo de prompt abaixo da área de upload: "O que você quer editar em seu vídeo?" (habilitado após upload).
    *   **Barra Lateral Direita:** Lista de tarefas/histórico de edições (vídeos enviados, status do processamento, vídeos editados).
    *   **Footer:** Informações básicas, links (Termos de Serviço, Política de Privacidade).

2.  **`/login`:**
    *   Formulário de login local (email/senha).
    *   Botões para login via Google e Facebook.
    *   Link para a página de cadastro (`/signup`).

3.  **`/signup`:**
    *   Formulário de cadastro local (nome, email, senha).
    *   Link para a página de login (`/login`).

4.  **`/profile` (Opcional/Integrado):**
    *   Poderia ser uma seção na página principal ou uma página separada.
    *   Exibição do histórico detalhado de edições.
    *   Opções para gerenciar a conta (alterar senha, etc.).

### Endpoints da API (Backend Flask):

*   **Autenticação:**
    *   `POST /api/auth/login/local`: Login com email/senha.
    *   `POST /api/auth/signup/local`: Cadastro de novo usuário.
    *   `GET /api/auth/login/google`: Redireciona para o fluxo OAuth do Google.
    *   `GET /api/auth/callback/google`: Callback do Google OAuth.
    *   `GET /api/auth/login/facebook`: Redireciona para o fluxo OAuth do Facebook.
    *   `GET /api/auth/callback/facebook`: Callback do Facebook OAuth.
    *   `POST /api/auth/logout`: Encerra a sessão do usuário.
    *   `GET /api/auth/status`: Verifica o status de autenticação do usuário.
*   **Vídeos e Edição:**
    *   `POST /api/upload`: Upload de novo vídeo.
    *   `GET /api/videos`: Lista os vídeos e tarefas do usuário logado.
    *   `POST /api/videos/{video_id}/edit`: Envia o prompt de edição para um vídeo específico.
    *   `GET /api/videos/{video_id}/status`: Obtém o status de processamento de uma tarefa de edição.
    *   `GET /api/videos/{video_id}/preview`: (Opcional) Obtém um preview do vídeo editado.
    *   `GET /api/videos/{video_id}/download`: Inicia o download do vídeo final editado.

## Fluxo de Usuários

1.  **Novo Usuário - Cadastro Local:**
    *   Acessa `/` -> Clica em "Cadastro".
    *   Preenche formulário em `/signup` -> Submete.
    *   Backend valida dados, cria usuário, inicia sessão -> Redireciona para `/` (logado).

2.  **Novo Usuário - Cadastro Social (Google/Facebook):**
    *   Acessa `/` -> Clica em "Login".
    *   Clica no botão Google ou Facebook em `/login`.
    *   Redirecionado para a plataforma social para autorização.
    *   Autoriza -> Redirecionado de volta para o callback (`/api/auth/callback/...`).
    *   Backend verifica token/código, cria usuário (se não existir), inicia sessão -> Redireciona para `/` (logado).

3.  **Usuário Existente - Login Local:**
    *   Acessa `/` -> Clica em "Login".
    *   Preenche formulário em `/login` -> Submete.
    *   Backend valida credenciais, inicia sessão -> Redireciona para `/` (logado).

4.  **Usuário Existente - Login Social:**
    *   Similar ao cadastro social, mas o backend apenas inicia a sessão do usuário existente.

5.  **Fluxo de Edição:**
    *   Usuário logado acessa `/`.
    *   Clica na área de upload, seleciona um vídeo.
    *   Frontend exibe progresso do upload para `/api/upload`.
    *   Após upload bem-sucedido, vídeo aparece na lista de tarefas (status: "Pronto para editar"), campo de prompt é habilitado.
    *   Usuário digita instruções no prompt (ex: "Cortar de 0:10 a 0:30", "Adicionar texto 'Final' no centro", "Aplicar filtro P&B").
    *   Usuário clica em "Editar".
    *   Frontend envia o ID do vídeo e o prompt para `/api/videos/{video_id}/edit`.
    *   Backend recebe, valida, enfileira a tarefa de edição (usando FFmpeg).
    *   Status na lista de tarefas muda para "Processando".
    *   Frontend (opcionalmente) consulta `/api/videos/{video_id}/status` periodicamente ou usa WebSocket.
    *   Backend conclui a edição, atualiza o status para "Concluído".
    *   Frontend atualiza a lista de tarefas, habilita botão de download.
    *   (Opcional: Exibe uma pré-visualização antes de habilitar o download).
    *   Usuário clica em "Download".
    *   Frontend requisita `/api/videos/{video_id}/download`.
    *   Backend envia o arquivo de vídeo editado.
