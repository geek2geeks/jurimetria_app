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

## Estado atual

O repositório contém a arquitetura, requisitos, especificações e guias de integração. A implementação funcional será desenvolvida pelas oito tarefas da equipa. Não confundas documentação pronta com fluxo funcional já implementado.
