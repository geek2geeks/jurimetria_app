"""Testes do MotorInferencia (P7) — ponta a ponta sobre uma execução de teste."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
import torch

from src.caracteristicas.vetorizador_tfidf import VetorizadorTfidfNumPy
from src.dados.esquemas import Acordao
from src.dados.manifesto import escrever_manifesto
from src.inferencia.motor_inferencia import MotorInferencia
from src.pre_processamento.limpeza_texto import limpar_texto
from src.treino.classificador_mlp import ClassificadorMLP

CATEGORIAS_VALIDAS = {"MANTIDA", "REVOGADA", "ANULADA", "NAO_CONHECIDA", "OUTRA"}

# Mapa canónico classe→índice (ADR-05).
_ID_PARA_CATEGORIA: dict[int, str] = {
    0: "MANTIDA",
    1: "REVOGADA",
    2: "ANULADA",
    3: "NAO_CONHECIDA",
    4: "OUTRA",
}

# Corpus mínimo para alimentar o vocabulário durante os testes.
_CORPUS_TESTE: tuple[str, ...] = (
    "expropriacao utilidade publica reversao predio expropriado acto",
    "arrendamento despejo renda locatario incumprimento contratual",
    "responsabilidade civil dano moral indemnizacao prejuizo",
    "prescricao prazo contagem direito caducidade",
)


def _fabricar_execucao_de_teste(
    pasta_artefactos: str | Path,
    id_execucao: str = "execucao_teste",
    semente: int = 42,
) -> Path:
    """Fixture local: cria uma execução completa em disco para os testes."""

    pasta_execucao: Path = Path(pasta_artefactos) / id_execucao
    (pasta_execucao / "vetorizador").mkdir(parents=True, exist_ok=True)
    (pasta_execucao / "categorias").mkdir(parents=True, exist_ok=True)
    (pasta_execucao / "modelo").mkdir(parents=True, exist_ok=True)

    # 1. Vocabulário e IDF a partir do corpus de teste.
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
    vetorizador.guardar(pasta_execucao / "vetorizador")

    # 2. Mapa de categorias.
    (pasta_execucao / "categorias" / "id_para_categoria.json").write_text(
        json.dumps(
            {str(i): c for i, c in _ID_PARA_CATEGORIA.items()},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # 3. Modelo NÃO TREINADO + configuração.
    torch.manual_seed(semente)
    configuracao_modelo: dict[str, int] = {
        "dim_entrada": len(vocabulario),
        "dim_oculta": 16,
        "num_classes": len(_ID_PARA_CATEGORIA),
    }
    modelo = ClassificadorMLP.de_configuracao(configuracao_modelo)
    torch.save(modelo.state_dict(), pasta_execucao / "modelo" / "pesos.pth")
    (pasta_execucao / "modelo" / "configuracao_modelo.json").write_text(
        json.dumps(configuracao_modelo, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 4. Métricas placeholder.
    (pasta_execucao / "metricas.json").write_text(
        json.dumps(
            {
                "macro_f1_modelo": None,
                "macro_f1_baseline": None,
                "nota": "fixture de teste",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # 5. Manifesto.
    escrever_manifesto(
        id_execucao,
        {
            "id_execucao": id_execucao,
            "semente": semente,
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


class TestMotorInferencia(unittest.TestCase):
    def setUp(self) -> None:
        self._pasta_temporaria = tempfile.TemporaryDirectory()
        self.pasta_artefactos = Path(self._pasta_temporaria.name)
        _fabricar_execucao_de_teste(
            pasta_artefactos=self.pasta_artefactos,
            id_execucao="execucao_teste",
            semente=42,
        )
        self.motor = MotorInferencia(
            "execucao_teste", pasta_artefactos=self.pasta_artefactos
        )

    def tearDown(self) -> None:
        self._pasta_temporaria.cleanup()

    def test_preve_categoria_valida(self) -> None:
        acordao = Acordao(
            descritores=["arrendamento", "despejo"],
            sumario="questão de arrendamento urbano",
        )
        resultado = self.motor.prever(acordao)
        self.assertIn(resultado.categoria_prevista, CATEGORIAS_VALIDAS)
        # A classe prevista é a que tem maior probabilidade na distribuição.
        # Usar `max(items(), key=lambda p: p[1])` é mais explícito para o type
        # checker do que `max(dict, key=dict.get)` — `.get` retorna Optional.
        classe_mais_provavel: str = max(
            resultado.distribuicao.items(), key=lambda par: par[1]
        )[0]
        self.assertEqual(resultado.categoria_prevista, classe_mais_provavel)

    def test_previsao_e_determinista(self) -> None:
        acordao = Acordao(descritores=["prova"], sumario="onus da prova")
        primeira = self.motor.prever(acordao).categoria_prevista
        segunda = self.motor.prever(acordao).categoria_prevista
        self.assertEqual(primeira, segunda)

    def test_distribuicao_soma_aproximadamente_um(self) -> None:
        acordao = Acordao(descritores=["revista"], sumario="incumprimento contratual")
        soma = sum(self.motor.prever(acordao).distribuicao.values())
        self.assertAlmostEqual(soma, 1.0, places=4)

    def test_campos_de_fuga_nao_alteram_a_previsao(self) -> None:
        # Mesmos descritores+sumário; ecli/tribunal/decisao_bruta/texto_integral
        # diferentes → MESMA previsão. Prova que a fuga não entra nas features.
        # Os campos comuns são expandidos em cada Acordao em vez de **dict para
        # o type checker poder validar cada parâmetro individualmente.
        acordao_a = Acordao(
            ecli="ECLI:PT:STJ:2099:1",
            tribunal="STJ",
            decisao_bruta="negado provimento",
            texto_integral="o tribunal decide negar provimento",
            descritores=["arrendamento"],
            sumario="questão de arrendamento urbano",
        )
        acordao_b = Acordao(
            ecli="ECLI:PT:TRL:2099:2",
            tribunal="TRL",
            decisao_bruta="concedida a revista",
            texto_integral="o tribunal decide conceder a revista",
            descritores=["arrendamento"],
            sumario="questão de arrendamento urbano",
        )
        self.assertEqual(
            self.motor.prever(acordao_a).categoria_prevista,
            self.motor.prever(acordao_b).categoria_prevista,
        )

    def test_explicacao_offline_e_segura(self) -> None:
        acordao = Acordao(
            descritores=["arrendamento", "despejo"],
            sumario="questão de arrendamento",
        )
        resultado = self.motor.prever(acordao, com_explicacao=True)
        # Sequência standard para narrow de Optional ao type checker:
        # primeiro afirma-se que não é None, depois usa-se a variável tipada
        # como str na asserção seguinte.
        self.assertIsNotNone(resultado.explicacao_gerada)
        assert resultado.explicacao_gerada is not None
        self.assertIn(
            "não constitui aconselhamento jurídico",
            resultado.explicacao_gerada,
        )

    def test_execucao_inexistente_falha_claramente(self) -> None:
        with self.assertRaises(FileNotFoundError):
            MotorInferencia(
                "execucao_que_nao_existe", pasta_artefactos=self.pasta_artefactos
            )


class TestMotorInferenciaV13(unittest.TestCase):
    """Testes das funcionalidades adicionadas na v1.3:
    métricas do treino e termos relevantes.
    """

    def setUp(self) -> None:
        self._pasta_temporaria = tempfile.TemporaryDirectory()
        self.pasta_artefactos = Path(self._pasta_temporaria.name)
        _fabricar_execucao_de_teste(
            pasta_artefactos=self.pasta_artefactos,
            id_execucao="execucao_v13",
            semente=42,
        )
        self.motor = MotorInferencia(
            "execucao_v13", pasta_artefactos=self.pasta_artefactos
        )

    def tearDown(self) -> None:
        self._pasta_temporaria.cleanup()

    def test_metricas_treino_carregadas_como_dict_ou_none(self) -> None:
        """metricas_treino é None (sem métricas numéricas) ou dict válido."""
        self.assertTrue(
            self.motor.metricas_treino is None
            or isinstance(self.motor.metricas_treino, dict)
        )

    def test_metricas_treino_com_json_real(self) -> None:
        """Motor lê metricas.json real e expõe como dict."""
        import json

        metricas_reais = {
            "exatidao": 0.85,
            "macro_f1": 0.70,
            "macro_f1_referencia": 0.20,
        }
        caminho = self.pasta_artefactos / "execucao_v13" / "metricas.json"
        caminho.write_text(json.dumps(metricas_reais), encoding="utf-8")
        # Recarregar motor para ler o ficheiro actualizado.
        motor_novo = MotorInferencia(
            "execucao_v13", pasta_artefactos=self.pasta_artefactos
        )
        self.assertIsNotNone(motor_novo.metricas_treino)
        assert motor_novo.metricas_treino is not None
        # `metricas_treino` é `dict[str, object]` porque o JSON pode trazer
        # qualquer tipo. Validamos com `isinstance` antes de usar como número.
        macro_f1 = motor_novo.metricas_treino["macro_f1"]
        self.assertIsInstance(macro_f1, (int, float))
        assert isinstance(macro_f1, (int, float))
        self.assertAlmostEqual(macro_f1, 0.70)

    def test_termos_relevantes_e_lista(self) -> None:
        """prever() sempre devolve termos_relevantes como lista (pode ser vazia)."""
        acordao = Acordao(
            descritores=["expropriação", "utilidade pública"],
            sumario="reversão do prédio expropriado",
        )
        resultado = self.motor.prever(acordao)
        self.assertIsInstance(resultado.termos_relevantes, list)

    def test_excerto_sumario_limitado_a_400_caracteres(self) -> None:
        """excerto_sumario nunca excede 400 caracteres."""
        acordao = Acordao(
            descritores=["teste"],
            sumario="palavra " * 100,  # 800 caracteres
        )
        resultado = self.motor.prever(acordao)
        self.assertLessEqual(len(resultado.excerto_sumario), 400)

    def test_acordao_sem_sumario_nao_rebenta(self) -> None:
        """Acordao só com descritores (sumario=None) deve funcionar."""
        acordao = Acordao(descritores=["expropriação"], sumario=None)
        resultado = self.motor.prever(acordao)
        self.assertIn(resultado.categoria_prevista, CATEGORIAS_VALIDAS)

    def test_acordao_completamente_vazio_nao_rebenta(self) -> None:
        """Acordao sem descritores nem sumário devolve categoria válida."""
        acordao = Acordao(descritores=[], sumario=None)
        resultado = self.motor.prever(acordao)
        self.assertIn(resultado.categoria_prevista, CATEGORIAS_VALIDAS)


if __name__ == "__main__":
    unittest.main()
