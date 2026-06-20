"""
Módulo que executa o treino da rede neural com dados simulados ou reais.

O script realiza:
1. Carregamento das matrizes NumPy (simuladas ou da Gleicy)
2. Criação dos DataLoaders
3. Loop de treino com registro da perda
4. Comparação de duas configurações diferentes (RF09)
5. Exportação dos pesos (.pth) e da configuração (.json)
"""

import os
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from src.modelos.rede_neuronal import RedeNeuronalClassificacao


def criar_dados_simulados(num_amostras: int = 1000, num_features: int = 100):
    """
    Cria dados sintéticos para teste enquanto espera os dados da Gleicy.
    
    Returns:
        tuple: (caracteristicas, categorias) como tensores PyTorch.
    """
    torch.manual_seed(42)
    caracteristicas = torch.randn(num_amostras, num_features)
    categorias = torch.randint(0, 5, (num_amostras,))
    return caracteristicas, categorias


def treinar_configuracao(
    caracteristicas: torch.Tensor,
    categorias: torch.Tensor,
    configuracao: dict,
    epocas: int = 50,
    verbose: bool = True
) -> dict:
    """
    Treina uma configuração específica da rede neural.
    
    Args:
        caracteristicas (torch.Tensor): Dados de entrada com shape (num_amostras, num_features).
        categorias (torch.Tensor): Rótulos com shape (num_amostras,).
        configuracao (dict): Configuração do modelo (entrada, oculta, saida, dropout, lr, batch_size).
        epocas (int): Número de épocas de treino.
        verbose (bool): Se True, imprime progresso.
    
    Returns:
        dict: Histórico de perdas e modelo treinado.
    """
    # Extrai parâmetros da configuração
    entrada = configuracao['numero_entradas']
    oculta = configuracao['numero_ocultas']
    saida = configuracao['numero_saidas']
    dropout = configuracao.get('dropout', 0.2)
    taxa_aprendizado = configuracao.get('learning_rate', 0.001)
    batch_size = configuracao.get('batch_size', 32)
    
    # Instancia o modelo
    modelo = RedeNeuronalClassificacao(entrada, oculta, saida, dropout)
    
    # Configura otimizador e função de perda
    otimizador = optim.Adam(modelo.parameters(), lr=taxa_aprendizado)
    criterio = nn.CrossEntropyLoss()
    
    # Cria DataLoader
    dataset = TensorDataset(caracteristicas, categorias)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    # Histórico de perdas
    historico_perdas = []
    
    # Loop de treino
    for epoca in range(epocas):
        perda_total = 0.0
        for lote_caracteristicas, lote_categorias in dataloader:
            # Passagem direta (forward)
            saidas = modelo(lote_caracteristicas)
            perda = criterio(saidas, lote_categorias)
            
            # Retropropagação (backward)
            otimizador.zero_grad()
            perda.backward()
            otimizador.step()
            
            perda_total += perda.item()
        
        perda_media = perda_total / len(dataloader)
        historico_perdas.append(perda_media)
        
        if verbose and (epoca + 1) % 10 == 0:
            print(f"Config {configuracao['nome']} - Época {epoca+1}/{epocas} - Perda: {perda_media:.4f}")
    
    return {
        'modelo': modelo,
        'historico_perdas': historico_perdas,
        'configuracao': configuracao
    }


def salvar_artefatos(modelo: nn.Module, configuracao: dict, pasta_destino: str = "artefactos/execucao_001/modelo"):
    """
    Salva os pesos e a configuração do modelo.
    
    Args:
        modelo (nn.Module): Modelo treinado.
        configuracao (dict): Configuração do modelo.
        pasta_destino (str): Pasta onde salvar os artefatos.
    """
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Salva os pesos (state_dict) - NUNCA usar torch.save(model, ...)
    caminho_pesos = os.path.join(pasta_destino, "pesos.pth")
    torch.save(modelo.state_dict(), caminho_pesos)
    print(f" Pesos salvos em: {caminho_pesos}")
    
    # Salva a configuração
    caminho_config = os.path.join(pasta_destino, "configuracao_modelo.json")
    with open(caminho_config, 'w') as f:
        json.dump(configuracao, f, indent=4)
    print(f" Configuração salva em: {caminho_config}")


