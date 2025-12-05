# Academia Dev Python - Desafio Técnico 2026.1

Sistema para gerenciar alunos, cursos e matrículas

## Funcionalidades implementadas

- CRUD de Alunos, Cursos e Matrículas por api (`/api/alunos/`, `/api/cursos/`, `/api/matriculas/`)
- Docker compose: a aplicação usa Postgres e PgAdmin, os scripts de inicialização criam o banco e importam as tabelas do arquivo `meu_database.sql`

## Requisitos

- Docker 
- Docker Compose
- Git

## Como rodar

1. Clone o repositorio 

```bash
git clone https://github.com/M2004GV/academia-dev-python.git .
```

2. Configure as variáveis de ambiente

 Copie `.env_example` para `.env` e ajuste as credenciais. O arquivo já contém valores do desenvolvimento Docker.
 ```bash
 cp .env_example .env
 # edite .env se deseja alterar o usuário, senha ou o nome do banco
  ```

3. Build e subir:

    ``` bash
    docker-compose up --build 
    ```
    O compose criará a imagem do django, inicializará o PostgreSQL com as tabelas definidas em `meu_database.sql` e disponibilizará o PgAdmin na porta 5050

4. **Acesse a aplicação**:

   - **Frontend (HTML)**:
     - Dashboard: [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/)
     - Histórico do aluno: [http://localhost:8000/alunos/1/historico/](http://localhost:8000/alunos/1/historico/) (substitua `1` pelo ID do aluno).

   - **API REST** (prefixo `/api/`):
     - Alunos: `http://localhost:8000/api/alunos/`
     - Cursos: `http://localhost:8000/api/cursos/`
     - Matrículas: `http://localhost:8000/api/matriculas/`
     - Relatórios JSON: `http://localhost:8000/api/relatorios/total_matriculas_por_curso/`, `total_devido_por_aluno/` e `pagamentos_pendentes/`

   - **Django Admin**: [http://localhost:8000/admin/](http://localhost:8000/admin/)

   - **PgAdmin**: [http://localhost:5050](http://localhost:5050).  Use as credenciais definidas em `.env` (variáveis `PGADMIN_USER` e `PGADMIN_PASSWORD`).  Após logar, adicione um servidor apontando para host `db`, porta `5432` e as credenciais do banco.

## 🛠 Uso da API

Os endpoints seguem o padrão REST do Django Rest Framework. Exemplos de uso com `curl`:

```bash
# Listar alunos
curl http://localhost:8000/api/alunos/

# Criar novo aluno
curl -X POST http://localhost:8000/api/alunos/ \
     -H "Content-Type: application/json" \
     -d '{"nome":"João","email":"joao@example.com","cpf":"12345678901"}'

# Matrículas de um aluno específico (aluno_id=1)
curl http://localhost:8000/api/matriculas/por_aluno/?aluno_id=1

# Total devido por aluno
curl http://localhost:8000/api/relatorios/total_devido_por_aluno/
```

## Dicas gerais

- A aplicação usa ``managed=False`` nos modelos para aproveitar as tabelas criadas via SQL no `meu_database.sql`.  Isso evita conflitos entre migrations e a estrutura definida no desafio.
- Os relatórios HTML podem ser acessados mesmo sem dados; experimente cadastrar alunos, cursos e matrículas via API ou admin para ver os gráficos popularem.
- Para criar um usuário administrador, conecte-se ao contêiner e execute `python manage.py createsuperuser`.  Por exemplo:
  ```bash
  docker compose exec web python manage.py createsuperuser
  ```
- Toda funcionalidade solicitada no PDF está mapeada: CRUD completo, relatório via SQL bruto, relatórios HTML e API, uso de Docker com Postgres【551091830093539†L24-L89】.