from app.database import db


class Maquina(db.Model):
    __tablename__ = "maquinas"

    id = db.Column(db.Integer, primary_key=True)

    identificacao = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

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