def comparar_configuracoes(caracteristicas: torch.Tensor, categorias: torch.Tensor):
    """
    Compara duas configurações diferentes (RF09).
    
    Critérios de comparação:
    - Config A: 1 camada oculta com 128 neurônios, lr=0.001, batch=32
    - Config B: 2 camadas ocultas (128, 64), lr=0.0005, batch=64
    
    Justificativa: Testar se aumentar a complexidade da rede melhora o aprendizado.
    """
    print("\n" + "="*60)
    print(" RF09 - Comparação de Configurações")
    print("="*60)
    
    # ------------------------------------------------------------
    # CONFIGURAÇÃO A: Arquitetura mais simples (1 camada oculta)
    # ------------------------------------------------------------
    # Justificativa dos hiperparâmetros:
    # - 128 neurônios: ponto de partida comum para problemas com ~5000 features,
    #   oferece capacidade moderada sem overfitting excessivo.
    # - dropout=0.2: regularização leve, adequada para redes de tamanho médio.
    # - learning_rate=0.001: valor padrão do Adam, geralmente eficaz sem ajuste fino.
    # - batch_size=32: padrão da literatura, equilibra estabilidade e velocidade.
    configuracao_a = {
        'nome': 'A - 1 camada oculta (128)',
        'numero_entradas': caracteristicas.shape[1],
        'numero_ocultas': 128,
        'numero_saidas': 5,
        'dropout': 0.2,
        'learning_rate': 0.001,
        'batch_size': 32
    }
    
    # ------------------------------------------------------------
    # CONFIGURAÇÃO B: Arquitetura mais profunda (2 camadas ocultas)
    # ------------------------------------------------------------
    # Justificativa dos hiperparâmetros:
    # - 128 e 64 neurônios: rede mais profunda para capturar padrões mais complexos,
    #   mas com redução gradual para evitar explosão de parâmetros.
    # - dropout=0.3: maior regularização para compensar a maior capacidade.
    # - learning_rate=0.0005: menor que a Config A, pois redes mais profundas
    #   exigem passos mais conservadores para convergir suavemente.
    # - batch_size=64: lotes maiores estabilizam a estimativa do gradiente
    #   em redes com mais parâmetros.
    configuracao_b = {
        'nome': 'B - 2 camadas ocultas (128, 64)',
        'numero_entradas': caracteristicas.shape[1],
        'numero_ocultas': 128,   # Primeira camada oculta
        'numero_saidas': 5,
        'dropout': 0.3,
        'learning_rate': 0.0005,
        'batch_size': 64
    }
    
    # Treina Configuração A
    print(f"\n Treinando {configuracao_a['nome']}...")
    resultado_treino_a = treinar_configuracao(caracteristicas, categorias, configuracao_a, epocas=30)
    
    # Treina Configuração B
    print(f"\n Treinando {configuracao_b['nome']}...")
    resultado_treino_b = treinar_configuracao(caracteristicas, categorias, configuracao_b, epocas=30)
    
    # Resumo comparativo
    print("\n" + "-"*60)
    print(" RESULTADOS COMPARATIVOS:")
    print("-"*60)
    print(f"Config A - Perda final: {resultado_treino_a['historico_perdas'][-1]:.4f}")
    print(f"Config B - Perda final: {resultado_treino_b['historico_perdas'][-1]:.4f}")
    
    if resultado_treino_a['historico_perdas'][-1] < resultado_treino_b['historico_perdas'][-1]:
        print("\n Config A apresentou melhor desempenho (menor perda final).")
    else:
        print("\n Config B apresentou melhor desempenho (menor perda final).")
    
    # Salva a melhor configuração
    if resultado_treino_a['historico_perdas'][-1] < resultado_treino_b['historico_perdas'][-1]:
        melhor_modelo = resultado_treino_a['modelo']
        melhor_configuracao = configuracao_a
    else:
        melhor_modelo = resultado_treino_b['modelo']
        melhor_configuracao = configuracao_b
    
    salvar_artefatos(melhor_modelo, melhor_configuracao)
    
    return resultado_treino_a, resultado_treino_b


def main():
    """
    Função principal que executa o treino.
    
    Fluxo:
    1. Carrega dados (simulados ou reais)
    2. Compara configurações
    3. Salva artefatos
    """
    print("Iniciando treino da rede neural...")
    print("-"*60)
    
    # Passo 1: Carregar ou simular dados
    # TODO: Quando a Gleicy entregar os dados, substituir por:
    # caracteristicas = torch.from_numpy(np.load('caracteristicas_treino.npy')).float()
    # categorias = torch.from_numpy(np.load('categorias_treino.npy')).long()
    
    print("Gerando dados simulados (20 amostras, 100 features)...")
    caracteristicas, categorias = criar_dados_simulados(num_amostras=20, num_features=100)
    print(f"   Shape features: {caracteristicas.shape}")
    print(f"   Shape labels: {categorias.shape}")
    print("-"*60)
    
    # Passo 2: Comparar configurações
    comparar_configuracoes(caracteristicas, categorias)
    
    print("\n" + "="*60)
    print("TREINO CONCLUÍDO COM SUCESSO!")
    print("="*60)


if __name__ == "__main__":
    main()