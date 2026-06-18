"""Testes do vetorizador TF-IDF com NumPy.

Cobre:
- Cálculo exato do TF-IDF para uma frase curta.
- Vocabulário criado apenas com dados de treino.
- `transform` mantém o mesmo número de colunas.
- Conversão de categorias para índices.
- Guardar e reler artefactos (vocabulario.json, idf.npy, categoria_para_id.json).
- Divisão treino/teste estratificada e reprodutível.
- Fuga de informação: `fit` não pode ser aplicado sobre todos os dados.
"""
from __future__ import annotations

import json
import os
import tempfile
import unittest

import numpy as np

from src.caracteristicas.vetorizador_tfidf import (
    PROPORCAO_TESTE_PADRAO,
    SEMENTE_PADRAO,
    VetorizadorTfidfNumPy,
    _dividir_treino_teste,
)
from src.dados.esquemas import RegistoClassificacao


def _criar_registos(
    textos_categorias: list[tuple[str, str]]
) -> list[RegistoClassificacao]:
    """Auxiliar: cria uma lista de `RegistoClassificacao` a partir de tuplos."""
    return [
        RegistoClassificacao(
            id_documento=f"documento_{i:03d}",
            texto=texto,
            categoria_normalizada=categoria,
        )
        for i, (texto, categoria) in enumerate(textos_categorias)
    ]


class TestDividirTreinoTeste(unittest.TestCase):
    """Testes da função de divisão treino/teste com NumPy."""

    def test_divisao_respeita_proporcao(self) -> None:
        registos = _criar_registos(
            [("texto a", "MANTIDA") for _ in range(50)]
            + [("texto b", "REVOGADA") for _ in range(50)]
        )
        treino, teste = _dividir_treino_teste(
            registos, proporcao_teste=0.2, semente=42
        )
        self.assertEqual(80, len(treino))
        self.assertEqual(20, len(teste))

    def test_divisao_mantem_ambas_categorias_nos_dois_subconjuntos(self) -> None:
        registos = _criar_registos(
            [("texto a", "MANTIDA") for _ in range(10)]
            + [("texto b", "REVOGADA") for _ in range(10)]
        )
        treino, teste = _dividir_treino_teste(
            registos, proporcao_teste=0.3, semente=42
        )
        categorias_treino = {r.categoria_normalizada for r in treino}
        categorias_teste = {r.categoria_normalizada for r in teste}
        self.assertIn("MANTIDA", categorias_treino)
        self.assertIn("REVOGADA", categorias_treino)
        self.assertIn("MANTIDA", categorias_teste)
        self.assertIn("REVOGADA", categorias_teste)

    def test_divisao_reprodutivel(self) -> None:
        registos = _criar_registos(
            [("texto a", "MANTIDA") for _ in range(30)]
            + [("texto b", "REVOGADA") for _ in range(20)]
        )
        treino1, teste1 = _dividir_treino_teste(registos, semente=42)
        treino2, teste2 = _dividir_treino_teste(registos, semente=42)
        textos_treino1 = sorted(r.texto for r in treino1)
        textos_treino2 = sorted(r.texto for r in treino2)
        self.assertEqual(textos_treino1, textos_treino2)

    def test_divisao_sementes_diferentes(self) -> None:
        registos = _criar_registos(
            [("texto a", "MANTIDA") for _ in range(50)]
            + [("texto b", "REVOGADA") for _ in range(50)]
        )
        treino1, _ = _dividir_treino_teste(registos, semente=42)
        treino2, _ = _dividir_treino_teste(registos, semente=123)
        ids1 = sorted(r.id_documento for r in treino1)
        ids2 = sorted(r.id_documento for r in treino2)
        self.assertNotEqual(ids1, ids2)

    def test_divisao_lista_vazia_lanca_erro(self) -> None:
        with self.assertRaises(ValueError):
            _dividir_treino_teste([], semente=42)

    def test_divisao_proporcao_invalida_lanca_erro(self) -> None:
        registos = _criar_registos([("texto", "MANTIDA")])
        with self.assertRaises(ValueError):
            _dividir_treino_teste(registos, proporcao_teste=0.0)
        with self.assertRaises(ValueError):
            _dividir_treino_teste(registos, proporcao_teste=1.0)


