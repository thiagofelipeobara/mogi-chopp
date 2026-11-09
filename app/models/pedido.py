from datetime import datetime
from app.database import db


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id"),
        nullable=False
    )

    data_evento = db.Column(db.Date, nullable=False)

    custo_barril = db.Column(db.Numeric(10, 2), nullable=False)
    valor_venda = db.Column(db.Numeric(10, 2), nullable=False)

    despesas_adicionais = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="pendente"
    )

    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    cliente = db.relationship("Cliente", backref="pedidos")

    @property
    def lucro_estimado(self):
        return (
            self.valor_venda
            - self.custo_barril
            - self.despesas_adicionais
        )