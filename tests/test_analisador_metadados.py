"""Testes do analisador posicional de metadados (SCRUM-6 / P2).

Cobre o contrato de saida do analisador: recebe DocumentoBruto, devolve
Acordao, tolera campos em falta, e levanta TypeError em inputs invalidos.
"""
from __future__ import annotations

import unittest

from src.dados.esquemas import Acordao, DocumentoBruto
from src.pre_processamento.analisador_metadados import (
    analisar_documento_bruto,
)


# Texto bem formado, usado em varios testes. Baseado no caso real
# data/documento_bruto_ECLI_PT_TRL_2025_20.24.0T8LSB.L1.4.D7.json
TEXTO_VALIDO = (
    "ECLI:PT:TRL:2025:20.24.0T8LSB.L1.4.D7\n"
    "http://jurisprudencia.csm.org.pt/ecli/ECLI:PT:TRL:2025:20.24.0T8LSB.L1.4.D7\n"
    "Relator Nº do Documento\n"
    "Francisca Mendes rl\n"
    "Apenso Data do Acordão\n"
    "12/03/2025\n"
    "Data de decisão sumária Votação\n"
    "unanimidade\n"
    "Tribunal de recurso Processo de recurso\n"
    "Data Recurso\n"
    "Referência de processo de recurso Nível de acesso\n"
    "Público\n"
    "Meio Processual Decisão\n"
    "Apelação improcedente\n"
    "Indicações eventuais Área Temática\n"
    "Referências Internacionais\n"
    "Jurisprudência Nacional\n"
    "Legislação Comunitária\n"
    "Legislação Estrangeira\n"
    "Descritores\n"
    "plataforma digital; aplicação da lei no tempo; presunção de laboralidade; "
    "subordinação jurídica; indícios;\n"
    "Página 1 / 21\n"
    "Sumário:\n"
    "1-Resultou provado que o estafeta exerce a sua actividade no âmbito de "
    "plataforma digital desde Outubro de 2020.\n"
    "2- Atenta a data do início do contrato, na qualificação do mesmo, não "
    "cumpre aplicar o disposto no art. 12º-A do CT.\n"
    "Decisão Integral:\n"
    "Acordam os juízes no Tribunal da Relação de Lisboa:\n"
)


