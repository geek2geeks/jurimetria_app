"""Testes unitários do módulo de gráficos de avaliação (SCRUM-31)."""

import os
import tempfile
import unittest

from src.avaliacao.graficos import gerar_grafico_curvas_perda


class TestGraficos(unittest.TestCase):
    """Conjunto de testes para a geração de gráficos."""

    def test_gerar_grafico_curvas_perda(self):
        loss_treino = [1.5, 1.0, 0.5, 0.2, 0.05]
        loss_teste = [1.6, 1.1, 0.6, 0.3, 0.08]

        with tempfile.TemporaryDirectory() as tmpdir:
            caminho_png = os.path.join(tmpdir, "test_loss.png")
            resultado = gerar_grafico_curvas_perda(
                loss_treino, loss_teste, caminho_destino=caminho_png
            )
            # Se matplotlib estiver disponível, o ficheiro deve ser criado
            if resultado is not None:
                self.assertTrue(os.path.exists(caminho_png))
                self.assertGreater(os.path.getsize(caminho_png), 0)


if __name__ == "__main__":
    unittest.main()
