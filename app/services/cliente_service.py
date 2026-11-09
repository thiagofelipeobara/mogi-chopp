
from app.database import db
from app.models import Cliente


def criar_cliente(nome, telefone):
    if not nome or not nome.strip():
        raise ValueError("O nome do cliente é obrigatório.")

    if not telefone or not telefone.strip():
        raise ValueError("O telefone do cliente é obrigatório.")

    cliente = Cliente(
        nome=nome.strip(),
        telefone=telefone.strip()
    )
    

    db.session.add(cliente)
    db.session.commit()

    return cliente

def listar_clientes():
    return Cliente.query.order_by(Cliente.nome).all()
