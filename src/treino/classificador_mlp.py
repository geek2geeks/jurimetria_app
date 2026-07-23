"""Módulo de treino — classe wrapper ClassificadorMLP."""

from __future__ import annotations

import torch
import torch.nn as nn
from pathlib import Path
from typing import Any, Optional

from src.modelos.rede_neuronal import RedeNeuronalClassificacao


class ClassificadorMLP(nn.Module):
    """Wrapper para a RedeNeuronalClassificacao com utilitários de treino."""

    def __init__(self, rede: RedeNeuronalClassificacao):
        """Inicializa o wrapper com a rede neuronal base."""
        super().__init__()
        self.rede = rede

    @classmethod
    def de_configuracao(cls, configuracao: dict[str, int]) -> ClassificadorMLP:
        """Instancia o classificador a partir de um dicionário de configuração."""
        rede = RedeNeuronalClassificacao(
            entrada=configuracao["dim_entrada"],
            oculta=configuracao.get("dim_oculta", 16),
            saida=configuracao["num_classes"],
        )
        return cls(rede)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Passagem direta."""
        return self.rede(x)

    def treinar(
        self,
        x_treino: torch.Tensor,
        y_treino: torch.Tensor,
        epocas: int,
        **kwargs: Any,
    ) -> None:
        """Laço de treino para a rede neuronal."""
        # TODO: Implementar laço de treino
        pass

    def prever(self, x: torch.Tensor) -> torch.Tensor:
        """Faz previsão sobre os dados de entrada."""
        self.eval()
        with torch.no_grad():
            logits = self(x)
            probabilidades = torch.softmax(logits, dim=1)
            return probabilidades

    def salvar(self, caminho: str | Path) -> None:
        """Guarda o state_dict do modelo."""
        torch.save(self.state_dict(), caminho)

    @classmethod
    def carregar(
        cls,
        caminho: str | Path,
        configuracao: Optional[dict[str, int]] = None
    ) -> ClassificadorMLP:
        """Carrega o modelo a partir do disco.
        
        Se a configuração não for fornecida, assume que o ficheiro guardado
        é um dicionário contendo 'estado' e 'configuracao'.
        """
        caminho_path = Path(caminho)
        dados = torch.load(caminho_path)
        
        if configuracao is None:
            # Caso os dados incluam a configuração
            configuracao = dados.get("configuracao", {})
            estado = dados.get("estado", dados)
        else:
            estado = dados
            
        modelo = cls.de_configuracao(configuracao)
        modelo.load_state_dict(estado)
        return modelo