class TestVetorizadorTfidfNumPy(unittest.TestCase):
    """Testes da classe principal do vetorizador TF-IDF."""

    def setUp(self) -> None:
        self.vetorizador = VetorizadorTfidfNumPy()

    def test_fit_sem_textos_lanca_erro(self) -> None:
        with self.assertRaises(ValueError):
            self.vetorizador.fit([])

    def test_transform_sem_fit_lanca_erro(self) -> None:
        with self.assertRaises(RuntimeError):
            self.vetorizador.transform(["texto"])

    def test_vocabulario_criado_apenas_no_fit(self) -> None:
        textos = ["juiz nega recurso", "tribunal concede recurso", "juiz mantem decisao"]
        self.vetorizador.fit(textos)
        self.assertTrue(self.vetorizador.esta_ajustado)
        self.assertIn("juiz", self.vetorizador.vocabulario)
        self.assertIn("recurso", self.vetorizador.vocabulario)
        self.assertIn("decisao", self.vetorizador.vocabulario)

    def test_transform_mantem_numero_colunas(self) -> None:
        textos_treino = ["juiz nega recurso", "tribunal concede recurso"]
        textos_teste = ["juiz mantem decisao"]

        self.vetorizador.fit(textos_treino)
        matriz_treino = self.vetorizador.transform(textos_treino)
        matriz_teste = self.vetorizador.transform(textos_teste)

        self.assertEqual(matriz_treino.shape[1], matriz_teste.shape[1])
        self.assertEqual(len(self.vetorizador.vocabulario), matriz_teste.shape[1])

    def test_tokens_desconhecidos_ignorados(self) -> None:
        textos_treino = ["a b c"]
        textos_teste = ["a x y z"]

        self.vetorizador.fit(textos_treino)
        matriz_teste = self.vetorizador.transform(textos_teste)

        # Apenas o token "a" é conhecido; os outros são ignorados.
        self.assertEqual((1, 3), matriz_teste.shape)
        self.assertGreater(matriz_teste[0, self.vetorizador.vocabulario["a"]], 0.0)
        # As colunas de "b" e "c" devem ser zero para o documento de teste.
        self.assertEqual(0.0, matriz_teste[0, self.vetorizador.vocabulario["b"]])
        self.assertEqual(0.0, matriz_teste[0, self.vetorizador.vocabulario["c"]])

    def test_calculo_tfidf_manual(self) -> None:
        """Verifica o cálculo do TF-IDF contra valores obtidos manualmente.

        Dois documentos:
          d1: "a a b"
          d2: "a c"
        Vocabulário: ["a", "b", "c"]

        IDF:
          df("a") = 2 → idf = log((2+1)/(2+1)) + 1 = log(1) + 1 = 1.0
          df("b") = 1 → idf = log((2+1)/(1+1)) + 1 = log(3/2) + 1 ≈ 1.405...
          df("c") = 1 → idf = log((2+1)/(1+1)) + 1 = log(3/2) + 1 ≈ 1.405...

        TF (normalizado por comprimento do documento):
          d1: comprimento=3 → tf("a")=2/3, tf("b")=1/3, tf("c")=0
          d2: comprimento=2 → tf("a")=1/2, tf("b")=0,   tf("c")=1/2

        TF-IDF:
          d1: a=2/3*1.0=0.666..., b=1/3*1.405...≈0.468..., c=0
          d2: a=1/2*1.0=0.5,     b=0,                 c=1/2*1.405...≈0.702...
        """
        textos = ["a a b", "a c"]
        self.vetorizador.fit(textos)
        matriz = self.vetorizador.transform(textos)

        voc = self.vetorizador.vocabulario

        # Verifica que o vocabulário tem 3 tokens ordenados alfabeticamente.
        self.assertEqual(3, len(voc))
        self.assertEqual(["a", "b", "c"], sorted(voc.keys()))

        indice_a = voc["a"]
        indice_b = voc["b"]
        indice_c = voc["c"]

        self.assertAlmostEqual(2 / 3, matriz[0, indice_a], places=4)
        self.assertAlmostEqual(1 / 3 * (np.log(3 / 2) + 1), matriz[0, indice_b], places=4)
        self.assertEqual(0.0, matriz[0, indice_c])

        self.assertAlmostEqual(0.5, matriz[1, indice_a], places=4)
        self.assertEqual(0.0, matriz[1, indice_b])
        self.assertAlmostEqual(0.5 * (np.log(3 / 2) + 1), matriz[1, indice_c], places=4)

    def test_fit_transform_equivale_fit_seguido_transform(self) -> None:
        textos = ["a b c", "b c d"]

        vet1 = VetorizadorTfidfNumPy()
        matriz1 = vet1.fit_transform(textos)

        vet2 = VetorizadorTfidfNumPy()
        vet2.fit(textos)
        matriz2 = vet2.transform(textos)

        np.testing.assert_array_equal(matriz1, matriz2)

    def test_fit_transform_documento_vazio(self) -> None:
        """Documento vazio não deve causar divisão por zero."""
        textos = ["a b", ""]
        self.vetorizador.fit(textos)
        matriz = self.vetorizador.transform(textos)
        self.assertEqual((2, len(self.vetorizador.vocabulario)), matriz.shape)
        # Documento vazio deve ter todos os valores a zero.
        np.testing.assert_array_equal(np.zeros(len(self.vetorizador.vocabulario)), matriz[1])

    def test_mapa_categorias_construido_corretamente(self) -> None:
        textos = ["a b", "c d"]
        self.vetorizador.fit(textos)
        mapa_cat, mapa_id = self.vetorizador._construir_mapas_categorias(
            ["MANTIDA", "REVOGADA", "ANULADA"]
        )
        self.assertEqual(3, len(mapa_cat))
        self.assertEqual(3, len(mapa_id))
        self.assertEqual(0, mapa_cat["ANULADA"])
        self.assertEqual("ANULADA", mapa_id[0])
        self.assertEqual(1, mapa_cat["MANTIDA"])
        self.assertEqual(2, mapa_cat["REVOGADA"])

    def test_guardar_e_carregar_artefactos(self) -> None:
        textos = ["juiz nega recurso", "tribunal concede recurso", "juiz mantem decisao"]
        self.vetorizador.fit(textos)
        self.vetorizador.mapa_categoria_para_id = {"MANTIDA": 0, "REVOGADA": 1}
        self.vetorizador.mapa_id_para_categoria = {0: "MANTIDA", 1: "REVOGADA"}

        with tempfile.TemporaryDirectory() as tmp:
            self.vetorizador.guardar_artefactos(tmp)

            # Verifica que os ficheiros existem.
            self.assertTrue(os.path.isfile(os.path.join(tmp, "vocabulario.json")))
            self.assertTrue(os.path.isfile(os.path.join(tmp, "idf.npy")))
            self.assertTrue(os.path.isfile(os.path.join(tmp, "categoria_para_id.json")))
            self.assertTrue(os.path.isfile(os.path.join(tmp, "id_para_categoria.json")))

            # Relê os artefactos.
            vetorizador_carregado = VetorizadorTfidfNumPy.carregar_artefactos(tmp)

            self.assertTrue(vetorizador_carregado.esta_ajustado)
            self.assertEqual(
                self.vetorizador.vocabulario, vetorizador_carregado.vocabulario
            )
            np.testing.assert_array_equal(self.vetorizador.idf, vetorizador_carregado.idf)
            self.assertEqual(
                self.vetorizador.mapa_categoria_para_id,
                vetorizador_carregado.mapa_categoria_para_id,
            )
            self.assertEqual(
                self.vetorizador.mapa_id_para_categoria,
                vetorizador_carregado.mapa_id_para_categoria,
            )

            # Confirma que o vetorizador carregado transforma corretamente.
            matriz_original = self.vetorizador.transform(textos)
            matriz_carregada = vetorizador_carregado.transform(textos)
            np.testing.assert_array_equal(matriz_original, matriz_carregada)

    def test_guardar_sem_fit_lanca_erro(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RuntimeError):
                self.vetorizador.guardar_artefactos(tmp)

    def test_processar_registos_integra(self) -> None:
        """Teste de integração do fluxo completo processar_registos."""
        registos = _criar_registos(
            [("a b c", "MANTIDA") for _ in range(10)]
            + [("d e f", "REVOGADA") for _ in range(10)]
        )
        vet = VetorizadorTfidfNumPy()
        x_treino, x_teste, y_treino, y_teste = vet.processar_registos(
            registos, proporcao_teste=0.3, semente=42
        )

        self.assertTrue(vet.esta_ajustado)
        self.assertEqual(2, len(vet.mapa_categoria_para_id))
        self.assertGreater(x_treino.shape[0], 0)
        self.assertGreater(x_teste.shape[0], 0)
        self.assertEqual(x_treino.shape[1], x_teste.shape[1])
        self.assertEqual(x_treino.shape[0], y_treino.shape[0])
        self.assertEqual(x_teste.shape[0], y_teste.shape[0])

        # Categorias devem ser índices inteiros.
        self.assertTrue(np.issubdtype(y_treino.dtype, np.integer))
        self.assertTrue(np.issubdtype(y_teste.dtype, np.integer))

    def test_fit_sem_vazar_informacao_teste(self) -> None:
        """O vocabulário não deve conter tokens exclusivos do teste.

        Simula manualmente o que `processar_registos` faz: divide, aplica `fit`
        apenas nos textos de treino e verifica que tokens só presentes no teste
        estão ausentes do vocabulário.
        """
        textos_treino = ["palavra_treino unica", "termo_adicional"]
        textos_teste = ["palavra_teste exclusiva"]

        vet = VetorizadorTfidfNumPy()
        vet.fit(textos_treino)

        self.assertIn("palavra_treino", vet.vocabulario)
        self.assertIn("unica", vet.vocabulario)
        self.assertIn("termo_adicional", vet.vocabulario)
        self.assertNotIn("palavra_teste", vet.vocabulario)
        self.assertNotIn("exclusiva", vet.vocabulario)

        # O transform sobre o teste deve funcionar sem erros.
        matriz_teste = vet.transform(textos_teste)
        self.assertEqual((1, 3), matriz_teste.shape)

    def test_processar_registos_reprodutivel(self) -> None:
        registos = _criar_registos(
            [("a b", "MANTIDA") for _ in range(10)]
            + [("c d", "REVOGADA") for _ in range(10)]
        )
        vet1 = VetorizadorTfidfNumPy()
        x1, _, y1, _ = vet1.processar_registos(registos, semente=42)

        vet2 = VetorizadorTfidfNumPy()
        x2, _, y2, _ = vet2.processar_registos(registos, semente=42)

        np.testing.assert_array_equal(x1, x2)
        np.testing.assert_array_equal(y1, y2)

    def test_processar_registos_categorias_indices_consistentes(self) -> None:
        registos = _criar_registos(
            [("a", "MANTIDA"), ("b", "MANTIDA"), ("c", "REVOGADA"), ("d", "REVOGADA")]
        )
        vet = VetorizadorTfidfNumPy()
        _, _, y_treino, _ = vet.processar_registos(registos, semente=42)

        indices_unicos = set(y_treino.tolist())
        self.assertEqual(2, len(indices_unicos))


if __name__ == "__main__":
    unittest.main()
