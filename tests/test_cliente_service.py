
from app.services.cliente_service import criar_cliente, listar_clientes


def test_criar_cliente(app):
    with app.app_context():
        cliente = criar_cliente("João Teste", "11999999999")

        assert cliente.id is not None
        assert cliente.nome == "João Teste"
        assert cliente.telefone == "11999999999"


def test_listar_clientes(app):
    with app.app_context():
        criar_cliente("Ana", "11988888888")
        criar_cliente("Carlos", "11977777777")

        clientes = listar_clientes()

        assert len(clientes) == 2
        assert clientes[0].nome == "Ana"
        assert clientes[1].nome == "Carlos"


def test_criar_cliente_sem_nome(app):
    with app.app_context():
        try:
            criar_cliente("", "11999999999")
            assert False, "Deveria ter lançado ValueError"
        except ValueError as erro:
            assert str(erro) == "O nome do cliente é obrigatório."
