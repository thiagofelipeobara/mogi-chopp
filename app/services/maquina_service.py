from app.database import db
from app.models import Maquina


def criar_maquina(identificacao):
    if not identificacao or not identificacao.strip():
        raise ValueError("A identificação da máquina é obrigatória.")

    maquina_existente = Maquina.query.filter_by(
        identificacao=identificacao.strip()
    ).first()

    if maquina_existente:
        raise ValueError("Já existe uma máquina com essa identificação.")

    maquina = Maquina(
        identificacao=identificacao.strip()
    )

    db.session.add(maquina)
    db.session.commit()

    return maquina


def listar_maquinas():
    return Maquina.query.order_by(Maquina.identificacao).all()