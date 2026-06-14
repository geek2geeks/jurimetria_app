"""Testes do adaptador JSON -> Acordao.

Usa apenas fixtures SINTÉTICAS escritas em ficheiros temporários. Nenhum dado
real do corpus é versionado (constituição §8, ethics).
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.dados.carregador_acordaos_json import (
    acordao_de_dicionario,
    carregar_acordaos_json,
)

# Fixture sintética com o mesmo schema do corpus real (valores inventados).
EXEMPLO_JSON = {
    "ecli": "ECLI:PT:STJ:2099:000000.XX",
    "jurisprudencia_url": "http://exemplo.local/ecli/000000.XX",
    "relator": "Relator Ficticio",
    "numero_documento": "ficticio000000",
    "data_acordao": "01/01/2099",
    "votacao": "unanimidade",
    "meio_processual": "Revista",
    "decisao": "negado provimento.",
    "area_tematica": "dir civil.",
    "descritores": "tema um; tema dois; tema tres;",
    "sumario_texto": "Sumario sintetico de teste.",
    "sumario_exists": True,
    "decisao_integral_texto": None,
    "court_code": "STJ",
    "year": 2099,
    "extraction_success": True,
}


class TestCarregadorAcordaosJson(unittest.TestCase):
    def test_mapeia_campos_externos_para_portugues(self) -> None:
        acordao = acordao_de_dicionario(EXEMPLO_JSON)
        self.assertEqual("STJ", acordao.tribunal)  # court_code -> tribunal
        self.assertEqual(2099, acordao.ano)  # year -> ano
        self.assertEqual("Sumario sintetico de teste.", acordao.sumario)
        self.assertEqual("negado provimento.", acordao.decisao_bruta)
        self.assertEqual("json", acordao.origem)

    def test_descritores_separados_por_ponto_e_virgula(self) -> None:
        acordao = acordao_de_dicionario(EXEMPLO_JSON)
        self.assertEqual(["tema um", "tema dois", "tema tres"], acordao.descritores)

    def test_campos_ausentes_ou_vazios_viram_none(self) -> None:
        acordao = acordao_de_dicionario({"sumario_texto": "   ", "year": "nao-int"})
        self.assertIsNone(acordao.sumario)
        self.assertIsNone(acordao.ano)
        self.assertIsNone(acordao.decisao_bruta)
        self.assertEqual([], acordao.descritores)

    def test_carregar_de_ficheiro_objeto_unico(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "acordao.json"
            caminho.write_text(json.dumps(EXEMPLO_JSON), encoding="utf-8")
            acordaos = carregar_acordaos_json(caminho)
        self.assertEqual(1, len(acordaos))
        self.assertEqual("STJ", acordaos[0].tribunal)

    def test_carregar_de_ficheiro_lista(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "acordaos.json"
            caminho.write_text(json.dumps([EXEMPLO_JSON, EXEMPLO_JSON]), encoding="utf-8")
            acordaos = carregar_acordaos_json(caminho)
        self.assertEqual(2, len(acordaos))

    def test_tolera_encoding_com_caractere_de_substituicao(self) -> None:
        # Simula o mojibake do corpus (bytes com U+FFFD) sem rebentar.
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "mojibake.json"
            conteudo = json.dumps({"decisao": "confirmada a senten�a."})
            caminho.write_text(conteudo, encoding="utf-8")
            acordaos = carregar_acordaos_json(caminho)
        self.assertEqual(1, len(acordaos))
        self.assertIsNotNone(acordaos[0].decisao_bruta)


if __name__ == "__main__":
    unittest.main()
