
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from flask import Blueprint, render_template, request, redirect, url_for

from app.database import db
from app.models import Cliente, Pedido, Barril, Maquina

from app.services.cliente_service import criar_cliente, listar_clientes
from app.services.pedido_service import (
    criar_pedido,
    listar_pedidos,
    atualizar_status_pedido
)
from app.services.barril_service import criar_barril, listar_barris
from app.services.maquina_service import criar_maquina, listar_maquinas

main = Blueprint("main", __name__)

@main.route("/pedidos/<int:pedido_id>/status", methods=["POST"])
def alterar_status_pedido(pedido_id):
    novo_status = request.form.get("status", "")

    try:
        atualizar_status_pedido(pedido_id, novo_status)
        return redirect(url_for("main.pedidos", sucesso="status"))

    except ValueError as erro:
        return render_template(
            "pedidos.html",
            pedidos=listar_pedidos(),
            clientes=listar_clientes(),
            erro=str(erro)
        )


@main.route("/")
def index():
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

    return render_template(
        "index.html",
        pedidos_mes=pedidos_mes,
        clientes_total=clientes_total,
        barris_disponiveis=barris_disponiveis,
        maquinas_disponiveis=maquinas_disponiveis,
        proximos_pedidos=proximos_pedidos
    )

# CLIENTES

@main.route("/clientes")
def clientes():
    return render_template(
        "clientes.html",
        clientes=listar_clientes()
    )


@main.route("/clientes/novo", methods=["POST"])
def novo_cliente():
    nome = request.form.get("nome", "")
    telefone = request.form.get("telefone", "")

    try:
        criar_cliente(nome, telefone)
        return redirect(url_for("main.clientes", sucesso="cliente"))
    except ValueError as erro:
        return render_template(
            "clientes.html",
            clientes=listar_clientes(),
            erro=str(erro)
        )


# PEDIDOS

@main.route("/pedidos")
def pedidos():
    return render_template(
        "pedidos.html",
        pedidos=listar_pedidos(),
        clientes=listar_clientes()
    )


@main.route("/pedidos/novo", methods=["POST"])
def novo_pedido():
    try:
        dados = {
            "cliente_id": int(request.form["cliente_id"]),
            "data_evento": datetime.strptime(
                request.form["data_evento"], "%Y-%m-%d"
            ).date(),
            "custo_barril": Decimal(request.form["custo_barril"]),
            "valor_venda": Decimal(request.form["valor_venda"]),
            "despesas_adicionais": Decimal(
                request.form.get("despesas_adicionais") or "0"
            )
        }

        criar_pedido(dados)
        return redirect(url_for("main.pedidos", sucesso="pedido"))

    except (ValueError, InvalidOperation, KeyError) as erro:
        return render_template(
            "pedidos.html",
            pedidos=listar_pedidos(),
            clientes=listar_clientes(),
            erro=str(erro)
        )


# EQUIPAMENTOS

@main.route("/equipamentos")
def equipamentos():
    return render_template(
        "equipamentos.html",
        barris=listar_barris(),
        maquinas=listar_maquinas()
    )


@main.route("/equipamentos/barris/novo", methods=["POST"])
def novo_barril():
    try:
        capacidade = request.form.get("capacidade_litros")

        criar_barril(
            request.form.get("identificacao", ""),
            int(capacidade) if capacidade else None
        )

        return redirect(url_for("main.equipamentos", sucesso="barril"))

    except ValueError as erro:
        return render_template(
            "equipamentos.html",
            barris=listar_barris(),
            maquinas=listar_maquinas(),
            erro=str(erro)
        )


@main.route("/equipamentos/maquinas/novo", methods=["POST"])
def nova_maquina():
    try:
        criar_maquina(request.form.get("identificacao", ""))
        return redirect(url_for("main.equipamentos", sucesso="maquina"))

    except ValueError as erro:
        return render_template(
            "equipamentos.html",
            barris=listar_barris(),
            maquinas=listar_maquinas(),
            erro=str(erro)
        )
