"""Testes do contrato de dados (esquemas)."""
from __future__ import annotations

import unittest

from src.dados.esquemas import (
    CAMPOS_FUGA_INFORMACAO,
    Acordao,
    DocumentoBruto,
    RegistoClassificacao,
)


class TestEsquemas(unittest.TestCase):
    def test_documento_bruto_tem_campos_minimos(self) -> None:
        documento = DocumentoBruto(
            nome_ficheiro="exemplo.pdf",
            caminho="dados/amostra/exemplo.pdf",
            texto="texto",
            numero_paginas=2,
            origem="pdf",
        )
        self.assertEqual("pdf", documento.origem)

    def test_texto_caracteristicas_junta_descritores_e_sumario(self) -> None:
        acordao = Acordao(
            descritores=["direito de preferencia", "onus da prova"],
            sumario="o sumario do acordao",
        )
        texto = acordao.texto_caracteristicas()
        self.assertIn("direito de preferencia", texto)
        self.assertIn("onus da prova", texto)
        self.assertIn("o sumario do acordao", texto)

    def test_texto_caracteristicas_nao_inclui_fuga(self) -> None:
        # A resposta (decisao_bruta) e os identificadores nunca podem aparecer
        # no texto de características.
        acordao = Acordao(
            ecli="ECLI:PT:STJ:2024:000.AB",
            tribunal="STJ",
            descritores=["tema"],
            sumario="resumo",
            decisao_bruta="negado provimento",
            texto_integral="o tribunal decide negar provimento",
        )
        texto = acordao.texto_caracteristicas()
        self.assertNotIn("STJ", texto)
        self.assertNotIn("negado provimento", texto)
        self.assertNotIn("ECLI", texto)

    def test_acordao_vazio_devolve_texto_vazio(self) -> None:
        self.assertEqual("", Acordao().texto_caracteristicas())

    def test_campos_de_fuga_existem_no_contrato(self) -> None:
        nomes = set(Acordao().__dict__)
        for campo in CAMPOS_FUGA_INFORMACAO:
            self.assertIn(campo, nomes)

    def test_registo_classificacao_tem_alvo(self) -> None:
        registo = RegistoClassificacao(
            id_documento="documento_001",
            texto="tema resumo",
            categoria_normalizada="MANTIDA",
            tribunal="TRL",
            ano=2015,
        )
        self.assertEqual("MANTIDA", registo.categoria_normalizada)


if __name__ == "__main__":
    unittest.main()
