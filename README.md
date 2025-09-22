# SafeWay API - Sistema de Controle de Acesso Inteligente

API para sistema de controle de acesso baseado em RFID, desenvolvida com Python e FastAPI.

## 🚀 Início Rápido

### 1. Iniciar o Sistema
```bash
docker-compose up -d
```

### 2. Acessar a API
- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc

### 3. Testar no Swagger
1. Acesse http://localhost:8000/docs
2. Clique em qualquer endpoint
3. Clique em "Try it out"
4. Preencha os dados e clique em "Execute"

## 📋 Funcionalidades

- **Gestão de Usuários**: CRUD completo para usuários do sistema
- **Credenciais RFID**: Gerenciamento de cartões RFID e associação com usuários
- **Controle de Acesso**: Validação de acesso em tempo real
- **Logs de Eventos**: Registro de tentativas de acesso (sucesso/negação)
- **Logs de Erros**: Monitoramento de falhas nos componentes do sistema

## 🛠️ Tecnologias

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic

## 📊 Dados Iniciais

O sistema já vem com dados de exemplo:
- **10 usuários** pré-cadastrados
- **10 cartões RFID** (RFID001 a RFID010)
- Todos os dados ficam ativos por padrão

## 🐳 Comandos Docker

```bash
docker-compose up -d          # Iniciar todos os serviços
docker-compose down           # Parar todos os serviços
docker-compose logs -f        # Ver logs dos serviços
docker-compose exec app bash  # Acessar shell do container
docker-compose exec db psql -U safeway_user -d safeway_db  # Acessar banco
docker-compose down -v        # Limpar containers e volumes
```

## 🔗 Endpoints Principais

### 👥 Usuários
- `POST /api/v1/users/` - Criar usuário
- `GET /api/v1/users/` - Listar usuários (paginado)
- `GET /api/v1/users/all` - Listar todos os usuários
- `GET /api/v1/users/{id}` - Obter usuário por ID
- `PUT /api/v1/users/{id}` - Atualizar usuário
- `DELETE /api/v1/users/{id}` - Desativar usuário

### 🏷️ RFID
- `POST /api/v1/rfid/credentials` - Criar credencial RFID
- `GET /api/v1/rfid/credentials` - Listar credenciais (paginado)
- `GET /api/v1/rfid/credentials/all` - Listar todas as credenciais
- `GET /api/v1/rfid/credentials/{id}` - Obter credencial por ID
- `PUT /api/v1/rfid/credentials/{id}` - Atualizar credencial
- `POST /api/v1/rfid/validate-access` - Validar acesso (sistema local)

### 📝 Logs de Acesso
- `GET /api/v1/logs/access` - Listar logs de acesso (paginado)
- `GET /api/v1/logs/access/all` - Listar todos os logs de acesso
- `GET /api/v1/logs/access/{id}` - Obter log de acesso por ID

### ❌ Logs de Erro
- `POST /api/v1/logs/errors` - Criar log de erro
- `GET /api/v1/logs/errors` - Listar logs de erro (paginado)
- `GET /api/v1/logs/errors/all` - Listar todos os logs de erro
- `GET /api/v1/logs/errors/{id}` - Obter log de erro por ID

## 📚 Documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
