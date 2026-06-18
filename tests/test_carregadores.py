"""Testes unitários da especificação P1.

Os testes usam simulação/mocks para validar comportamento sem depender de PDFs
reais. Isso é intencional: o objetivo é provar que os iteradores emitem
DocumentoBruto e continuam funcionando mesmo quando há falhas.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.dados.carregador_json_bruto import carregar_jsons_brutos
from src.dados.carregador_pdf import carregar_pdfs
from src.dados.esquemas import DocumentoBruto


class TestCarregadoresP1(unittest.TestCase):
    """Valida os carregadores incrementais de PDF e JSON bruto."""

    @patch("src.dados.carregador_pdf.pdfplumber.open")
    def test_carregar_pdf_valido_emite_documento_bruto(self, mock_pdf_open: MagicMock) -> None:
        """PDF válido deve emitir uma instância de DocumentoBruto."""
        pagina_1 = MagicMock()
        pagina_1.extract_text.return_value = "Texto da página 1"
        pagina_2 = MagicMock()
        pagina_2.extract_text.return_value = "Texto da página 2"

        pdf_mock = MagicMock()
        pdf_mock.pages = [pagina_1, pagina_2]
        mock_pdf_open.return_value.__enter__.return_value = pdf_mock

        with tempfile.TemporaryDirectory() as pasta_tmp:
            caminho_pdf = Path(pasta_tmp) / "valido.pdf"
            caminho_pdf.write_bytes(b"conteudo simulado")

            documentos = list(carregar_pdfs(pasta_tmp))

        self.assertEqual(len(documentos), 1)
        self.assertIsInstance(documentos[0], DocumentoBruto)
        self.assertEqual(documentos[0].nome_ficheiro, "valido.pdf")
        self.assertEqual(documentos[0].numero_paginas, 2)
        self.assertEqual(documentos[0].origem, "pdf")
        self.assertIn("Texto da página 1", documentos[0].texto)
        self.assertIn("Texto da página 2", documentos[0].texto)

    @patch("src.dados.carregador_pdf.pdfplumber.open")
    def test_pdf_corrompido_nao_interrompe_iterador(self, mock_pdf_open: MagicMock) -> None:
        """PDF corrompido deve cair no except e não quebrar o ciclo."""
        mock_pdf_open.side_effect = RuntimeError("PDF corrompido")

        with tempfile.TemporaryDirectory() as pasta_tmp:
            caminho_pdf = Path(pasta_tmp) / "corrompido.pdf"
            caminho_pdf.write_bytes(b"conteudo invalido")

            documentos = list(carregar_pdfs(pasta_tmp))

        self.assertEqual(documentos, [])

    def test_json_bruto_valido_emite_documento_bruto(self) -> None:
        """JSON com chave texto deve emitir DocumentoBruto com origem json."""
        with tempfile.TemporaryDirectory() as pasta_tmp:
            caminho_json = Path(pasta_tmp) / "bruto.json"
            caminho_json.write_text(json.dumps({"texto": "Texto jurídico bruto."}), encoding="utf-8")

            documentos = list(carregar_jsons_brutos(pasta_tmp))

        self.assertEqual(len(documentos), 1)
        self.assertIsInstance(documentos[0], DocumentoBruto)
        self.assertEqual(documentos[0].nome_ficheiro, "bruto.json")
        self.assertEqual(documentos[0].texto, "Texto jurídico bruto.")
        self.assertIsNone(documentos[0].numero_paginas)
        self.assertEqual(documentos[0].origem, "json")

    def test_json_estruturado_e_rejeitado_na_p1(self) -> None:
        """JSON estruturado deve ser ignorado, pois pertence ao adaptador da P2."""
        with tempfile.TemporaryDirectory() as pasta_tmp:
            caminho_json = Path(pasta_tmp) / "estruturado.json"
            caminho_json.write_text(
                json.dumps({"ecli": "ECLI:PT:STA:1950:000578.FF", "relator": "Vaz Pereira"}),
                encoding="utf-8",
            )

            documentos = list(carregar_jsons_brutos(pasta_tmp))

        self.assertEqual(documentos, [])


if __name__ == "__main__":
    unittest.main()
