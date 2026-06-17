"""Modelo de referência, métricas e avaliação do JurisTriage PT.

Compara o modelo PyTorch (P5) com um modelo de referência de classe maioritária.
Exporta os resultados para metricas.json na pasta de artefactos da execução.

Nota sobre desequilíbrio: MANTIDA domina ~52% do corpus.
Um modelo que preveja sempre MANTIDA teria ~52% de exatidão mas Macro-F1
muito baixo — daí a obrigatoriedade de reportar Macro-F1 (RNF08, ADR-02).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, f1_score


class ModeloReferenciaClasseMaioritaria:
    """Estratégia cega que prevê sempre a classe mais frequente no treino.

    Serve de baseline: se o modelo PyTorch não superar este valor,
    a rede neuronal não aprendeu nada útil.
    """

    def __init__(self) -> None:
        self.classe_maioritaria: int | None = None

    def fit(self, categorias_treino: np.ndarray) -> None:
        """Aprende qual a classe mais frequente no conjunto de treino.

        Args:
            categorias_treino: array 1-D de inteiros com os rótulos de treino,
                               ex: [0, 0, 1, 0, 2, 0, 1, ...]
        """
        self.classe_maioritaria = int(np.argmax(np.bincount(categorias_treino)))

    def prever(self, categorias_reais: np.ndarray) -> np.ndarray:
        """Prevê sempre a classe maioritária para todos os exemplos.

        Args:
            categorias_reais: array 1-D usado só para saber quantas
                              previsões devolver (o conteúdo é ignorado).

        Returns:
            Array 1-D preenchido com self.classe_maioritaria.
        """
        if self.classe_maioritaria is None:
            raise RuntimeError("Chama fit() antes de prever().")
        return np.full(len(categorias_reais), self.classe_maioritaria)


def avaliar_execucao(
    categorias_reais: np.ndarray,
    categorias_previstas: np.ndarray,
    categorias_previstas_referencia: np.ndarray,
) -> dict:
    """Calcula e devolve as métricas de avaliação da execução.

    Usa Macro-F1 porque o corpus é desequilibrado (MANTIDA ~52%):
    a exatidão sozinha seria enganosa — um modelo que preveja sempre
    MANTIDA teria ~52% de exatidão mas Macro-F1 muito baixo.

    Args:
        categorias_reais: array 1-D com as classes verdadeiras do teste.
        categorias_previstas: array 1-D com as previsões da rede PyTorch.
        categorias_previstas_referencia: previsões do modelo de referência.

    Returns:
        Dicionário com exatidao, macro_f1 e macro_f1_referencia.
    """
    exatidao = float(accuracy_score(categorias_reais, categorias_previstas))

    # average="macro" dá igual peso a cada classe, independentemente
    # de quantos exemplos tem — essencial para dados desequilibrados
    macro_f1 = float(f1_score(
        categorias_reais, categorias_previstas,
        average="macro", zero_division=0
    ))

    macro_f1_referencia = float(f1_score(
        categorias_reais, categorias_previstas_referencia,
        average="macro", zero_division=0
    ))

    return {
        "exatidao": round(exatidao, 4),
        "macro_f1": round(macro_f1, 4),
        "macro_f1_referencia": round(macro_f1_referencia, 4),
    }


def exportar_metricas(
    metricas: dict,
    pasta_execucao: str | Path,
) -> Path:
    """Guarda as métricas em metricas.json na pasta da execução.

    Não usa print() como relatório permanente — o ficheiro JSON é
    o registo oficial e reprodutível desta execução.

    Args:
        metricas: dicionário devolvido por avaliar_execucao().
        pasta_execucao: caminho para artefactos/execucao_XXX/

    Returns:
        Caminho do ficheiro gravado.
    """
    pasta = Path(pasta_execucao)
    pasta.mkdir(parents=True, exist_ok=True)

    caminho = pasta / "metricas.json"
    with open(caminho, "w", encoding="utf-8") as ficheiro:
        json.dump(metricas, ficheiro, indent=2, ensure_ascii=False)

    print(f"Métricas exportadas para: {caminho}")
    return caminho