"""Módulo de gráficos de avaliação (P6 - Alessandro Bezerra / SCRUM-31).

Gera visualizações das curvas de perda e exatidão de treino vs teste.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Sequence


def gerar_grafico_curvas_perda(
    historico_loss_treino: Sequence[float],
    historico_loss_teste: Sequence[float],
    caminho_destino: str | Path = "artefactos/curva_perda.png",
    titulo: str = "Curva de Perda — Treino vs Teste",
) -> str | None:
    """Gera e guarda um gráfico PNG com a evolução da perda ao longo das épocas.

    Tenta utilizar matplotlib. Se não estiver instalado, imprime mensagem
    informativa sem interromper o pipeline.

    Args:
        historico_loss_treino: Lista de perdas por época no treino.
        historico_loss_teste: Lista de perdas por época no teste.
        caminho_destino: Caminho onde guardar o ficheiro PNG.
        titulo: Título do gráfico.

    Returns:
        Caminho do ficheiro guardado se bem-sucedido, None caso contrário.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")  # Backend não-interativo para CI/CD
        import matplotlib.pyplot as plt
    except ImportError:
        print("[INFO] matplotlib não está instalado. Gráfico de perda não gerado.")
        return None

    caminho = Path(caminho_destino)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    epocas = range(1, len(historico_loss_treino) + 1)

    plt.figure(figsize=(8, 5))
    plt.plot(epocas, historico_loss_treino, label="Perda (Treino)", color="#1f77b4", linewidth=2)
    plt.plot(epocas, historico_loss_teste, label="Perda (Teste)", color="#ff7f0e", linewidth=2, linestyle="--")

    plt.title(titulo, fontsize=14, fontweight="bold")
    plt.xlabel("Época", fontsize=12)
    plt.ylabel("CrossEntropy Loss", fontsize=12)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()

    plt.savefig(caminho, dpi=300)
    plt.close()
    print(f"✓ Gráfico de perda guardado em: {caminho}")
    return str(caminho)
