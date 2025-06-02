# README - Hollywood AI

## Visão Geral

Hollywood AI é uma aplicação web que permite aos usuários fazer upload de vídeos e editá-los através de comandos em linguagem natural. O design é inspirado nos estúdios de Hollywood, com um logo representando a icônica caixa d'água de Hollywood.

## Funcionalidades Principais

- **Autenticação de Usuários**: Login via Google, Facebook ou credenciais locais
- **Upload de Vídeos**: Suporte para formatos comuns de vídeo (MP4, AVI, MOV, etc.)
- **Edição de Vídeos**: Corte, adição de texto e aplicação de filtros via instruções em linguagem natural
- **Lista de Tarefas**: Acompanhamento em tempo real do status das edições
- **Download de Vídeos Editados**: Opções para baixar os vídeos após a edição

## Estrutura do Projeto

```
hollywood_ai_final/
├── src/                        # Código-fonte principal
│   ├── models/                 # Modelos de dados
│   │   └── auth/               # Modelos de autenticação
│   ├── routes/                 # Rotas e endpoints da API
│   │   └── auth/               # Rotas de autenticação
│   ├── static/                 # Arquivos estáticos
│   │   ├── css/                # Folhas de estilo
│   │   ├── js/                 # Scripts JavaScript
│   │   └── images/             # Imagens e ícones
│   ├── templates/              # Templates HTML
│   │   └── auth/               # Templates de autenticação
│   └── main.py                 # Ponto de entrada da aplicação
├── design_assets/              # Arquivos de design
│   ├── hollywood_ai_logo.png   # Logo principal
│   └── homepage_mockup.png     # Mockup da página inicial
├── requisitos_tecnicos_funcionais.md  # Documentação de requisitos
├── estrutura_fluxo.md          # Documentação da estrutura e fluxo
├── validacao.md                # Relatório de validação
└── README.md                   # Este arquivo
```

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: MySQL
- **Autenticação**: OAuth 2.0 (Google, Facebook), JWT
- **Processamento de Vídeo**: FFmpeg (simulado na versão atual)

## Configuração e Instalação

### Pré-requisitos

- Python 3.8+
- MySQL
- FFmpeg (para processamento real de vídeo)

### Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/hollywood-ai.git
   cd hollywood-ai
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   ```
   export SECRET_KEY="sua-chave-secreta"
   export GOOGLE_CLIENT_ID="seu-client-id-google"
   export GOOGLE_CLIENT_SECRET="seu-client-secret-google"
   export FACEBOOK_CLIENT_ID="seu-client-id-facebook"
   export FACEBOOK_CLIENT_SECRET="seu-client-secret-facebook"
   ```

5. Inicialize o banco de dados:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Execute a aplicação:
   ```
   python src/main.py
   ```

7. Acesse a aplicação em `http://localhost:5000`

## Implementação de Edição de Vídeo

Na versão atual, o processamento de edição de vídeo é simulado. Para implementar a edição real, você precisará:

1. Instalar o FFmpeg
2. Analisar o prompt do usuário para identificar comandos (corte, texto, filtros)
3. Gerar e executar comandos FFmpeg correspondentes
4. Atualizar o status e fornecer o vídeo editado para download

## Melhorias Futuras

- Implementação real de edição de vídeo usando FFmpeg
- Mais opções de filtros pré-definidos
- Visualização prévia do vídeo antes do download
- Sistema de notificações por email
- Histórico detalhado de edições
- Compartilhamento direto em redes sociais

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.
