# Blog API

## Iniciando aplicação via docker (utilizando banco de dados PostgreSQL)
 - `docker-compose up`
---
## Iniciando aplicação localmente (utilizando banco de dados SQLite)
### Preparando ambiente virtual
 - `pip install pipenv`
 - `pipenv shell`
 - `pipenv install`

### Iniciando banco de dados
 - `flask shell`
 - `db.create_all()`

### Iniciando API
 - `flask run`
---
## Consumo da api
 - No postman, importar o arquivo `desafio-framework.postman_collection.json` na raiz do projeto para verificar os padrões de requisição
 - Tempo de validade do token JWT: 15 minutos
