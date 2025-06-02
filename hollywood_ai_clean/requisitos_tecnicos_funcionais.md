# Requisitos Técnicos e Funcionais - Hollywood AI

## Visão Geral
Hollywood AI é uma aplicação web que permite aos usuários fazer upload de vídeos e editá-los através de comandos em linguagem natural. O design é inspirado nos estúdios de Hollywood, com um logo representando a icônica caixa d'água de Hollywood.

## Requisitos Funcionais

### 1. Autenticação de Usuários
- Autenticação via API do Google
- Autenticação via API do Facebook
- Autenticação via repositório local (email/senha)
- Perfil de usuário com histórico de edições
- Gerenciamento de sessões de usuário

### 2. Upload de Vídeos
- Suporte para formatos comuns de vídeo (MP4, AVI, MOV, etc.)
- Limite de tamanho de arquivo (sugestão: 100MB)
- Barra de progresso durante o upload
- Validação de formato e tamanho de arquivo
- Armazenamento temporário de vídeos enviados

### 3. Edição de Vídeos
- Corte de vídeo (definir pontos de início e fim)
- Adição de texto sobreposto (diferentes fontes, cores e posições)
- Aplicação de filtros pré-definidos (preto e branco, sépia, saturação, etc.)
- Interface para instruções em linguagem natural
- Processamento das instruções para aplicar edições correspondentes

### 4. Interface do Usuário
- Design inspirado nos estúdios de Hollywood
- Logo personalizado (caixa d'água de Hollywood)
- Campo de upload centralizado na página principal
- Campo de prompt para instruções de edição
- Lista de tarefas/histórico no lado direito
- Visualização prévia do vídeo antes e depois da edição
- Responsividade para diferentes dispositivos

### 5. Gerenciamento de Tarefas
- Lista de tarefas/edições pendentes
- Histórico de edições concluídas
- Status de processamento em tempo real
- Notificações de conclusão

### 6. Download de Vídeos Editados
- Opções de qualidade de download
- Opções de formato de saída
- Link de download direto
- Opção de compartilhamento via link

## Requisitos Técnicos

### 1. Arquitetura
- Aplicação web Flask (Python)
- Frontend com HTML5, CSS3, JavaScript
- Banco de dados para armazenamento de usuários e metadados
- Sistema de filas para processamento de vídeos

### 2. Tecnologias
- Backend: Flask (Python)
- Frontend: HTML5, CSS3, JavaScript (com possível uso de frameworks como React)
- Banco de dados: SQLite para desenvolvimento, MySQL para produção
- Processamento de vídeo: FFmpeg
- Autenticação: OAuth 2.0 para Google e Facebook, JWT para autenticação local
- Armazenamento: Sistema de arquivos local ou serviço de armazenamento em nuvem

### 3. Segurança
- Autenticação segura com OAuth 2.0
- Proteção contra ataques CSRF
- Validação de entrada de usuário
- Sanitização de arquivos enviados
- Proteção contra uploads maliciosos
- Controle de acesso baseado em usuário

### 4. Performance
- Otimização de carregamento de página
- Processamento assíncrono de vídeos
- Compressão de recursos estáticos
- Cache de recursos frequentemente acessados
- Limitação de tamanho de arquivo para upload

### 5. Escalabilidade
- Arquitetura modular
- Sistema de filas para processamento de vídeos
- Separação clara entre frontend e backend
- API RESTful para comunicação entre camadas

## Limitações Técnicas
- Edições limitadas a operações simples (corte, texto, filtros)
- Tamanho máximo de arquivo para upload
- Tempo de processamento dependente da complexidade da edição
- Sem suporte para edições complexas baseadas em IA generativa
- Sem suporte para edições que exigem reconhecimento de objetos ou pessoas

## Fluxo Básico de Usuário
1. Usuário se autentica no sistema
2. Usuário faz upload de um vídeo
3. Sistema processa e armazena temporariamente o vídeo
4. Usuário insere instruções de edição no campo de prompt
5. Sistema interpreta as instruções e aplica edições correspondentes
6. Usuário visualiza prévia do vídeo editado
7. Usuário confirma edições ou solicita ajustes
8. Usuário baixa o vídeo editado em formato desejado
