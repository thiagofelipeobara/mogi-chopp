# Mogi Chopp

Sistema de gerenciamento de clientes, pedidos e equipamentos para a empresa Mogi Chopp.

## Objetivo

O projeto tem como objetivo facilitar a organização das reservas e o controle operacional da empresa, substituindo controles informais por um sistema centralizado.

## Funcionalidades

- Cadastro e consulta de clientes.
- Cadastro e gerenciamento de pedidos.
- Acompanhamento do status dos pedidos.
- Controle de barris de chopp.
- Controle de máquinas.
- Cálculo de lucro estimado por pedido.
- Painel inicial com resumo dos pedidos.

## Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- SQLite para testes automatizados
- HTML, CSS e Bootstrap
- Pytest

## Requisitos

- Python 3.11 ou superior
- Git
- Banco de dados PostgreSQL

## Instalação

Clone o repositório:

```bash
git clone https://github.com/thiagofelipeobara/mogi-chopp.git
cd mogi-chopp
```

Crie e ative o ambiente virtual no Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração do banco de dados

Crie um arquivo `.env` na raiz do projeto e configure a variável:

```env
DATABASE_URL=postgresql+psycopg2://USUARIO:SENHA@HOST/BASE?sslmode=require
```

Substitua os valores de exemplo pelas credenciais do seu banco PostgreSQL.

Inicialize as tabelas:

```bash
python -m app.database.init_db
```

## Executar o sistema

```bash
python -m app.main
```

Acesse no navegador:

```text
http://127.0.0.1:5000
```

## Executar os testes

```bash
pytest -v
```

Os testes automatizados utilizam SQLite em memória, sem alterar os dados do banco PostgreSQL de desenvolvimento.

## Estrutura do projeto

```text
mogi-chopp/
├── app/
│   ├── database/
│   ├── models/
│   ├── services/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   ├── main.py
│   └── routes.py
├── tests/
├── .env
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```
