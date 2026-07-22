"""Testes do módulo de métricas e modelo de referência (SCRUM-10).

Usa exclusivamente dados sintéticos — nunca dados reais do corpus.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

try:
    from src.avaliacao.metricas import (
        ModeloReferenciaClasseMaioritaria,
        avaliar_execucao,
        exportar_metricas,
    )
except ImportError as e:
    raise unittest.SkipTest(
        f"Dependência opcional em falta para testes de métricas: {e}"
    ) from e


class TestModeloReferencia(unittest.TestCase):

    def test_aprende_classe_maioritaria(self) -> None:
        # Treino com MANTIDA (0) dominante — aparece 5 vezes
        treino = np.array([0, 0, 0, 1, 2, 0, 1, 0])
        referencia = ModeloReferenciaClasseMaioritaria()
        referencia.fit(treino)
        self.assertEqual(0, referencia.classe_maioritaria)

    def test_preve_sempre_a_mesma_classe(self) -> None:
        treino = np.array([0, 0, 1, 2])
        referencia = ModeloReferenciaClasseMaioritaria()
        referencia.fit(treino)
        previsoes = referencia.prever(np.array([1, 2, 3, 0, 1]))
        # todas as previsões devem ser 0
        self.assertTrue(np.all(previsoes == 0))

    def test_erro_sem_fit(self) -> None:
        referencia = ModeloReferenciaClasseMaioritaria()
        with self.assertRaises(RuntimeError):
            referencia.prever(np.array([0, 1, 2]))


class TestMetricas(unittest.TestCase):

    def test_exatidao_perfeita(self) -> None:
        reais      = np.array([0, 1, 2, 0, 1])
        previstas  = np.array([0, 1, 2, 0, 1])
        referencia = np.array([0, 0, 0, 0, 0])
        resultado = avaliar_execucao(reais, previstas, referencia)
        self.assertAlmostEqual(1.0, resultado["exatidao"])
        self.assertAlmostEqual(1.0, resultado["macro_f1"])

    def test_referencia_tem_macro_f1_baixo_com_dados_desequilibrados(self) -> None:
        """Prova que exatidão sozinha é enganosa com dados desequilibrados.

        Com MANTIDA (0) dominante, a referência tem exatidão alta
        mas Macro-F1 muito baixo.
        """
        # 8 exemplos MANTIDA, 1 REVOGADA, 1 ANULADA
        reais      = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 2])
        referencia = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        resultado = avaliar_execucao(reais, referencia, referencia)

        # Exatidão: 8/10 = 0.8 — parece bom!
        self.assertGreater(resultado["exatidao"], 0.7)

        # Mas Macro-F1 é baixo — prova que o modelo é inútil para classes minoritárias
        self.assertLess(resultado["macro_f1_referencia"], 0.4)

    def test_exporta_json_valido(self) -> None:
        reais      = np.array([0, 1, 2])
        previstas  = np.array([0, 1, 1])
        referencia = np.array([0, 0, 0])
        metricas = avaliar_execucao(reais, previstas, referencia)

        with tempfile.TemporaryDirectory() as pasta:
            caminho = exportar_metricas(metricas, pasta)
            self.assertTrue(caminho.exists())

            with open(caminho, encoding="utf-8") as f:
                dados = json.load(f)

            self.assertIn("exatidao", dados)
            self.assertIn("macro_f1", dados)
            self.assertIn("macro_f1_referencia", dados)

    def test_resultado_tem_formato_correto(self) -> None:
        reais      = np.array([0, 1, 2, 0, 1])
        previstas  = np.array([0, 1, 1, 0, 2])
        referencia = np.array([0, 0, 0, 0, 0])
        resultado = avaliar_execucao(reais, previstas, referencia)

        # Verifica que todas as chaves esperadas existem
        self.assertIn("exatidao", resultado)
        self.assertIn("macro_f1", resultado)
        self.assertIn("macro_f1_referencia", resultado)

        # Verifica que os valores estão entre 0 e 1
        self.assertGreaterEqual(resultado["exatidao"], 0.0)
        self.assertLessEqual(resultado["exatidao"], 1.0)
        self.assertGreaterEqual(resultado["macro_f1"], 0.0)
        self.assertLessEqual(resultado["macro_f1"], 1.0)


if __name__ == "__main__":
    unittest.main()