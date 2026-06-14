# JurisTriage PT

Projeto académico da disciplina **Engenharia de Software para IA e Frameworks Profundos**.

O objetivo é construir uma prova de conceito que classifica o sentido normativo de decisões judiciais portuguesas usando apenas `descritores` e `sumario`. A arquitetura central é:

```text
RawDocument -> Acordao -> DatasetRow -> NumPy -> PyTorch
            -> métricas -> manifest -> inferência
```

`decisao_raw`, texto dispositivo, ECLI, URL e qualquer conteúdo que revele a resposta não podem ser usados como entrada do modelo.

## Antes de começar

Lê por esta ordem:

1. [Constituição do projeto](constitution.md)
2. [Onboarding para iniciantes](docs/onboarding_for_beginners.md)
3. [Guia de instalação](docs/software_setup.md)
4. [Fluxo GitHub e Jira](docs/github_jira_workflow.md)
5. [Boas práticas](docs/development_best_practices.md)
6. [Onboarding individual](docs/onboarding_individual/README.md)
7. A tua spec em `docs/specs/`

## Instalação rápida

O guia completo, com Windows e macOS, está em [docs/software_setup.md](docs/software_setup.md).

Depois de instalar Anaconda, abre o Anaconda Prompt no Windows ou Terminal no macOS:

```bash
conda create -n juristriage python=3.11 -y
conda activate juristriage
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m unittest discover -s tests -p "test_*.py" -v
```

## Uso de IA

O professor aprovou a equipa de oito membros, mas não deu uma autorização específica para código gerado por IA. Se um aluno decidir usar IA e isso for compatível com as regras da disciplina, deve seguir o [fluxo de desenvolvimento assistido por IA](docs/ai_development_workflow.md).

Configuração recomendada:

- GitHub Spec Kit `v0.10.2`;
- OpenCode `>=1.14.24`;
- DeepSeek V4 Pro;
- revisão humana obrigatória.

Não coloques chaves, dados jurídicos reais ou dados pessoais em prompts.

## Trabalho diário

Cada tarefa deve ter um ticket Jira, uma branch e um Pull Request:

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/SCRUM-123-resumo-curto
```

Antes do commit:

```bash
git status
git diff
python -m unittest discover -s tests -p "test_*.py" -v
```

O PR deve indicar o ticket Jira, testes executados e se houve apoio de IA. Pedro revê os PRs dos colegas. Os PRs do Pedro precisam de outro revisor humano.

## Dados

O corpus completo não pertence ao GitHub. Apenas amostras pequenas, sintéticas ou sanitizadas podem ser versionadas.

O endereço do dataset de trabalho encontra-se em `.env.example`. Cria o teu `.env` local e não o commits.

## Documentação

- [Arquitetura](docs/architecture.md)
- [Requisitos](docs/requirements.md)
- [Decisões arquiteturais](docs/decisions.md)
- [Ética e privacidade](docs/ethics.md)
- [Estrutura dos PDFs](docs/pdf_structure_report.md)
- [Fluxo assistido por IA](docs/ai_development_workflow.md)
- [Instalação de software](docs/software_setup.md)
- [GitHub e Jira](docs/github_jira_workflow.md)
- [Boas práticas](docs/development_best_practices.md)
- [Relatório desta atualização](docs/ai_documentation_update_report.md)

## Estado atual

O repositório contém a arquitetura, requisitos, specs e onboarding. A implementação funcional será desenvolvida pelas oito tarefas da equipa. Não confundas documentação pronta com pipeline já implementada.
