#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pipeline principal do JurisTriage PT — Entrega 3 (PyTorch Parte 2).

Demonstra o fluxo end-to-end:
    1. Carregar dados (simulados ou JSON reais)
    2. Pré-processar textos (limpeza + normalização)
    3. Vetorizar com TF-IDF (NumPy puro)
    4. Converter para tensores PyTorch
    5. Treinar modelo MLP (RedeNeuronalClassificacao)
    6. Avaliar no conjunto de teste
    7. Imprimir métricas de treino e teste por época
    8. Salvar modelo treinado e artefactos

Execução:
    python main.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from src.dados.esquemas import RegistoClassificacao
from src.caracteristicas.vetorizador_tfidf import (
    VetorizadorTfidfNumPy,
    CLASSES_CANONICAS,
)
from src.pre_processamento.limpeza_texto import limpar_texto, normalizar_categoria
from src.modelos.rede_neuronal import RedeNeuronalClassificacao


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
SEMENTE: int = 42
PROPORCAO_TESTE: float = 0.2
PASTA_ARTEFACTOS: str = "artefactos/execucao_entrega3"


# ---------------------------------------------------------------------------
# 1. Carregar / gerar dados
# ---------------------------------------------------------------------------
def gerar_registos_simulados(n: int = 200) -> list[RegistoClassificacao]:
    """Gera registos simulados para demonstrar o pipeline.

    Em produção, estes seriam carregados via carregador_acordaos_json +
    analisador de metadados + limpeza de texto.
    """
    np.random.seed(SEMENTE)
    categorias = CLASSES_CANONICAS
    frases_base = {
        "ANULADA": [
            "o tribunal decidiu anular a sentenca recorrida",
            "a decisao foi declarada nula por vicio processual",
            "anulacao da sentenca por falta de fundamentacao",
        ],
        "MANTIDA": [
            "o recurso foi julgado improcedente mantendo a decisao",
            "confirma-se a sentenca recorrida em todos os seus termos",
            "o tribunal manteve a decisao de primeira instancia",
        ],
        "NAO_CONHECIDA": [
            "o recurso nao foi admitido por falta de legitimidade",
            "nao se conhece do recurso por intempestividade",
            "o tribunal decidiu nao tomar conhecimento do recurso",
        ],
        "OUTRA": [
            "decisao parcialmente procedente com custas repartidas",
            "o tribunal remeteu o processo para outra jurisdicao",
            "decisao de natureza interlocutoria sem caracter definitivo",
        ],
        "REVOGADA": [
            "a sentenca recorrida foi revogada e substituida",
            "revogacao total da decisao de primeira instancia",
            "o tribunal superior revogou a decisao anterior",
        ],
    }

    registos: list[RegistoClassificacao] = []
    for i in range(n):
        cat = categorias[i % len(categorias)]
        frases = frases_base[cat]
        texto = frases[i % len(frases)]
        # Adicionar variação aleatória
        palavras_extra = ["direito", "lei", "justica", "processo", "acordao",
                          "relator", "juiz", "tribunal", "recurso", "sentenca"]
        extras = np.random.choice(palavras_extra, size=3, replace=False)
        texto_completo = f"{texto} {' '.join(extras)}"

        registos.append(RegistoClassificacao(
            id_documento=f"DOC-{i:04d}",
            texto=limpar_texto(texto_completo),
            categoria_normalizada=cat,
            tribunal="STJ" if i % 2 == 0 else "TRL",
            ano=2024,
        ))

    return registos


