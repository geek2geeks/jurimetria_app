"""[ENTREGA-3] Testes da persistência da execução — Sandro Tarabay.

Prova a costura treino -> inferência: o que `guardar_execucao` escreve é
exactamente o que `MotorInferencia` consegue reconstruir.

Dados sintéticos apenas (constituição §5). Sem rede.

Comando:
    python -m unittest tests/test_persistencia_execucao.py -v
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

try:
    import torch

    from src.caracteristicas.vetorizador_tfidf import VetorizadorTfidfNumPy
    from src.dados.esquemas import Acordao
    from src.dados.manifesto import ler_manifesto
    from src.inferencia.motor_inferencia import MotorInferencia
    from src.modelos.rede_neuronal import RedeNeuronalClassificacao
    from src.treino.persistencia_execucao import guardar_execucao
except ImportError as erro:  # pragma: no cover
    raise unittest.SkipTest(
        f"Dependência em falta para os testes de persistência: {erro}"
    ) from erro


SEMENTE = 42
ID_EXECUCAO = "execucao_costura"

_CORPUS = [
    "recurso provimento decisao revogada tribunal",
    "recurso negado provimento decisao mantida",
    "sentenca anulada nulidade processo",
    "recurso nao conhecido extemporaneo",
    "processo extinto outra decisao",
]
_CATEGORIAS = ["REVOGADA", "MANTIDA", "ANULADA", "NAO_CONHECIDA", "OUTRA"]


def _vetorizador_ajustado() -> VetorizadorTfidfNumPy:
    vetorizador = VetorizadorTfidfNumPy()
    vetorizador.fit(_CORPUS)
    mapa_categoria, mapa_id = vetorizador._construir_mapas_categorias(_CATEGORIAS)
    vetorizador.mapa_categoria_para_id = mapa_categoria
    vetorizador.mapa_id_para_categoria = mapa_id
    return vetorizador


class TestPersistenciaExecucao(unittest.TestCase):
    def setUp(self) -> None:
        self._temporaria = tempfile.TemporaryDirectory()
        self.pasta_artefactos = Path(self._temporaria.name)

        self.vetorizador = _vetorizador_ajustado()
        self.numero_entradas = len(self.vetorizador.vocabulario)
        self.numero_saidas = len(self.vetorizador.mapa_id_para_categoria)

        torch.manual_seed(SEMENTE)
        self.rede = RedeNeuronalClassificacao(
            entrada=self.numero_entradas,
            oculta=16,
            saida=self.numero_saidas,
        )

        self.pasta_execucao = guardar_execucao(
            id_execucao=ID_EXECUCAO,
            rede=self.rede,
            vetorizador=self.vetorizador,
            dimensoes={
                "numero_entradas": self.numero_entradas,
                "numero_ocultas": 16,
                "numero_saidas": self.numero_saidas,
            },
            metricas={"exatidao": 1.0, "nota": "execução sintética de teste"},
            semente=SEMENTE,
            pasta_artefactos=self.pasta_artefactos,
        )

    def tearDown(self) -> None:
        self._temporaria.cleanup()

    def test_estrutura_da_constituicao_e_respeitada(self) -> None:
        for relativo in (
            "manifesto.json",
            "metricas.json",
            "modelo/pesos.pth",
            "modelo/configuracao_modelo.json",
            "vetorizador/vocabulario.json",
            "vetorizador/idf.npy",
            "categorias/id_para_categoria.json",
        ):
            with self.subTest(relativo=relativo):
                self.assertTrue((self.pasta_execucao / relativo).is_file())

    def test_manifesto_aponta_para_ficheiros_existentes(self) -> None:
        manifesto = ler_manifesto(ID_EXECUCAO, self.pasta_artefactos)
        for chave in ("vetorizador", "idf", "categorias", "configuracao_modelo", "pesos"):
            with self.subTest(chave=chave):
                self.assertTrue(
                    (self.pasta_execucao / str(manifesto[chave])).is_file()
                )

    def test_pesos_tem_o_prefixo_do_involucro(self) -> None:
        """Sem o prefixo `rede.`, o load_state_dict do motor rejeita o ficheiro."""
        estado = torch.load(
            self.pasta_execucao / "modelo" / "pesos.pth",
            map_location="cpu",
            weights_only=True,
        )
        self.assertTrue(all(chave.startswith("rede.") for chave in estado))

    def test_configuracao_serve_as_duas_familias_de_chaves(self) -> None:
        configuracao = json.loads(
            (self.pasta_execucao / "modelo" / "configuracao_modelo.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(configuracao["numero_entradas"], configuracao["dim_entrada"])
        self.assertEqual(configuracao["numero_ocultas"], configuracao["dim_oculta"])
        self.assertEqual(configuracao["numero_saidas"], configuracao["num_classes"])

    def test_motor_reconstroi_a_execucao(self) -> None:
        """O coração do ENTREGA-3: a inferência carrega o que o treino gravou."""
        motor = MotorInferencia(ID_EXECUCAO, self.pasta_artefactos)
        self.assertEqual(self.numero_saidas, len(motor.id_para_categoria))
        self.assertEqual(self.numero_entradas, len(motor.vetorizador.vocabulario))

    def test_previsao_devolve_categoria_valida(self) -> None:
        motor = MotorInferencia(ID_EXECUCAO, self.pasta_artefactos)
        acordao = Acordao(
            ecli="ECLI:PT:STA:2020:TESTE",
            descritores=["recurso", "provimento"],
            sumario="Concedido provimento ao recurso.",
        )
        resultado = motor.prever(acordao)
        self.assertIn(resultado.categoria_prevista, _CATEGORIAS)
        self.assertAlmostEqual(1.0, sum(resultado.distribuicao.values()), places=4)

    def test_vetorizador_nao_ajustado_e_rejeitado(self) -> None:
        with self.assertRaises(ValueError):
            guardar_execucao(
                id_execucao="execucao_invalida",
                rede=self.rede,
                vetorizador=VetorizadorTfidfNumPy(),
                dimensoes={
                    "numero_entradas": 1,
                    "numero_ocultas": 1,
                    "numero_saidas": 1,
                },
                pasta_artefactos=self.pasta_artefactos,
            )

    def test_dimensoes_em_falta_sao_rejeitadas(self) -> None:
        with self.assertRaises(ValueError):
            guardar_execucao(
                id_execucao="execucao_invalida",
                rede=self.rede,
                vetorizador=self.vetorizador,
                dimensoes={"numero_entradas": 10},
                pasta_artefactos=self.pasta_artefactos,
            )


if __name__ == "__main__":
    unittest.main()
