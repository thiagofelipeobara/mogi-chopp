
from datetime import date

from app.models import Cliente, Pedido, Barril, Maquina


def obter_dados_dashboard():
    hoje = date.today()
    inicio_mes = hoje.replace(day=1)

    if hoje.month == 12:
        proximo_mes = date(hoje.year + 1, 1, 1)
    else:
        proximo_mes = date(hoje.year, hoje.month + 1, 1)

    pedidos_mes = Pedido.query.filter(
        Pedido.data_evento >= inicio_mes,
        Pedido.data_evento < proximo_mes
    ).count()

    clientes_total = Cliente.query.count()

    barris_disponiveis = Barril.query.filter_by(
        status="disponivel",
        ativo=True
    ).count()

    maquinas_disponiveis = Maquina.query.filter_by(
        status="disponivel",
        ativo=True
    ).count()

    proximos_pedidos = Pedido.query.filter(
        Pedido.data_evento >= hoje,
        Pedido.status != "cancelado"
    ).order_by(
        Pedido.data_evento.asc()
    ).limit(5).all()

    return {
        "pedidos_mes": pedidos_mes,
        "clientes_total": clientes_total,
        "barris_disponiveis": barris_disponiveis,
        "maquinas_disponiveis": maquinas_disponiveis,
        "proximos_pedidos": proximos_pedidos
    }
