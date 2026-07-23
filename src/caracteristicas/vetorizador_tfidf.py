"""Vetorizador TF-IDF com NumPy puro.

Converte uma lista de `RegistoClassificacao` em matrizes NumPy de características
e categorias, com divisão treino/teste reprodutível e exportação de artefactos
MLOps.

Regra crítica (constitution.md §5, ADR-02):
    O `fit` ocorre estritamente nos textos de treino. Validação, teste e
    inferência usam apenas `transform`. Isto impede que informação do
    conjunto de teste contamine o vocabulário e os pesos IDF.
"""
from __future__ import annotations

import json
import os
from typing import Optional

import numpy as np

from src.dados.esquemas import RegistoClassificacao

SEMENTE_PADRAO: int = 42
PROPORCAO_TESTE_PADRAO: float = 0.2

CLASSES_CANONICAS: list[str] = [
    "ANULADA",
    "MANTIDA",
    "NAO_CONHECIDA",
    "OUTRA",
    "REVOGADA",
]

def _dividir_treino_teste(
    registos: list[RegistoClassificacao],
    proporcao_teste: float = PROPORCAO_TESTE_PADRAO,
    semente: int = SEMENTE_PADRAO,
) -> tuple[list[RegistoClassificacao], list[RegistoClassificacao]]:
    """Divide a lista de registos em treino e teste usando NumPy.

    A divisão é estratificada por categoria para manter a distribuição das
    classes nos dois subconjuntos. Usa uma semente fixa para garantir
    reprodutibilidade.

    Args:
        registos: Lista de instâncias `RegistoClassificacao`.
        proporcao_teste: Fração dos dados reservada para teste (0 < p < 1).
        semente: Semente para o gerador aleatório do NumPy.

    Returns:
        Tuplo (treino, teste) com as duas listas de registos.
    """
    if not registos:
        raise ValueError("A lista de registos nao pode estar vazia.")
    if not (0.0 < proporcao_teste < 1.0):
        raise ValueError("A proporcao_teste deve estar entre 0 e 1, exclusivo.")

    gerador = np.random.default_rng(semente)
    indices = np.arange(len(registos))

    categorias = np.array([r.categoria_normalizada for r in registos])
    classes_unicas = np.unique(categorias)

    indices_treino: list[int] = []
    indices_teste: list[int] = []

    for classe in classes_unicas:
        mascara = categorias == classe
        indices_classe = indices[mascara]
        gerador.shuffle(indices_classe)
        n_teste = max(1, int(len(indices_classe) * proporcao_teste))
        indices_teste.extend(indices_classe[:n_teste].tolist())
        indices_treino.extend(indices_classe[n_teste:].tolist())

    treino = [registos[i] for i in indices_treino]
    teste = [registos[i] for i in indices_teste]

    # Reembaralha para evitar que os dados fiquem agrupados por classe.
    gerador.shuffle(indices_treino)
    gerador.shuffle(indices_teste)
    treino = [registos[i] for i in indices_treino]
    teste = [registos[i] for i in indices_teste]

    return treino, teste


