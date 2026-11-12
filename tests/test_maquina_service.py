
import pytest

from app.services.maquina_service import criar_maquina, listar_maquinas


def test_criar_maquina(app):
    with app.app_context():
        maquina = criar_maquina("MAQUINA-01")

        assert maquina.id is not None
        assert maquina.identificacao == "MAQUINA-01"
        assert maquina.status == "disponivel"


def test_listar_maquinas(app):
    with app.app_context():
        criar_maquina("MAQUINA-02")
        criar_maquina("MAQUINA-01")

        maquinas = listar_maquinas()

        assert len(maquinas) == 2
        assert maquinas[0].identificacao == "MAQUINA-01"


def test_impedir_maquina_duplicada(app):
    with app.app_context():
        criar_maquina("MAQUINA-01")

        with pytest.raises(ValueError, match="Já existe uma máquina"):
            criar_maquina("MAQUINA-01")


def test_impedir_maquina_sem_identificacao(app):
    with app.app_context():
        with pytest.raises(ValueError, match="identificação da máquina é obrigatória"):
            criar_maquina("")
