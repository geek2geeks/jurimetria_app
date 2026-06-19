# -*- coding: utf-8 -*-
"""Testes unitarios do modulo de limpeza de texto (P3)."""

import unittest

from src.pre_processamento.limpeza_texto import limpar_texto, normalizar_categoria


class TestLimpezaTexto(unittest.TestCase):
    """Conjunto de testes para as funcoes de limpeza e normalizacao."""

    def test_limpar_texto_remove_tcpdf(self) -> None:
        """Garante que a assinatura do TCPDF e removida, insensivel a maiusculas."""
        self.assertEqual("teste", limpar_texto("Powered by TCPDF teste"))
        self.assertEqual("teste", limpar_texto("powered by tcpdf teste"))
        self.assertEqual("teste", limpar_texto("POWERED BY TCPDF teste"))
        self.assertEqual("teste", limpar_texto("Powered by TCPDF (www.tcpdf.org) teste"))

    def test_limpar_texto_remove_emails(self) -> None:
        """Garante que enderecos de email sao removidos."""
        self.assertEqual("Contacto teste", limpar_texto("Contacto tribunal@mail.pt teste"))
        self.assertEqual("Contacto teste", limpar_texto("Contacto relacao.lisboa@tribunais.org.pt teste"))

    def test_limpar_texto_remove_urls_e_dominios(self) -> None:
        """Garante que URLs e dominios .pt comuns sao removidos."""
        self.assertEqual("Site teste", limpar_texto("Site http://www.dgsi.pt teste"))
        self.assertEqual("Site teste", limpar_texto("Site https://csm.org.pt teste"))
        self.assertEqual("Site teste", limpar_texto("Site www.tribunais.org.pt teste"))
        self.assertEqual("Site teste", limpar_texto("Site dgsi.pt teste"))

    def test_limpar_texto_remove_telefones_e_faxes(self) -> None:
        """Garante que numeros de telefone e fax portugueses sao removidos."""
        self.assertEqual("Contacto teste", limpar_texto("Contacto Tel: 213240500 teste"))
        self.assertEqual("Contacto teste", limpar_texto("Contacto Fax: +351 213 240 550 teste"))
        self.assertEqual("Contacto teste", limpar_texto("Contacto 21-324-05-00 teste"))
        self.assertEqual("Contacto teste", limpar_texto("Contacto 912345678 teste"))

    def test_limpar_texto_remove_codigos_postais(self) -> None:
        """Garante que codigos postais no formato XXXX-XXX sao removidos."""
        self.assertEqual("Lisboa teste", limpar_texto("1200-001 Lisboa teste"))
        self.assertEqual("Porto teste", limpar_texto("4000-011 Porto teste"))

    def test_limpar_texto_normaliza_espacamento(self) -> None:
        """Garante que espacos multiplos, tabulacoes e quebras de linha sao normalizados."""
        self.assertEqual("texto limpo", limpar_texto("  texto   limpo  "))
        self.assertEqual("texto limpo", limpar_texto("texto\tlimpo\n"))
        self.assertEqual("texto limpo", limpar_texto("texto\r\nlimpo"))

    def test_limpar_texto_valores_nulos_ou_vazios(self) -> None:
        """Garante que valores nulos ou vazios sao tratados com seguranca."""
        # Nota: Por contrato, a assinatura de limpar_texto exige str.
        self.assertEqual("", limpar_texto(""))
        self.assertEqual("", limpar_texto(None))  # type: ignore

    def test_normalizar_categoria_nao_conhecida(self) -> None:
        """Testa o mapeamento para a classe NAO_CONHECIDA."""
        self.assertEqual("NAO_CONHECIDA", normalizar_categoria("decidido nao tomar conhecimento do recurso"))
        self.assertEqual("NAO_CONHECIDA", normalizar_categoria("recurso rejeitado"))
        self.assertEqual("NAO_CONHECIDA", normalizar_categoria("recurso deserto"))
        self.assertEqual("NAO_CONHECIDA", normalizar_categoria("julgada a extincao por extemporaneidade"))
        self.assertEqual("NAO_CONHECIDA", normalizar_categoria("nao admitido o recurso"))

    def test_normalizar_categoria_anulada(self) -> None:
        """Testa o mapeamento para a classe ANULADA."""
        self.assertEqual("ANULADA", normalizar_categoria("anulada a decisao recorrida"))
        self.assertEqual("ANULADA", normalizar_categoria("declarada a nulidade da sentenca"))

    def test_normalizar_categoria_mantida(self) -> None:
        """Testa o mapeamento para a classe MANTIDA."""
        self.assertEqual("MANTIDA", normalizar_categoria("negado provimento ao recurso"))
        self.assertEqual("MANTIDA", normalizar_categoria("julgou-se improcedente a accao"))
        self.assertEqual("MANTIDA", normalizar_categoria("confirmada a sentenca recorrida"))
        self.assertEqual("MANTIDA", normalizar_categoria("manter a decisao impugnada"))

    def test_normalizar_categoria_revogada(self) -> None:
        """Testa o mapeamento para a classe REVOGADA."""
        self.assertEqual("REVOGADA", normalizar_categoria("concedido provimento ao recurso"))
        self.assertEqual("REVOGADA", normalizar_categoria("recurso provido parcialmente"))
        self.assertEqual("REVOGADA", normalizar_categoria("julgou-se procedente a apelacao"))
        self.assertEqual("REVOGADA", normalizar_categoria("revoga-se a sentenca recorrida"))
        self.assertEqual("REVOGADA", normalizar_categoria("alterada a decisao"))

    def test_normalizar_categoria_outra(self) -> None:
        """Testa o mapeamento para a classe OUTRA."""
        self.assertEqual("OUTRA", normalizar_categoria("declarado extinto o processo"))
        self.assertEqual("OUTRA", normalizar_categoria("recurso prejudicado"))
        self.assertEqual("OUTRA", normalizar_categoria("homologada a transaccao"))
        self.assertEqual("OUTRA", normalizar_categoria("declara-se a incompetencia do tribunal"))

    def test_normalizar_categoria_precedencia(self) -> None:
        """Garante que a ordem de precedencia (ADR-05) e estritamente respeitada."""
        # 1. "negado provimento" tem "provimento" (REVOGADA) e "negado provimento" (MANTIDA)
        # Deve dar MANTIDA porque MANTIDA e verificada antes de REVOGADA, ou porque a regra de MANTIDA contem o stem completo.
        # Mais especificamente, "negado provimento" deve bater em MANTIDA.
        self.assertEqual("MANTIDA", normalizar_categoria("negado provimento"))

        # 2. "rejeitado por nulidade" tem "rejei" (NAO_CONHECIDA) e "nulidad" (ANULADA)
        # Deve dar NAO_CONHECIDA porque a admissibilidade (Ordem 1) tem precedencia.
        self.assertEqual("NAO_CONHECIDA", normalizar_categoria("recurso rejeitado por nulidade"))

        # 3. "sentenca anulada por improcedencia" tem "anulad" (ANULADA) e "improced" (MANTIDA)
        # Deve dar ANULADA porque ANULADA (Ordem 2) tem precedencia sobre MANTIDA (Ordem 3).
        self.assertEqual("ANULADA", normalizar_categoria("sentenca anulada por improcedencia"))

    def test_normalizar_categoria_descarte_e_nulos(self) -> None:
        """Garante que valores nulos, vazios ou nao reconhecidos devolvem None (descarte)."""
        self.assertIsNone(normalizar_categoria(None))
        self.assertIsNone(normalizar_categoria(""))
        self.assertIsNone(normalizar_categoria("absolvido do pedido"))
        self.assertIsNone(normalizar_categoria("decidido conhecer do recurso"))

    def test_mojibake_tolerancia(self) -> None:
        """Garante que o caractere de substituicao (mojibake) e tolerado e removido."""
        # \uFFFD e o caractere de substituicao 
        self.assertEqual("colocaao", limpar_texto("coloca\uFFFD\uFFFDao"))
        self.assertEqual("sentena", limpar_texto("senten\uFFFDa"))
        self.assertEqual("MANTIDA", normalizar_categoria("decis\uFFFDo mantida"))

    def test_normalizar_categoria_com_acentos(self) -> None:
        """Garante que entradas com acentuacao ou cedilha sao normalizadas e mapeadas corretamente."""
        self.assertEqual("MANTIDA", normalizar_categoria("não provido"))
        self.assertEqual("REVOGADA", normalizar_categoria("concedido provimento à reclamação"))
        self.assertEqual("REVOGADA", normalizar_categoria("reformada a sentença"))
        self.assertEqual("OUTRA", normalizar_categoria("declara-se a competência"))


if __name__ == "__main__":
    unittest.main()