class VetorizadorTfidfNumPy:
    """Vetorizador TF-IDF implementado exclusivamente com NumPy.

    Aprende o vocabulário e os pesos IDF a partir dos textos de treino e
    transforma qualquer lista de textos numa matriz NumPy de características.

    Atributos:
        vocabulario (dict[str, int]): Mapeia cada token para o índice da coluna.
        idf (np.ndarray): Vetor de pesos IDF com dimensão (n_tokens,).
        esta_ajustado (bool): Indica se o `fit` já foi executado.
        mapa_categoria_para_id (dict[str, int]): Mapeia categoria para índice.
        mapa_id_para_categoria (dict[int, str]): Mapeia índice para categoria.
    """

    def __init__(
        self,
        min_df: int = 1,
        normalizar_l2: bool = True,
        **kwargs: object,
    ) -> None:
        self.min_df = min_df
        self.normalizar_l2 = normalizar_l2
        self.vocabulario: dict[str, int] = {}
        self.idf: Optional[np.ndarray] = None
        self.esta_ajustado: bool = False
        self.mapa_categoria_para_id: dict[str, int] = {}
        self.mapa_id_para_categoria: dict[int, str] = {}

    def _tokenizar(self, texto: str) -> list[str]:
        """Divide um texto numa lista de tokens por espacos em branco.

        Args:
            texto: String a tokenizar.

        Returns:
            Lista de tokens (palavras).
        """
        return texto.strip().split()

    def _construir_vocabulario(self, textos: list[str]) -> dict[str, int]:
        """Constrói o dicionário de tokens a partir de uma lista de textos.

        Args:
            textos: Lista de strings de treino.

        Returns:
            Dicionário que mapeia cada token único para um índice de coluna.
        """
        tokens_unicos: set[str] = set()
        for texto in textos:
            tokens_unicos.update(self._tokenizar(texto))
        return {token: indice for indice, token in enumerate(sorted(tokens_unicos))}

    def _construir_matriz_contagens(self, textos: list[str]) -> np.ndarray:
        """Constrói a matriz de contagens de termos (Bag-of-Words).

        Cada linha corresponde a um documento, cada coluna a um token do
        vocabulário.

        Args:
            textos: Lista de strings.

        Returns:
            Matriz NumPy de forma (n_documentos, n_tokens) com as contagens.
        """
        n_documentos = len(textos)
        n_tokens = len(self.vocabulario)
        matriz = np.zeros((n_documentos, n_tokens), dtype=np.float64)

        for i, texto in enumerate(textos):
            for token in self._tokenizar(texto):
                if token in self.vocabulario:
                    matriz[i, self.vocabulario[token]] += 1

        return matriz

    def fit(self, textos: list[str]) -> VetorizadorTfidfNumPy:
        """Aprende o vocabulário e calcula os pesos IDF a partir dos textos.

        Este método só deve ser invocado sobre os textos de treino. Usar sobre
        o conjunto completo antes da divisão constitui fuga de informação.

        Args:
            textos: Lista de strings de treino.

        Returns:
            A própria instância (permite encadeamento).
        """
        if not textos:
            raise ValueError("A lista de textos de treino nao pode estar vazia.")

        self.vocabulario = self._construir_vocabulario(textos)

        matriz_contagens = self._construir_matriz_contagens(textos)
        n_documentos = matriz_contagens.shape[0]

        # Frequência documental: número de documentos que contêm cada token.
        frequencia_documental = np.count_nonzero(matriz_contagens, axis=0)

        # IDF suave: log((N + 1) / (df + 1)) + 1
        self.idf = np.log((n_documentos + 1) / (frequencia_documental + 1)) + 1

        self.esta_ajustado = True
        return self

    def transform(self, textos: list[str]) -> np.ndarray:
        """Transforma uma lista de textos na matriz TF-IDF.

        Usa o vocabulário e os pesos IDF aprendidos durante o `fit`.
        Tokens desconhecidos são ignorados silenciosamente.

        Args:
            textos: Lista de strings a transformar.

        Returns:
            Matriz NumPy de forma (n_documentos, n_tokens) com os valores
            TF-IDF.

        Raises:
            RuntimeError: Se `fit` ainda não tiver sido executado.
        """
        if not self.esta_ajustado:
            raise RuntimeError(
                "O vetorizador ainda nao foi ajustado. Execute fit() primeiro."
            )

        matriz_contagens = self._construir_matriz_contagens(textos)
        n_documentos = matriz_contagens.shape[0]

        # TF normalizado por documento (comprimento do documento em tokens).
        comprimentos = matriz_contagens.sum(axis=1, keepdims=True)
        # Evita divisão por zero em documentos vazios.
        comprimentos = np.where(comprimentos == 0, 1, comprimentos)
        tf = matriz_contagens / comprimentos

        return tf * self.idf

    def fit_transform(self, textos: list[str]) -> np.ndarray:
        """Ajusta o vetorizador e transforma os mesmos textos.

        Método de conveniência para os dados de treino. Equivale a chamar
        `fit(textos)` seguido de `transform(textos)`.

        Args:
            textos: Lista de strings de treino.

        Returns:
            Matriz NumPy TF-IDF de forma (n_documentos, n_tokens).
        """
        self.fit(textos)
        return self.transform(textos)

    def _construir_mapas_categorias(
        self, categorias: list[str]
    ) -> tuple[dict[str, int], dict[int, str]]:
        """Constrói os mapas utilizando as classes canónicas do projeto."""
        categorias_invalidas = set(categorias) - set(CLASSES_CANONICAS)
        if categorias_invalidas:
            raise ValueError(
                f"Categorias desconhecidas encontradas: {sorted(categorias_invalidas)}"
            )
        categoria_para_id = {
            categoria: indice
            for indice, categoria in enumerate(CLASSES_CANONICAS)
        }
        id_para_categoria = {
            indice: categoria
            for indice, categoria in enumerate(CLASSES_CANONICAS)
        }

        return categoria_para_id, id_para_categoria

    def _categorias_para_indices(self, categorias: list[str]) -> np.ndarray:
        """Converte uma lista de categorias textuais num vetor de índices.

        Args:
            categorias: Lista de strings de categorias normalizadas.

        Returns:
            Vetor NumPy de inteiros com forma (n_amostras,).
        """
        categorias_invalidas = [
            c for c in categorias
            if c not in self.mapa_categoria_para_id
        ]
        if categorias_invalidas:
            raise ValueError(
                f"Categorias não suportadas: {categorias_invalidas}"
            )
        return np.array(
            [self.mapa_categoria_para_id[c] for c in categorias], dtype=np.int64,
        )

    def processar_registos(
        self,
        registos: list[RegistoClassificacao],
        proporcao_teste: float = PROPORCAO_TESTE_PADRAO,
        semente: int = SEMENTE_PADRAO,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Processa uma lista de registos e devolve as matrizes de treino e teste.

        Executa a pipeline completa: divisão treino/teste, construção dos mapas
        de categorias, ajuste do vocabulário e IDF nos textos de treino, e
        transformação de ambos os subconjuntos.

        Args:
            registos: Lista de instâncias `RegistoClassificacao`.
            proporcao_teste: Fração dos dados reservada para teste.
            semente: Semente para reprodutibilidade da divisão.

        Returns:
            Tuplo com quatro matrizes NumPy:
            - caracteristicas_treino: forma (n_treino, n_tokens)
            - caracteristicas_teste: forma (n_teste, n_tokens)
            - categorias_treino: forma (n_treino,) — índices inteiros
            - categorias_teste: forma (n_teste,) — índices inteiros
        """
        treino, teste = _dividir_treino_teste(registos, proporcao_teste, semente)

        textos_treino = [r.texto for r in treino]
        textos_teste = [r.texto for r in teste]
        categorias_treino_str = [r.categoria_normalizada for r in treino]
        categorias_teste_str = [r.categoria_normalizada for r in teste]

        # Os mapas de categorias utilizam as classes canónicas definidas
        # pela Constituição do Projeto, garantindo estabilidade entre
        # treino, inferência e exportação de artefactos.
        self.mapa_categoria_para_id, self.mapa_id_para_categoria = (
            self._construir_mapas_categorias(categorias_treino_str)
        )

        # O fit é executado exclusivamente nos textos de treino para evitar
        # fuga de informação do conjunto de teste para o vocabulário e IDF.
        self.fit(textos_treino)

        caracteristicas_treino = self.transform(textos_treino)
        caracteristicas_teste = self.transform(textos_teste)

        categorias_treino = self._categorias_para_indices(categorias_treino_str)
        categorias_teste = self._categorias_para_indices(categorias_teste_str)

        return (
            caracteristicas_treino,
            caracteristicas_teste,
            categorias_treino,
            categorias_teste,
        )

    def guardar_artefactos(self, directoria: str) -> None:
        """Guarda os artefactos MLOps da vetorização no disco.

        Escreve três ficheiros na directoria indicada:
        - ``vocabulario.json``: dicionário token -> índice.
        - ``idf.npy``: vetor NumPy com os pesos IDF.
        - ``categoria_para_id.json``: dicionário categoria -> índice inteiro.
        - ``id_para_categoria.json``: dicionário índice inteiro -> categoria.

        Args:
            directoria: Caminho da pasta de destino. É criada se não existir.

        Raises:
            RuntimeError: Se o vetorizador ainda não tiver sido ajustado.
        """
        if not self.esta_ajustado:
            raise RuntimeError(
                "O vetorizador ainda nao foi ajustado. Execute fit() antes de guardar."
            )

        os.makedirs(directoria, exist_ok=True)

        caminho_vocabulario = os.path.join(directoria, "vocabulario.json")
        with open(caminho_vocabulario, "w", encoding="utf-8") as f:
            json.dump(self.vocabulario, f, ensure_ascii=False, indent=2)

        caminho_idf = os.path.join(directoria, "idf.npy")
        np.save(caminho_idf, self.idf)

        caminho_categorias = os.path.join(directoria, "categoria_para_id.json")
        with open(caminho_categorias, "w", encoding="utf-8") as f:
            json.dump(self.mapa_categoria_para_id, f, ensure_ascii=False, indent=2)

        caminho_ids = os.path.join(directoria, "id_para_categoria.json")
        with open(caminho_ids, "w", encoding="utf-8") as f:
            json.dump(self.mapa_id_para_categoria, f, ensure_ascii=False, indent=2)

    @classmethod
    def carregar_artefactos(cls, directoria: str) -> VetorizadorTfidfNumPy:
        """Carrega um vetorizador previamente guardado a partir dos artefactos.

        Reconstrói o estado completo (vocabulário, IDF, mapas de categorias) a
        partir dos ficheiros gravados por `guardar_artefactos`. Usado pelo
        motor de inferência (P7).

        Args:
            directoria: Caminho da pasta onde os artefactos foram guardados.

        Returns:
            Instância de `VetorizadorTfidfNumPy` pronta para `transform`.
        """
        instancia = cls()

        caminho_vocabulario = os.path.join(directoria, "vocabulario.json")
        with open(caminho_vocabulario, "r", encoding="utf-8") as f:
            instancia.vocabulario = json.load(f)
        caminho_idf = os.path.join(directoria, "idf.npy")
        instancia.idf = np.load(caminho_idf)

        caminho_categorias = os.path.join(directoria, "categoria_para_id.json")
        if os.path.exists(caminho_categorias):
            with open(caminho_categorias, "r", encoding="utf-8") as f:
                instancia.mapa_categoria_para_id = json.load(f)
            # Reconstrói o mapa inverso.
            instancia.mapa_id_para_categoria = {
                int(indice): categoria
                for categoria, indice in instancia.mapa_categoria_para_id.items()
            }
        instancia.esta_ajustado = True
        return instancia

    def guardar(self, caminho_pasta: str | Path) -> str:
        """Alias de compatibilidade para guardar_artefactos."""
        return self.guardar_artefactos(caminho_pasta)

    @classmethod
    def carregar(cls, caminho_pasta: str | Path) -> "VetorizadorTfidfNumPy":
        """Alias de compatibilidade para carregar_artefactos."""
        return cls.carregar_artefactos(caminho_pasta)

    def transformar(self, textos: list[str]) -> np.ndarray:
        """Alias de compatibilidade para transform."""
        return self.transform(textos)