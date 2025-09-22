# SafeWay API - Sistema de Controle de Acesso Inteligente

API para sistema de controle de acesso baseado em RFID, desenvolvida com Python e FastAPI.

## Funcionalidades

- **Gestão de Usuários**: CRUD completo para usuários do sistema
- **Credenciais RFID**: Gerenciamento de cartões RFID e associação com usuários
- **Controle de Acesso**: Validação de acesso em tempo real
- **Logs de Eventos**: Registro de tentativas de acesso (sucesso/negação)
- **Logs de Erros**: Monitoramento de falhas nos componentes do sistema

## Tecnologias

- Python 3.8+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (migrações)
- Pydantic

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   ```bash
   cp env.example .env
   # Edite o arquivo .env com suas configurações
   ```

5. Execute as migrações:
   ```bash
   alembic upgrade head
   ```

6. Execute o servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

## Endpoints Principais

### Usuários
- `POST /api/v1/users/` - Criar usuário
- `GET /api/v1/users/` - Listar usuários
- `GET /api/v1/users/{id}` - Obter usuário
- `PUT /api/v1/users/{id}` - Atualizar usuário
- `DELETE /api/v1/users/{id}` - Desativar usuário

### RFID
- `POST /api/v1/rfid/credentials` - Criar credencial RFID
- `GET /api/v1/rfid/credentials` - Listar credenciais
- `POST /api/v1/rfid/validate-access` - Validar acesso (sistema local)

### Logs
- `GET /api/v1/logs/access` - Listar logs de acesso
- `POST /api/v1/logs/errors` - Criar log de erro
- `GET /api/v1/logs/errors` - Listar logs de erro

## Documentação

Acesse `http://localhost:8000/docs` para a documentação interativa da API (Swagger UI).