class TestAnalisadorMetadados(unittest.TestCase):
    """Cobre o contrato de saida do analisador posicional."""

    def _doc(self, texto: str) -> DocumentoBruto:
        """Helper para construir um DocumentoBruto com texto ficticio."""
        return DocumentoBruto(
            nome_ficheiro="exemplo.pdf",
            caminho="dados/amostra/exemplo.pdf",
            texto=texto,
            numero_paginas=1,
            origem="pdf",
        )

    # --- Testes funcionais ---

    def test_caso_valido_extrai_todos_os_campos(self) -> None:
        """Texto bem formado produz Acordao com todos os campos extraidos."""
        acordao = analisar_documento_bruto(self._doc(TEXTO_VALIDO))
        self.assertIsInstance(acordao, Acordao)
        self.assertEqual("ECLI:PT:TRL:2025:20.24.0T8LSB.L1.4.D7", acordao.ecli)
        self.assertEqual("TRL", acordao.tribunal)
        self.assertEqual("Francisca Mendes", acordao.relator)
        self.assertEqual("12/03/2025", acordao.data_acordao)
        self.assertEqual("Apelação", acordao.meio_processual)
        self.assertEqual("improcedente", acordao.decisao_bruta)
        self.assertIsNotNone(acordao.sumario)
        self.assertIn("plataforma digital", acordao.sumario or "")
        # O sumario do caso real contem tambem referencias a "presuncao de
        # laboralidade". No nosso TEXTO_VALIDO simplificado so' temos 2
        # paragrafos, mas validamos que comeca com "1-Resultou".
        self.assertTrue((acordao.sumario or "").startswith("1-Resultou"))
        self.assertEqual(
            [
                "plataforma digital",
                "aplicação da lei no tempo",
                "presunção de laboralidade",
                "subordinação jurídica",
                "indícios",
            ],
            acordao.descritores,
        )
        # Proveniencia
        self.assertEqual("pdf", acordao.origem)
        self.assertTrue(acordao.extracao_bem_sucedida)

    def test_saida_e_sempre_instancia_de_acordao(self) -> None:
        """Resultado e' sempre Acordao, nunca dict (regra da spec P2)."""
        for texto in (TEXTO_VALIDO, "texto livre sem metadados", "", "abc"):
            resultado = analisar_documento_bruto(self._doc(texto))
            self.assertIsInstance(resultado, Acordao)

    # --- Testes de tolerancia ---

    def test_texto_sem_metadados_devolve_none_e_lista_vazia(self) -> None:
        """Texto sem estrutura devolve None/[] (NAO falha)."""
        acordao = analisar_documento_bruto(
            self._doc("Apenas um paragrafo livre sem campos estruturados.")
        )
        self.assertIsNone(acordao.ecli)
        self.assertIsNone(acordao.tribunal)
        self.assertIsNone(acordao.relator)
        self.assertIsNone(acordao.sumario)
        self.assertIsNone(acordao.data_acordao)
        self.assertIsNone(acordao.meio_processual)
        self.assertIsNone(acordao.decisao_bruta)
        self.assertEqual([], acordao.descritores)

    def test_texto_vazio_e_tolerado(self) -> None:
        """Texto vazio e' tolerado, devolve Acordao com todos os campos None."""
        acordao = analisar_documento_bruto(self._doc(""))
        self.assertIsNone(acordao.ecli)
        self.assertIsNone(acordao.relator)
        self.assertEqual([], acordao.descritores)

    def test_sumario_nao_inclui_seccao_decisao_integral(self) -> None:
        """Sumario para ANTES de 'Decisao Integral:' (anti-contaminacao)."""
        texto = (
            "Sumário:\n"
            "Texto do sumario aqui.\n"
            "Decisão Integral:\n"
            "Texto da decisao NAO deve estar no sumario.\n"
        )
        acordao = analisar_documento_bruto(self._doc(texto))
        self.assertEqual("Texto do sumario aqui.", acordao.sumario)

    def test_sumario_com_e_sem_acento(self) -> None:
        """Sumario e Sumário (com e sem acento) sao ambos apanhados."""
        for etiqueta in ("Sumário", "Sumario"):
            texto = f"{etiqueta}:\nTexto de teste.\nDecisão Integral:\n"
            acordao = analisar_documento_bruto(self._doc(texto))
            self.assertEqual("Texto de teste.", acordao.sumario)

    def test_descritores_separados_por_ponto_e_virgula(self) -> None:
        """4 descritores com ';' viram lista de 4."""
        texto = "Descritores: a; b; c; d"
        acordao = analisar_documento_bruto(self._doc(texto))
        self.assertEqual(["a", "b", "c", "d"], acordao.descritores)

    def test_descritores_ignoram_string_vazia(self) -> None:
        """'a;;b;;c' vira ['a', 'b', 'c'] (descarta vazios)."""
        texto = "Descritores: a;;b;;c"
        acordao = analisar_documento_bruto(self._doc(texto))
        self.assertEqual(["a", "b", "c"], acordao.descritores)

    def test_ecli_bem_formado_e_extraido(self) -> None:
        """ECLI canonico com prefixo completo e' apanhado."""
        texto = "ECLI:PT:STJ:2024:12345\nRelator: Maria"
        acordao = analisar_documento_bruto(self._doc(texto))
        self.assertEqual("ECLI:PT:STJ:2024:12345", acordao.ecli)
        self.assertEqual("STJ", acordao.tribunal)

    # --- Testes de erro (TypeError) ---

    def test_documento_bruto_none_levanta_typeerror(self) -> None:
        """documento_bruto=None e' erro de programacao, NAO silencio."""
        with self.assertRaises(TypeError):
            analisar_documento_bruto(None)  # type: ignore[arg-type]

    def test_texto_none_levanta_typeerror(self) -> None:
        """documento_bruto.texto=None e' erro de contrato."""
        doc = DocumentoBruto(
            nome_ficheiro="x.pdf",
            caminho="x.pdf",
            texto=None,  # type: ignore[arg-type]
            numero_paginas=0,
            origem="pdf",
        )
        with self.assertRaises(TypeError):
            analisar_documento_bruto(doc)


if __name__ == "__main__":
    unittest.main()
