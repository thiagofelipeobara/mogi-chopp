
from datetime import date

from app.models import Cliente, Pedido, Barril, Maquina


def test_pagina_inicial(app, client):
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert b"Mogi Chopp" in resposta.data


def test_pagina_clientes(app, client):
    resposta = client.get("/clientes")

    assert resposta.status_code == 200


def test_cadastrar_cliente_pela_rota(app, client):
    resposta = client.post("/clientes/novo", data={
        "nome": "Cliente Rota",
        "telefone": "11999999999"
    })

    assert resposta.status_code == 302

    with app.app_context():
        cliente = Cliente.query.filter_by(
            nome="Cliente Rota"
        ).first()

        assert cliente is not None
        assert cliente.telefone == "11999999999"


def test_pagina_pedidos(app, client):
    resposta = client.get("/pedidos")

    assert resposta.status_code == 200


def test_cadastrar_pedido_pela_rota(app, client):
    with app.app_context():
        cliente = Cliente(
            nome="Cliente Pedido",
            telefone="11988888888"
        )
        from app.database import db
        db.session.add(cliente)
        db.session.commit()
        cliente_id = cliente.id

    resposta = client.post("/pedidos/novo", data={
        "cliente_id": str(cliente_id),
        "data_evento": "2026-12-20",
        "custo_barril": "180.00",
        "valor_venda": "450.00",
        "despesas_adicionais": "30.00"
    })

    assert resposta.status_code == 302

    with app.app_context():
        pedido = Pedido.query.first()

        assert pedido is not None
        assert pedido.data_evento == date(2026, 12, 20)
        assert pedido.lucro_estimado == 240


def test_pagina_equipamentos(app, client):
    resposta = client.get("/equipamentos")

    assert resposta.status_code == 200


def test_cadastrar_barril_pela_rota(app, client):
    resposta = client.post("/equipamentos/barris/novo", data={
        "identificacao": "BARRIL-ROTA-01",
        "capacidade_litros": "50"
    })

    assert resposta.status_code == 302

    with app.app_context():
        barril = Barril.query.filter_by(
            identificacao="BARRIL-ROTA-01"
        ).first()

        assert barril is not None
        assert barril.capacidade_litros == 50


def test_cadastrar_maquina_pela_rota(app, client):
    resposta = client.post("/equipamentos/maquinas/novo", data={
        "identificacao": "MAQUINA-ROTA-01"
    })

    assert resposta.status_code == 302

    with app.app_context():
        maquina = Maquina.query.filter_by(
            identificacao="MAQUINA-ROTA-01"
        ).first()

        assert maquina is not None
        assert maquina.status == "disponivel"


def test_alterar_status_pedido_pela_rota(app, client):
    from app.database import db

    with app.app_context():
        cliente = Cliente(
            nome="Cliente Status",
            telefone="11977777777"
        )
        db.session.add(cliente)
        db.session.commit()

        pedido = Pedido(
            cliente_id=cliente.id,
            data_evento=date(2026, 12, 20),
            custo_barril=180,
            valor_venda=450,
            despesas_adicionais=30,
            status="pendente"
        )
        db.session.add(pedido)
        db.session.commit()
        pedido_id = pedido.id

    resposta = client.post(
        f"/pedidos/{pedido_id}/status",
        data={"status": "confirmado"}
    )

    assert resposta.status_code == 302

    with app.app_context():
        pedido_atualizado = db.session.get(Pedido, pedido_id)
        assert pedido_atualizado.status == "confirmado"
