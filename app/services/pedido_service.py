
from app.database import db
from app.models import Pedido, Cliente


def criar_pedido(dados):
    campos_obrigatorios = [
        "cliente_id",
        "data_evento",
        "custo_barril",
        "valor_venda"
    ]

    for campo in campos_obrigatorios:
        if campo not in dados or dados[campo] is None:
            raise ValueError(f"O campo {campo} é obrigatório.")

    custo_barril = dados["custo_barril"]
    valor_venda = dados["valor_venda"]
    despesas = dados.get("despesas_adicionais", 0)

    if custo_barril < 0 or valor_venda < 0 or despesas < 0:
        raise ValueError("Os valores financeiros não podem ser negativos.")

    cliente = db.session.get(Cliente, dados["cliente_id"])

    if not cliente:
        raise ValueError("Cliente não encontrado.")

    pedido = Pedido(
        cliente_id=dados["cliente_id"],
        data_evento=dados["data_evento"],
        custo_barril=custo_barril,
        valor_venda=valor_venda,
        despesas_adicionais=despesas,
        status=dados.get("status", "pendente")
    )

    db.session.add(pedido)
    db.session.commit()

    return pedido

def listar_pedidos():
    return Pedido.query.order_by(Pedido.data_evento).all()


def atualizar_status_pedido(pedido_id, novo_status):
    status_validos = [
        "pendente",
        "confirmado",
        "concluido",
        "cancelado"
    ]

    if novo_status not in status_validos:
        raise ValueError("Status inválido.")

    pedido = db.session.get(Pedido, pedido_id)

    if not pedido:
        raise ValueError("Pedido não encontrado.")

    pedido.status = novo_status

    db.session.commit()

    return pedido
