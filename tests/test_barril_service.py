
import pytest

from app.services.barril_service import criar_barril, listar_barris


def test_criar_barril(app):
    with app.app_context():
        barril = criar_barril("BARRIL-01", 50)

        assert barril.id is not None
        assert barril.identificacao == "BARRIL-01"
        assert barril.capacidade_litros == 50
        assert barril.status == "disponivel"


def test_listar_barris(app):
    with app.app_context():
        criar_barril("BARRIL-02", 50)
        criar_barril("BARRIL-01", 30)

        barris = listar_barris()

        assert len(barris) == 2
        assert barris[0].identificacao == "BARRIL-01"


def test_impedir_barril_duplicado(app):
    with app.app_context():
        criar_barril("BARRIL-01", 50)

        with pytest.raises(ValueError, match="Já existe um barril"):
            criar_barril("BARRIL-01", 50)


def test_impedir_capacidade_invalida(app):
    with app.app_context():
        with pytest.raises(ValueError, match="A capacidade deve ser maior que zero"):
            criar_barril("BARRIL-01", 0)
