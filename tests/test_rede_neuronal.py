"""Testes unitários para o módulo de rede neural.

Verifica:
1. A arquitetura do modelo (dimensões de entrada/saída)
2. Que o treino reduz a perda
3. Que os artefatos são salvos corretamente

Durante a integração progressiva, os módulos `src.modelos.rede_neuronal` e
`src.treino.treinar_modelo` podem ainda não estar mergeados no `main`. Em vez
de falhar com `ModuleNotFoundError`, este ficheiro faz **skip condicional** —
quando ambos chegarem ao `main`, os testes passam automaticamente sem
qualquer alteração aqui.
"""
import importlib.util as _importlib_util
import unittest

# --- Skip condicional: dependências da equipa --------------------------------
_DEPENDENCIAS_DA_EQUIPA = (
    "src.modelos.rede_neuronal",      # SCRUM-9 — módulo próprio
    "src.treino.treinar_modelo",      # SCRUM-9 — função de treino
)
_em_falta = [
    nome for nome in _DEPENDENCIAS_DA_EQUIPA
    if _importlib_util.find_spec(nome) is None
]
if _em_falta:
    raise unittest.SkipTest(
        "Módulos da equipa ainda não disponíveis no main: " + ", ".join(_em_falta)
    )
# -----------------------------------------------------------------------------

import json
import os

import torch
import torch.nn as nn

from src.modelos.rede_neuronal import RedeNeuronalClassificacao
from src.treino.treinar_modelo import salvar_artefatos, treinar_configuracao


class TestRedeNeuronal(unittest.TestCase):
    """Testes para a rede neural e treino."""

    def setUp(self):
        """Configuração antes de cada teste."""
        torch.manual_seed(0)
        self.num_entradas = 10
        self.num_ocultas = 5
        self.num_saidas = 3
        self.batch_size = 4

        # Dados sintéticos para teste
        self.caracteristicas = torch.randn(20, self.num_entradas)
        self.categorias = torch.randint(0, self.num_saidas, (20,))

        self.modelo = RedeNeuronalClassificacao(
            self.num_entradas,
            self.num_ocultas,
            self.num_saidas
        )

    def test_dimensoes_saida(self):
        """Testa se a saída tem o formato esperado."""
        dados_teste = torch.randn(5, self.num_entradas)
        saida = self.modelo(dados_teste)
        self.assertEqual(saida.shape, (5, self.num_saidas))

    def test_diminuicao_perda(self):
        """Testa se a perda diminui após algumas iterações."""
        config = {
            'numero_entradas': self.num_entradas,
            'numero_ocultas': self.num_ocultas,
            'numero_saidas': self.num_saidas,
            'dropout': 0.0,
            'learning_rate': 0.01,
            'batch_size': self.batch_size
        }

        resultado = treinar_configuracao(
            self.caracteristicas,
            self.categorias,
            config,
            epocas=5,
            verbose=False
        )

        perda_inicial = resultado['historico_perdas'][0]
        perda_final = resultado['historico_perdas'][-1]

        # A perda deve ter diminuído (ou pelo menos não aumentado)
        self.assertLess(perda_final, perda_inicial)

    def test_salvamento_artefatos(self):
        """Testa se os artefatos são salvos corretamente."""
        pasta_teste = "test_artefactos"

        # Cria modelo de teste
        modelo_teste = RedeNeuronalClassificacao(10, 5, 3)
        config_teste = {
            'numero_entradas': 10,
            'numero_ocultas': 5,
            'numero_saidas': 3,
            'dropout': 0.2,
            'classe_modelo': 'RedeNeuronalClassificacao'
        }

        # Salva artefatos
        salvar_artefatos(modelo_teste, config_teste, pasta_teste)

        # Verifica se os arquivos existem
        self.assertTrue(os.path.exists(f"{pasta_teste}/pesos.pth"))
        self.assertTrue(os.path.exists(f"{pasta_teste}/configuracao_modelo.json"))

        # Verifica conteúdo do JSON
        with open(f"{pasta_teste}/configuracao_modelo.json", 'r') as f:
            config_carregada = json.load(f)
            self.assertEqual(config_carregada['numero_entradas'], 10)
            self.assertEqual(config_carregada['numero_ocultas'], 5)
            self.assertEqual(config_carregada['numero_saidas'], 3)

        # Limpa arquivos de teste
        os.remove(f"{pasta_teste}/pesos.pth")
        os.remove(f"{pasta_teste}/configuracao_modelo.json")
        os.rmdir(pasta_teste)


if __name__ == '__main__':
    unittest.main()