# ---------------------------------------------------------------------------
# 2. Pipeline de treino
# ---------------------------------------------------------------------------
def treinar_pipeline(
    registos: list[RegistoClassificacao],
    epocas: int = 50,
    taxa_aprendizado: float = 0.001,
    tamanho_lote: int = 32,
    dropout: float = 0.2,
    numero_ocultas: int = 128,
) -> dict:
    """Executa o pipeline completo de treino.

    Returns:
        Dicionário com modelo, vetorizador, históricos e métricas.
    """
    print("=" * 65)
    print("  JurisTriage PT — Pipeline de Treino (Entrega 3)")
    print("=" * 65)

    # --- Passo 1: Vetorização TF-IDF ---
    print("\n[1/6] Vetorização TF-IDF com NumPy...")
    vetorizador = VetorizadorTfidfNumPy()
    x_treino_np, x_teste_np, y_treino_np, y_teste_np = vetorizador.processar_registos(
        registos, proporcao_teste=PROPORCAO_TESTE, semente=SEMENTE,
    )
    n_treino = x_treino_np.shape[0]
    n_teste = x_teste_np.shape[0]
    n_features = x_treino_np.shape[1]
    n_classes = len(vetorizador.mapa_categoria_para_id)
    print(f"      Treino: {n_treino} amostras | Teste: {n_teste} amostras")
    print(f"      Features (tokens): {n_features} | Classes: {n_classes}")
    print(f"      Classes: {list(vetorizador.mapa_categoria_para_id.keys())}")

    # --- Passo 2: Conversão para tensores PyTorch ---
    print("\n[2/6] Conversão para tensores PyTorch...")
    x_treino = torch.tensor(x_treino_np, dtype=torch.float32)
    y_treino = torch.tensor(y_treino_np, dtype=torch.long)
    x_teste = torch.tensor(x_teste_np, dtype=torch.float32)
    y_teste = torch.tensor(y_teste_np, dtype=torch.long)
    print(f"      x_treino shape: {x_treino.shape}")
    print(f"      y_treino shape: {y_treino.shape}")
    print(f"      x_teste  shape: {x_teste.shape}")
    print(f"      y_teste  shape: {y_teste.shape}")

    # Criar DataLoaders
    dataset_treino = TensorDataset(x_treino, y_treino)
    dataset_teste = TensorDataset(x_teste, y_teste)
    loader_treino = DataLoader(dataset_treino, batch_size=tamanho_lote, shuffle=True)
    loader_teste = DataLoader(dataset_teste, batch_size=tamanho_lote, shuffle=False)

    # --- Passo 3: Instanciar modelo ---
    print("\n[3/6] Instanciação do modelo MLP...")
    torch.manual_seed(SEMENTE)
    modelo = RedeNeuronalClassificacao(
        entrada=n_features,
        oculta=numero_ocultas,
        saida=n_classes,
        dropout=dropout,
    )
    criterio = nn.CrossEntropyLoss()
    optimizador = optim.Adam(modelo.parameters(), lr=taxa_aprendizado)
    total_params = sum(p.numel() for p in modelo.parameters())
    print(f"      Arquitetura: {n_features} -> {numero_ocultas} -> {n_classes}")
    print(f"      Parâmetros totais: {total_params:,}")
    print(f"      Dropout: {dropout} | LR: {taxa_aprendizado} | Batch: {tamanho_lote}")

    # --- Passo 4: Laço de treino ---
    print(f"\n[4/6] Treino ({epocas} épocas)...")
    print(f"      {'Época':>6}  {'Loss Treino':>12}  {'Acc Treino':>10}  {'Loss Teste':>11}  {'Acc Teste':>10}")
    print("      " + "-" * 56)

    historico_loss_treino: list[float] = []
    historico_loss_teste: list[float] = []
    historico_acc_treino: list[float] = []
    historico_acc_teste: list[float] = []

    for epoca in range(epocas):
        # --- Treino ---
        modelo.train()
        perda_total_treino = 0.0
        acertos_treino = 0
        total_treino = 0

        for lote_x, lote_y in loader_treino:
            saidas = modelo(lote_x)
            perda = criterio(saidas, lote_y)

            optimizador.zero_grad()
            perda.backward()
            optimizador.step()

            perda_total_treino += perda.item() * lote_x.size(0)
            previsoes = torch.argmax(saidas, dim=1)
            acertos_treino += (previsoes == lote_y).sum().item()
            total_treino += lote_x.size(0)

        loss_treino = perda_total_treino / total_treino
        acc_treino = acertos_treino / total_treino

        # --- Avaliação no teste ---
        modelo.eval()
        perda_total_teste = 0.0
        acertos_teste = 0
        total_teste = 0

        with torch.no_grad():
            for lote_x, lote_y in loader_teste:
                saidas = modelo(lote_x)
                perda = criterio(saidas, lote_y)

                perda_total_teste += perda.item() * lote_x.size(0)
                previsoes = torch.argmax(saidas, dim=1)
                acertos_teste += (previsoes == lote_y).sum().item()
                total_teste += lote_x.size(0)

        loss_teste = perda_total_teste / total_teste
        acc_teste = acertos_teste / total_teste

        historico_loss_treino.append(loss_treino)
        historico_loss_teste.append(loss_teste)
        historico_acc_treino.append(acc_treino)
        historico_acc_teste.append(acc_teste)

        # Imprimir a cada 5 épocas e na última
        if (epoca + 1) % 5 == 0 or epoca == 0 or epoca == epocas - 1:
            print(f"      {epoca+1:>5}/{epocas}  {loss_treino:>12.4f}  {acc_treino:>9.1%}  {loss_teste:>11.4f}  {acc_teste:>9.1%}")

    # --- Passo 5: Salvar modelo e artefactos ---
    print(f"\n[5/6] Salvamento de artefactos em {PASTA_ARTEFACTOS}/...")
    from src.treino.persistencia_execucao import guardar_execucao

    config_modelo = {
        "numero_entradas": n_features,
        "numero_ocultas": numero_ocultas,
        "numero_saidas": n_classes,
        "dropout": dropout,
        "taxa_aprendizado": taxa_aprendizado,
        "epocas": epocas,
        "tamanho_lote": tamanho_lote,
    }

    pasta = guardar_execucao(
        id_execucao=os.path.basename(PASTA_ARTEFACTOS),
        rede=modelo,
        vetorizador=vetorizador,
        dimensoes={
            "numero_entradas": n_features,
            "numero_ocultas": numero_ocultas,
            "numero_saidas": n_classes,
        },
        metricas={
            "exatidao": historico_acc_teste[-1],
            "perda_treino": historico_loss_treino[-1],
            "perda_teste": historico_loss_teste[-1],
            "nota": "dados simulados — não representa desempenho em corpus real",
        },
        hiperparametros={
            "dropout": dropout,
            "taxa_aprendizado": taxa_aprendizado,
            "epocas": epocas,
            "tamanho_lote": tamanho_lote,
        },
        semente=SEMENTE,
        pasta_artefactos=os.path.dirname(PASTA_ARTEFACTOS),
    )
    print(f"      [OK] Execução completa + manifesto: {pasta}")

  # --- Passo 6: Verificar carregamento ---
    print("\n[6/6] Verificação: carregar modelo salvo e fazer inferência...")
    from src.treino.classificador_mlp import ClassificadorMLP

    caminho_pesos = os.path.join(PASTA_ARTEFACTOS, "modelo", "pesos.pth")
    modelo_carregado = ClassificadorMLP.de_configuracao({
        "dim_entrada": n_features,
        "dim_oculta": numero_ocultas,
        "num_classes": n_classes,
    })
    modelo_carregado.load_state_dict(torch.load(caminho_pesos, weights_only=True))
    modelo_carregado.eval()

    with torch.no_grad():
        saidas_teste = modelo_carregado(x_teste)
        previsoes_teste = torch.argmax(saidas_teste, dim=1)
        acc_verificacao = (previsoes_teste == y_teste).float().mean().item()

    print(f"      [OK] Modelo carregado com sucesso!")
    print(f"      [OK] Accuracy no teste (verificação): {acc_verificacao:.1%}")

    # --- Resumo final ---
    print("\n" + "=" * 65)
    print("  RESULTADOS FINAIS")
    print("=" * 65)
    print(f"  Loss treino final:    {historico_loss_treino[-1]:.4f}")
    print(f"  Loss teste final:     {historico_loss_teste[-1]:.4f}")
    print(f"  Accuracy treino:      {historico_acc_treino[-1]:.1%}")
    print(f"  Accuracy teste:       {historico_acc_teste[-1]:.1%}")
    print(f"  Artefactos salvos em: {PASTA_ARTEFACTOS}/")
    print("=" * 65)

    return {
        "modelo": modelo,
        "vetorizador": vetorizador,
        "historico_loss_treino": historico_loss_treino,
        "historico_loss_teste": historico_loss_teste,
        "historico_acc_treino": historico_acc_treino,
        "historico_acc_teste": historico_acc_teste,
        "config": config_modelo,
    }


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------
def main() -> None:
    """Ponto de entrada principal."""
    print("Gerando dados simulados (200 acórdãos, 5 classes)...\n")
    registos = gerar_registos_simulados(n=200)
    print(f"Total de registos: {len(registos)}")
    print(f"Distribuição: {dict(sorted({cat: sum(1 for r in registos if r.categoria_normalizada == cat) for cat in CLASSES_CANONICAS}.items()))}\n")

    treinar_pipeline(registos, epocas=50)


if __name__ == "__main__":
    main()
