"""Testes de executar_inferencia.py — CLI e funções auxiliares.

Cobre:
  - _ficheiros_json: resolução de ficheiro único, pasta e pasta vazia.
  - _processar_ficheiro: previsão + formatação para um JSON real na pasta data/.
  - _exibir_metricas_treino: os três formatos (texto, markdown, json) e o caso
    sem métricas (execução de scaffolding sem valores numéricos).
  - principal: código de retorno 0 (sucesso) e 1 (pasta vazia).

Nenhum dado real é transmitido para fora da máquina (constituição §8).
As execuções de artefactos são criadas em directórios temporários, fabricadas
por uma fixture LOCAL ao ficheiro (`_fabricar_execucao_de_teste` abaixo).

Durante a integração progressiva, alguns módulos da equipa podem ainda não
estar mergeados no `main`. Em vez de falhar com `ModuleNotFoundError`, este
ficheiro faz **skip condicional** — quando todas as dependências chegarem ao
`main`, os testes passam automaticamente sem qualquer alteração aqui.
"""
from __future__ import annotations

import importlib.util as _importlib_util
import unittest

# --- Skip condicional: dependências da equipa --------------------------------
_DEPENDENCIAS_DA_EQUIPA: tuple[str, ...] = (
    "src.caracteristicas.vetorizador_tfidf",   # P4 — Gleicy
    "src.dados.carregador_acordaos_json",       # P2 — Daniela
    "src.dados.esquemas",                       # P2/P8
    "src.dados.manifesto",                      # P8 — Pedro
    "src.pre_processamento.limpeza_texto",      # P3 — Gustavo
    "src.treino.classificador_mlp",             # P5 — Helton
)
_em_falta: list[str] = [
    nome for nome in _DEPENDENCIAS_DA_EQUIPA
    if _importlib_util.find_spec(nome) is None
]
if _em_falta:
    raise unittest.SkipTest(
        "Módulos da equipa ainda não disponíveis no main: " + ", ".join(_em_falta)
    )
# -----------------------------------------------------------------------------

import argparse
import io
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

import numpy as np
import torch

from src.caracteristicas.vetorizador_tfidf import VetorizadorTfidfNumPy
from src.dados.esquemas import Acordao
from src.dados.manifesto import escrever_manifesto
from src.inferencia.executar_inferencia import (
    _exibir_metricas_treino,
    _ficheiros_json,
    _processar_ficheiro,
    principal,
)
from src.inferencia.formatador_saida import ConfiguracaoSaida
from src.inferencia.motor_inferencia import MotorInferencia
from src.pre_processamento.limpeza_texto import limpar_texto
from src.treino.classificador_mlp import ClassificadorMLP


# --- Fixture LOCAL ---------------------------------------------------------
# Mapa canónico classe→índice (ADR-05).
_ID_PARA_CATEGORIA: dict[int, str] = {
    0: "MANTIDA", 1: "REVOGADA", 2: "ANULADA", 3: "NAO_CONHECIDA", 4: "OUTRA",
}
_CORPUS_TESTE: tuple[str, ...] = (
    "expropriacao utilidade publica reversao predio expropriado",
    "arrendamento despejo renda locatario incumprimento",
    "responsabilidade civil dano moral indemnizacao",
    "prescricao prazo contagem direito caducidade",
)


