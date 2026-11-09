from app.database import db


class Barril(db.Model):
    __tablename__ = "barris"

    id = db.Column(db.Integer, primary_key=True)

    identificacao = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    capacidade_litros = db.Column(db.Integer, nullable=True)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="disponivel"
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )