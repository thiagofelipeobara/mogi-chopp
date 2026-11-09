
from app.database import db
from app.models import Barril


def criar_barril(identificacao, capacidade_litros=None):
    if not identificacao or not identificacao.strip():
        raise ValueError("A identificação do barril é obrigatória.")

    barril_existente = Barril.query.filter_by(
        identificacao=identificacao.strip()
    ).first()

    if barril_existente:
        raise ValueError("Já existe um barril com essa identificação.")

    if capacidade_litros is not None and capacidade_litros <= 0:
        raise ValueError("A capacidade deve ser maior que zero.")

    barril = Barril(
        identificacao=identificacao.strip(),
        capacidade_litros=capacidade_litros
    )

    db.session.add(barril)
    db.session.commit()

    return barril


def listar_barris():
    return Barril.query.order_by(Barril.identificacao).all()
