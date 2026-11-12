
from datetime import date
from decimal import Decimal

import pytest

from app.services.cliente_service import criar_cliente
from app.services.pedido_service import (
    criar_pedido,
    listar_pedidos,
    atualizar_status_pedido,
)


def test_criar_pedido(app):
    with app.app_context():
        cliente = criar_cliente("João Teste", "11999999999")

        pedido = criar_pedido({
            "cliente_id": cliente.id,
            "data_evento": date(2026, 12, 20),
            "custo_barril": Decimal("180.00"),
            "valor_venda": Decimal("450.00"),
            "despesas_adicionais": Decimal("30.00"),
        })

        assert pedido.id is not None
        assert pedido.status == "pendente"
        assert pedido.lucro_estimado == Decimal("240.00")


def test_listar_pedidos(app):
    with app.app_context():
        cliente = criar_cliente("João", "11999999999")

        criar_pedido({
            "cliente_id": cliente.id,
            "data_evento": date(2026, 12, 20),
            "custo_barril": Decimal("100"),
            "valor_venda": Decimal("300"),
        })

        criar_pedido({
            "cliente_id": cliente.id,
            "data_evento": date(2026, 11, 20),
            "custo_barril": Decimal("100"),
            "valor_venda": Decimal("250"),
        })

        pedidos = listar_pedidos()

        assert len(pedidos) == 2
        assert pedidos[0].data_evento == date(2026, 11, 20)


def test_impedir_pedido_sem_cliente(app):
    with app.app_context():
        with pytest.raises(ValueError, match="Cliente não encontrado"):
            criar_pedido({
                "cliente_id": 999,
                "data_evento": date(2026, 12, 20),
                "custo_barril": Decimal("100"),
                "valor_venda": Decimal("300"),
            })


def test_impedir_valores_negativos(app):
    with app.app_context():
        cliente = criar_cliente("João", "11999999999")

        with pytest.raises(ValueError, match="não podem ser negativos"):
            criar_pedido({
                "cliente_id": cliente.id,
                "data_evento": date(2026, 12, 20),
                "custo_barril": Decimal("-100"),
                "valor_venda": Decimal("300"),
            })


def test_impedir_pedido_sem_campo_obrigatorio(app):
    with app.app_context():
        with pytest.raises(ValueError, match="data_evento é obrigatório"):
            criar_pedido({
                "cliente_id": 1,
                "custo_barril": Decimal("100"),
                "valor_venda": Decimal("300"),
            })


def test_atualizar_status_pedido(app):
    with app.app_context():
        cliente = criar_cliente("João", "11999999999")

        pedido = criar_pedido({
            "cliente_id": cliente.id,
            "data_evento": date(2026, 12, 20),
            "custo_barril": Decimal("100"),
            "valor_venda": Decimal("300"),
        })

        pedido_atualizado = atualizar_status_pedido(
            pedido.id, "confirmado"
        )

        assert pedido_atualizado.status == "confirmado"


def test_impedir_status_invalido(app):
    with app.app_context():
        with pytest.raises(ValueError, match="Status inválido"):
            atualizar_status_pedido(1, "invalido")
