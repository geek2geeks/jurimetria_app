"""Testes mínimos para impedir uma configuração aparentemente verde e vazia."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from criar_tarefas_jira import TAREFAS, criar_descricao_adf


RAIZ = Path(__file__).resolve().parents[1]


class TestesConfiguracaoRepositorio(unittest.TestCase):
    """Valida contratos básicos da configuração inicial."""

    def test_documentacao_obrigatoria_existe(self) -> None:
        caminhos_obrigatorios = (
            "constitution.md",
            "docs/fluxo_desenvolvimento_ia.md",
            "docs/instalacao_software.md",
            "docs/boas_praticas_desenvolvimento.md",
            "docs/fluxo_github_jira.md",
        )
        caminhos_em_falta = [
            caminho
            for caminho in caminhos_obrigatorios
            if not (RAIZ / caminho).is_file()
        ]
        self.assertEqual([], caminhos_em_falta)

    def test_constituicao_exige_nomes_descritivos_em_portugues(self) -> None:
        constituicao = (RAIZ / "constitution.md").read_text(encoding="utf-8")
        regras_obrigatorias = (
            "## 9. Nomes descritivos em português",
            "`PascalCase`",
            "`snake_case`",
            "`DocumentoBruto`",
            "`RegistoClassificacao`",
            "`MotorInferencia`",
            "`decisao_bruta`",
            "`id_execucao`",
            "São proibidas abreviaturas vagas",
        )
        for regra in regras_obrigatorias:
            self.assertIn(regra, constituicao)

    def test_definicoes_tarefas_jira_sao_completas_e_unicas(self) -> None:
        self.assertEqual(8, len(TAREFAS))
        self.assertEqual(8, len({tarefa.pessoa for tarefa in TAREFAS}))
        self.assertEqual(8, len({tarefa.titulo for tarefa in TAREFAS}))
        for tarefa in TAREFAS:
            self.assertTrue(
                tarefa.caminho_especificacao.startswith(
                    "docs/especificacoes/"
                )
            )
            self.assertTrue(
                (RAIZ / tarefa.caminho_especificacao).is_file()
            )

    def test_estrutura_principal_usa_nomes_portugueses(self) -> None:
        diretorias_esperadas = {
            "dados",
            "pre_processamento",
            "caracteristicas",
            "modelos",
            "treino",
            "avaliacao",
            "inferencia",
        }
        diretorias_existentes = {
            caminho.name
            for caminho in (RAIZ / "src").iterdir()
            if caminho.is_dir() and caminho.name != "__pycache__"
        }
        self.assertEqual(diretorias_esperadas, diretorias_existentes)

        diretorias_antigas = {
            "data",
            "preprocessing",
            "features",
            "models",
            "training",
            "evaluation",
            "inference",
            "utils",
        }
        self.assertTrue(diretorias_antigas.isdisjoint(diretorias_existentes))

    def test_utilitario_inspecao_usa_nome_portugues(self) -> None:
        self.assertTrue((RAIZ / "inspecionar_pdfs.py").is_file())
        self.assertFalse((RAIZ / "inspect_pdfs.py").exists())

    def test_tarefas_jira_usam_portugues_consistente(self) -> None:
        titulos_esperados = (
            "JurisTriage P1 - Ingestão de dados PDF e JSON em bruto",
            "JurisTriage P2 - Análise posicional, esquemas e adaptação JSON",
            "JurisTriage P3 - Limpeza de texto e normalização de categorias",
            "JurisTriage P4 - Vetorização TF-IDF e divisão dos dados com NumPy",
            "JurisTriage P5 - Modelo e treino com PyTorch",
            "JurisTriage P6 - Modelo de referência, métricas e avaliação",
            "JurisTriage P7 - Inferência e modelo de linguagem opcional",
            "JurisTriage P8 - Integração, qualidade, testes automáticos e manifesto",
        )
        self.assertEqual(
            titulos_esperados,
            tuple(tarefa.titulo for tarefa in TAREFAS),
        )

        for tarefa in TAREFAS:
            descricao = " ".join(
                bloco["content"][0]["text"]
                for bloco in criar_descricao_adf(tarefa)["content"]
            )
            self.assertIn("Responsável:", descricao)
            self.assertIn("Especificação:", descricao)
            self.assertIn("Fluxo de trabalho:", descricao)
            self.assertIn("validação humana", descricao)
            self.assertIn("identificadores descritivos em português", descricao)

    def test_exemplo_membros_jira_cobre_equipa_completa(self) -> None:
        exemplo_membros = json.loads(
            (RAIZ / "membros_jira.exemplo.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            {tarefa.pessoa for tarefa in TAREFAS},
            set(exemplo_membros),
        )

    def test_numpy_fica_abaixo_da_versao_dois(self) -> None:
        requisitos = (RAIZ / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("numpy>=1.24.0,<2.0", requisitos)

    def test_exemplo_ambiente_contem_apenas_marcadores_para_tokens(self) -> None:
        exemplo_ambiente = (RAIZ / ".env.example").read_text(encoding="utf-8")
        self.assertIn(
            "JIRA_TOKEN_API=coloca_aqui_o_token_de_api_jira",
            exemplo_ambiente,
        )
        self.assertIn(
            "DEEPSEEK_CHAVE_API=coloca_aqui_a_chave_de_api_deepseek",
            exemplo_ambiente,
        )


if __name__ == "__main__":
    unittest.main()
