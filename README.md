# JurisTriage PT

Projeto académico da disciplina **Engenharia de Software para IA e Frameworks Profundos**.

O objetivo é construir uma prova de conceito que classifica o sentido normativo de decisões judiciais portuguesas usando apenas `descritores` e `sumario`. A arquitetura central é:

```text
DocumentoBruto -> Acordao -> RegistoClassificacao -> NumPy -> PyTorch
               -> métricas -> manifesto -> inferência
```

`decisao_bruta`, texto dispositivo, ECLI, URL e qualquer conteúdo que revele a resposta não podem ser usados como entrada do modelo.

## Antes de começar

Lê por esta ordem:

1. [Constituição do projeto](constitution.md) (Regras principais, equipa e boas práticas)
2. [Instalação de software](docs/instalacao_software.md)
3. [Fluxo GitHub e Jira](docs/fluxo_github_jira.md)
4. [Convenções de nomes](docs/convencoes_nomes.md)
5. O teu guia individual na pasta `docs/guias_individuais/`

## Instalação rápida

O guia completo, com Windows e macOS, está em [docs/instalacao_software.md](docs/instalacao_software.md).

Depois de instalar Anaconda, abre o Anaconda Prompt no Windows ou Terminal no macOS:

```bash
conda create -n juristriage python=3.11 -y
conda activate juristriage
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m unittest discover -s tests -p "test_*.py" -v
```

## Trabalho diário

Cada tarefa deve ter um ticket Jira, um ramo e um pedido de integração. Para detalhes sobre os tickets da equipa, regras de desenvolvimento assistido por IA e fluxo diário, consulta a [Constituição do projeto](constitution.md) e o [Fluxo GitHub e Jira](docs/fluxo_github_jira.md).

## Dados

O corpus completo não pertence ao GitHub. Apenas amostras pequenas, sintéticas ou sanitizadas podem ser versionadas.

O endereço do conjunto de dados de trabalho encontra-se em `.env.example`. Cria o teu `.env` local e não o incluas num commit.

## Documentação Central

- [Constituição do projeto](constitution.md)
- [Arquitetura](docs/arquitetura.md)
- [Requisitos](docs/requisitos.md)
- [Decisões arquiteturais](docs/decisoes.md)
- [Ética e privacidade](docs/etica.md)
- [Fluxo assistido por IA](docs/fluxo_desenvolvimento_ia.md)
- [Instalação de software](docs/instalacao_software.md)
- [Fluxo GitHub e Jira](docs/fluxo_github_jira.md)
- [Convenções de nomes](docs/convencoes_nomes.md)

## Entrega 3 — Pipeline de Treino PyTorch

A Entrega 3 (PyTorch Parte 2) implementa a pipeline end-to-end de treino e avaliação do modelo neural:

```bash
# Executar a pipeline principal de treino e validação:
python main.py

# Executar a suite de testes unitários:
python -m unittest discover -s tests -v
```

O comando `python main.py` realiza:
1. Vetorização TF-IDF dos dados de treino e teste
2. Conversão dos dados NumPy para tensores PyTorch
3. Treino da rede neural MLP (`RedeNeuronalClassificacao`) com cálculo de perda (`CrossEntropyLoss`) e otimizador Adam
4. Impressão de métricas de treino e teste (perda e exatidão) a cada época
5. Exportação dos pesos (`pesos.pth`) e metadados na pasta `artefactos/`

## Estado atual

O repositório inclui a pipeline completa da Entrega 3 (PyTorch Parte 2), com módulos integrados e cobertura de testes automatizados.
