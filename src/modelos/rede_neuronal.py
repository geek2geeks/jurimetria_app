"""
Módulo que define a arquitetura da rede neural para classificação de decisões jurídicas.
...
"""


import torch
import torch.nn as nn

class RedeNeuronalClassificacao(nn.Module):
   
    def __init__(self, entrada: int, oculta: int, saida: int = 5, dropout: float = 0.2):
        super(RedeNeuronalClassificacao, self).__init__()
        
        # Fixa a semente para reprodutibilidade
        torch.manual_seed(42)
        
        # Arquitetura da rede
        self.camada1 = nn.Linear(entrada, oculta)
        self.camada2 = nn.Linear(oculta, saida)
        self.dropout = nn.Dropout(dropout)
        self.relu = nn.ReLU()
        
        # Inicialização dos pesos (He initialization para ReLU)
        nn.init.kaiming_uniform_(self.camada1.weight, nonlinearity='relu')
        nn.init.kaiming_uniform_(self.camada2.weight, nonlinearity='relu')
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Passagem direta dos dados pela rede.
        
        Args:
            x (torch.Tensor): Tensor de entrada com shape (batch_size, entrada).
            
        Returns:
            torch.Tensor: Logits (saída bruta) com shape (batch_size, saida).
                          A Softmax é aplicada pela CrossEntropyLoss durante o treino.
        """
        x = self.relu(self.camada1(x))
        x = self.dropout(x)
        x = self.camada2(x)  # Saída bruta (logits)
        return x