def _fabricar_execucao_de_teste(
    pasta_artefactos: str | Path,
    id_execucao: str = "execucao_teste",
    semente: int = 42,
    pasta_dados: str | Path | None = None,  # noqa: ARG001 (retrocompatibilidade)
) -> Path:
    """Cria uma execução completa em disco para o teste consumir.

    O modelo NÃO é treinado (pesos aleatórios com `semente`). Valida só a
    canalização do CLI. O parâmetro `pasta_dados` é ignorado.
    """
    pasta_execucao: Path = Path(pasta_artefactos) / id_execucao
    (pasta_execucao / "vetorizador").mkdir(parents=True, exist_ok=True)
    (pasta_execucao / "categorias").mkdir(parents=True, exist_ok=True)
    (pasta_execucao / "modelo").mkdir(parents=True, exist_ok=True)

    textos_limpos: list[str] = [limpar_texto(t) for t in _CORPUS_TESTE]
    vocabulario: dict[str, int] = {}
    for texto in textos_limpos:
        for token in texto.split():
            if token not in vocabulario:
                vocabulario[token] = len(vocabulario)
    frequencia_documento = np.zeros(len(vocabulario), dtype=np.float64)
    for texto in textos_limpos:
        for token in set(texto.split()):
            frequencia_documento[vocabulario[token]] += 1.0
    idf = np.log((1.0 + len(textos_limpos)) / (1.0 + frequencia_documento)) + 1.0

    vetorizador = VetorizadorTfidfNumPy(min_df=1, normalizar_l2=True)
    vetorizador.vocabulario = vocabulario
    vetorizador.idf = idf.astype(np.float32)
    vetorizador.esta_ajustado = True
    vetorizador.guardar(pasta_execucao / "vetorizador")

    (pasta_execucao / "categorias" / "id_para_categoria.json").write_text(
        json.dumps({str(i): c for i, c in _ID_PARA_CATEGORIA.items()},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    torch.manual_seed(semente)
    configuracao_modelo: dict[str, int] = {
        "dim_entrada": len(vocabulario), "dim_oculta": 16,
        "num_classes": len(_ID_PARA_CATEGORIA),
    }
    modelo = ClassificadorMLP.de_configuracao(configuracao_modelo)
    torch.save(modelo.state_dict(), pasta_execucao / "modelo" / "pesos.pth")
    (pasta_execucao / "modelo" / "configuracao_modelo.json").write_text(
        json.dumps(configuracao_modelo, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    (pasta_execucao / "metricas.json").write_text(
        json.dumps({"macro_f1_modelo": None, "macro_f1_baseline": None,
                    "nota": "fixture de teste"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    escrever_manifesto(
        id_execucao,
        {
            "id_execucao": id_execucao, "semente": semente,
            "vetorizador": "vetorizador/vocabulario.json",
            "idf": "vetorizador/idf.npy",
            "configuracao_vetorizador": "vetorizador/configuracao.json",
            "categorias": "categorias/id_para_categoria.json",
            "configuracao_modelo": "modelo/configuracao_modelo.json",
            "pesos": "modelo/pesos.pth",
            "metricas": "metricas.json",
        },
        pasta_artefactos,
    )
    return pasta_execucao
# --- fim da fixture --------------------------------------------------------


def _configuracao_texto() -> ConfiguracaoSaida:
    return ConfiguracaoSaida(
        usar_llm=False,
        formato="texto",
        url_base="",
        modelo="",
        chave_api=None,
        tempo_limite_segundos=5,
    )


def _motor_em_pasta(pasta: Path) -> MotorInferencia:
    _fabricar_execucao_de_teste(
        pasta_artefactos=pasta,
        id_execucao="execucao_cli",
        semente=42,
    )
    return MotorInferencia("execucao_cli", pasta_artefactos=pasta)


class TestFicheirosJson(unittest.TestCase):
    """_ficheiros_json: resolução de caminhos a partir de argumentos e .env."""

    def _args(self, ficheiro: str | None = None, pasta: str | None = None) -> argparse.Namespace:
        return argparse.Namespace(ficheiro_json=ficheiro, pasta_dados=pasta)

    def test_ficheiro_unico_devolvido_como_lista(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            caminho: Path = Path(tmp) / "acordao.json"
            caminho.write_text("{}", encoding="utf-8")
            resultado: list[Path] = _ficheiros_json(
                self._args(ficheiro=str(caminho)), "data"
            )
            self.assertEqual(resultado, [caminho])

    def test_pasta_devolvida_com_todos_os_jsons(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "a.json").write_text("{}", encoding="utf-8")
            (Path(tmp) / "b.json").write_text("{}", encoding="utf-8")
            (Path(tmp) / "c.txt").write_text("ignorar", encoding="utf-8")
            resultado = _ficheiros_json(self._args(pasta=tmp), "data")
            nomes: list[str] = [p.name for p in resultado]
            self.assertIn("a.json", nomes)
            self.assertIn("b.json", nomes)
            self.assertNotIn("c.txt", nomes)

    def test_pasta_vazia_devolve_lista_vazia(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            resultado = _ficheiros_json(self._args(pasta=tmp), "data")
            self.assertEqual(resultado, [])

    def test_pasta_do_env_usada_quando_nenhum_argumento(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "x.json").write_text("{}", encoding="utf-8")
            resultado = _ficheiros_json(self._args(), tmp)
            self.assertEqual(len(resultado), 1)
            self.assertEqual(resultado[0].name, "x.json")


class TestProcessarFicheiro(unittest.TestCase):
    """_processar_ficheiro: lê JSON, prevê, imprime para stdout."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self._pasta = Path(self._tmp.name)
        self._motor = _motor_em_pasta(self._pasta)
        self._configuracao = _configuracao_texto()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _json_acordao(self, nome: str = "teste.json") -> Path:
        """Cria um JSON mínimo válido para o carregador."""
        caminho: Path = self._pasta / nome
        caminho.write_text(
            json.dumps({
                "ecli": "ECLI:PT:STJ:2099:000",
                "descritores": "arrendamento; despejo;",
                "sumario_texto": "questão de arrendamento urbano",
                "decisao": "nega provimento",
                "year": 2099,
            }),
            encoding="utf-8",
        )
        return caminho

    def test_imprime_resultado_para_stdout(self) -> None:
        caminho: Path = self._json_acordao()
        saida = io.StringIO()
        with mock.patch("sys.stdout", saida):
            _processar_ficheiro(caminho, self._motor, self._configuracao)
        texto: str = saida.getvalue()
        self.assertIn("Resultado da inferência", texto)

    def test_ficheiro_json_vazio_nao_rebenta(self) -> None:
        """JSON vazio não produz acórdãos — deve pular silenciosamente."""
        caminho: Path = self._pasta / "vazio.json"
        caminho.write_text("[]", encoding="utf-8")
        # Não deve lançar excepção.
        _processar_ficheiro(caminho, self._motor, self._configuracao)

    def test_saida_contem_nome_do_ficheiro(self) -> None:
        caminho: Path = self._json_acordao("meu_acordao.json")
        saida = io.StringIO()
        with mock.patch("sys.stdout", saida):
            _processar_ficheiro(caminho, self._motor, self._configuracao)
        self.assertIn("meu_acordao.json", saida.getvalue())


class TestExibirMetricasTreino(unittest.TestCase):
    """_exibir_metricas_treino: três formatos e o caso sem métricas."""

    def _motor_com_metricas(self, metricas: dict[str, object]) -> MotorInferencia:
        with tempfile.TemporaryDirectory() as tmp:
            pasta = Path(tmp)
            _fabricar_execucao_de_teste(
                pasta_artefactos=pasta,
                id_execucao="execucao_metricas",
                semente=42,
            )
            (pasta / "execucao_metricas" / "metricas.json").write_text(
                json.dumps(metricas, ensure_ascii=False),
                encoding="utf-8",
            )
            motor = MotorInferencia("execucao_metricas", pasta_artefactos=pasta)
            # TemporaryDirectory já foi limpo — mas o motor já carregou tudo
            # em memória (metricas_treino), por isso podemos devolvê-lo.
            motor._pasta_tmp = tmp  # type: ignore[attr-defined]
            return motor

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self._pasta = Path(self._tmp.name)
        _fabricar_execucao_de_teste(
            pasta_artefactos=self._pasta,
            id_execucao="execucao_met",
            semente=42,
        )
        # Escrever métricas com valores reais para testar a exibição.
        (self._pasta / "execucao_met" / "metricas.json").write_text(
            json.dumps({
                "exatidao": 0.81,
                "macro_f1": 0.66,
                "macro_f1_referencia": 0.20,
                "nota": "exemplo de teste",
            }),
            encoding="utf-8",
        )
        self._motor = MotorInferencia("execucao_met", pasta_artefactos=self._pasta)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_formato_texto_contem_macro_f1(self) -> None:
        saida = io.StringIO()
        with mock.patch("sys.stdout", saida):
            _exibir_metricas_treino(self._motor, "texto")
        texto: str = saida.getvalue()
        self.assertIn("Macro-F1", texto)
        self.assertIn("66.00%", texto)

    def test_formato_markdown_tem_cabecalho(self) -> None:
        saida = io.StringIO()
        with mock.patch("sys.stdout", saida):
            _exibir_metricas_treino(self._motor, "markdown")
        self.assertIn("### Métricas do treino", saida.getvalue())

    def test_formato_json_parseavel(self) -> None:
        saida = io.StringIO()
        with mock.patch("sys.stdout", saida):
            _exibir_metricas_treino(self._motor, "json")
        parseado = json.loads(saida.getvalue())
        self.assertIn("metricas_treino", parseado)

    def test_sem_metricas_nao_imprime_nada(self) -> None:
        """Motor sem metricas_treino não deve imprimir nada."""
        self._motor.metricas_treino = None
        saida = io.StringIO()
        with mock.patch("sys.stdout", saida):
            _exibir_metricas_treino(self._motor, "texto")
        self.assertEqual(saida.getvalue(), "")

    def test_metricas_null_exibem_traco(self) -> None:
        """Métricas sem valores numéricos (null/None) mostram '—' em vez de crash."""
        self._motor.metricas_treino = {
            "macro_f1_modelo": None,
            "macro_f1_baseline": None,
            "nota": "scaffolding",
        }
        saida = io.StringIO()
        with mock.patch("sys.stdout", saida):
            _exibir_metricas_treino(self._motor, "texto")
        self.assertIn("—", saida.getvalue())


class TestPrincipal(unittest.TestCase):
    """principal(): código de retorno do CLI."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self._pasta_art = Path(self._tmp.name) / "artefactos"
        self._pasta_dados = Path(self._tmp.name) / "dados"
        self._pasta_dados.mkdir()
        _fabricar_execucao_de_teste(
            pasta_artefactos=self._pasta_art,
            id_execucao="execucao_cli_test",
            semente=42,
            pasta_dados=str(self._pasta_dados),
        )
        # JSON mínimo para o CLI processar.
        (self._pasta_dados / "acordao.json").write_text(
            json.dumps({
                "ecli": "ECLI:PT:STJ:2099:999",
                "descritores": "expropriação;",
                "sumario_texto": "questão de expropriação",
                "decisao": "nega provimento",
                "year": 2099,
            }),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_retorna_zero_com_dados_validos(self) -> None:
        argv: list[str] = [
            "executar_inferencia",
            "--id-execucao", "execucao_cli_test",
            "--pasta-artefactos", str(self._pasta_art),
            "--pasta-dados", str(self._pasta_dados),
        ]
        with mock.patch("sys.argv", argv), mock.patch("sys.stdout", io.StringIO()):
            codigo: int = principal()
        self.assertEqual(codigo, 0)

    def test_retorna_um_com_pasta_vazia(self) -> None:
        pasta_vazia: Path = Path(self._tmp.name) / "vazia"
        pasta_vazia.mkdir()
        argv: list[str] = [
            "executar_inferencia",
            "--id-execucao", "execucao_cli_test",
            "--pasta-artefactos", str(self._pasta_art),
            "--pasta-dados", str(pasta_vazia),
        ]
        with mock.patch("sys.argv", argv), mock.patch("sys.stdout", io.StringIO()):
            codigo = principal()
        self.assertEqual(codigo, 1)


if __name__ == "__main__":
    unittest.main()
