"""Testes do formatador de saída (offline / layouts / .env / fallback LLM)."""

from __future__ import annotations

import json
import logging
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src.inferencia.formatador_saida import (
    ConfiguracaoSaida,
    carregar_dotenv,
    explicar_offline,
    explicar_via_llm,
    formatar,
)
from src.inferencia.motor_inferencia import ResultadoInferencia

# Logger do módulo sob teste — usado para silenciar WARNINGs esperados.
_LOGGER_FORMATADOR = logging.getLogger("src.inferencia.formatador_saida")


def _resultado_de_exemplo() -> ResultadoInferencia:
    return ResultadoInferencia(
        categoria_prevista="MANTIDA",
        indice_previsto=0,
        distribuicao={
            "MANTIDA": 0.6,
            "REVOGADA": 0.2,
            "ANULADA": 0.1,
            "NAO_CONHECIDA": 0.05,
            "OUTRA": 0.05,
        },
        termos_relevantes=["arrendamento", "renda"],
        excerto_sumario="acórdão sobre arrendamento urbano",
    )


class TestExplicacaoOffline(unittest.TestCase):
    def test_inclui_classe_confianca_termos_e_aviso(self) -> None:
        texto = explicar_offline(_resultado_de_exemplo(), ["arrendamento", "renda"])
        self.assertIn("MANTIDA", texto)
        self.assertIn("60%", texto)
        self.assertIn("arrendamento", texto)
        self.assertIn("não constitui aconselhamento jurídico", texto)


class TestFormatadores(unittest.TestCase):
    def test_formato_texto(self) -> None:
        saida = formatar(_resultado_de_exemplo(), "explicação X", "texto")
        self.assertIn("Resultado da inferência", saida)
        self.assertIn("MANTIDA", saida)
        self.assertIn("explicação X", saida)

    def test_formato_markdown(self) -> None:
        saida = formatar(_resultado_de_exemplo(), "explicação X", "markdown")
        self.assertIn("### Resultado da inferência", saida)
        self.assertIn("| Classe | Probabilidade |", saida)
        self.assertIn("**Classe prevista:** `MANTIDA`", saida)

    def test_formato_json_e_parseavel(self) -> None:
        saida = formatar(_resultado_de_exemplo(), "explicação X", "json")
        parseado = json.loads(saida)
        self.assertEqual(parseado["categoria_prevista"], "MANTIDA")
        self.assertEqual(parseado["explicacao"], "explicação X")


class TestConfiguracao(unittest.TestCase):
    def test_carrega_dotenv_e_nao_sobrepoe_ambiente(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / ".env"
            caminho.write_text(
                "EXPLICACAO_VIA_LLM=true\nFORMATO_SAIDA=markdown\nDEEPSEEK_MODELO=teste/m\n",
                encoding="utf-8",
            )
            ambiente_base = {
                k: v
                for k, v in os.environ.items()
                if k not in {"EXPLICACAO_VIA_LLM", "FORMATO_SAIDA", "DEEPSEEK_MODELO"}
            }
            with mock.patch.dict(os.environ, ambiente_base, clear=True):
                carregar_dotenv(caminho)
                configuracao = ConfiguracaoSaida.a_partir_do_ambiente()
                self.assertTrue(configuracao.usar_llm)
                self.assertEqual(configuracao.formato, "markdown")
                self.assertEqual(configuracao.modelo, "teste/m")

    def test_formato_invalido_cai_para_texto(self) -> None:
        # O WARNING "FORMATO_SAIDA='xml' inválido" é o resultado *esperado*
        # deste teste — silenciamos o logger para o output do unittest ficar limpo.
        with mock.patch.dict(
            os.environ, {"FORMATO_SAIDA": "xml"}, clear=False
        ), mock.patch.object(_LOGGER_FORMATADOR, "warning"):
            self.assertEqual(ConfiguracaoSaida.a_partir_do_ambiente().formato, "texto")


class TestFallbackLLM(unittest.TestCase):
    def test_sem_chave_cai_para_offline(self) -> None:
        configuracao = ConfiguracaoSaida(
            usar_llm=True,
            formato="texto",
            url_base="https://openrouter.ai",
            modelo="x",
            chave_api=None,
            tempo_limite_segundos=5,
        )
        # WARNING "DEEPSEEK_CHAVE_API ausente" é o resultado esperado — silencia.
        with mock.patch.object(_LOGGER_FORMATADOR, "warning"):
            texto = explicar_via_llm(
                _resultado_de_exemplo(), ["arrendamento"], "excerto", configuracao
            )
        self.assertIn("MANTIDA", texto)
        self.assertIn("não constitui aconselhamento jurídico", texto)


if __name__ == "__main__":
    unittest.main()
