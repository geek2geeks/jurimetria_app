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

1. [Constituição do projeto](constitution.md)
2. [Guia para iniciantes](docs/guia_iniciantes.md)
3. [Guia de instalação](docs/instalacao_software.md)
4. [Fluxo GitHub e Jira](docs/fluxo_github_jira.md)
5. [Boas práticas](docs/boas_praticas_desenvolvimento.md)
6. [Guias individuais](docs/guias_individuais/README.md)
7. [Convenções de nomes](docs/convencoes_nomes.md)
8. A tua especificação em `docs/especificacoes/`

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

## Uso de IA

O professor aprovou a equipa de oito membros, mas não deu uma autorização específica para código gerado por IA. Se um aluno decidir usar IA e isso for compatível com as regras da disciplina, deve seguir o [fluxo de desenvolvimento assistido por IA](docs/fluxo_desenvolvimento_ia.md).

Configuração recomendada:

- GitHub Spec Kit `v0.10.2`;
- OpenCode `>=1.14.24`;
- DeepSeek V4 Pro;
- revisão humana obrigatória.

Não coloques chaves, dados jurídicos reais ou dados pessoais em prompts.

## Trabalho diário

Cada tarefa deve ter um ticket Jira, um ramo e um pedido de integração:

```bash
git switch main
git pull --ff-only origin main
git switch -c funcionalidade/SCRUM-123-resumo-curto
```

Antes do commit:

```bash
git status
git diff
python -m unittest discover -s tests -p "test_*.py" -v
```

O PR deve indicar o ticket Jira, testes executados e se houve apoio de IA. Pedro revê os PRs dos colegas e pode validar os próprios PRs como administrador, documentando os testes e a decisão.

## Tarefas Jira da equipa

| Pessoa | Ticket |
|---|---|
| Alessandro | `SCRUM-5` |
| Daniela | `SCRUM-6` |
| Gustavo | `SCRUM-7` |
| Gleicy | `SCRUM-8` |
| Helton | `SCRUM-9` |
| Luciana | `SCRUM-10` |
| Sandro | `SCRUM-11` |
| Pedro | `SCRUM-12` |

As tarefas estão no projeto Jira `SCRUM` e encontram-se atribuídas aos oito responsáveis.

## Dados

O corpus completo não pertence ao GitHub. Apenas amostras pequenas, sintéticas ou sanitizadas podem ser versionadas.

O endereço do conjunto de dados de trabalho encontra-se em `.env.example`. Cria o teu `.env` local e não o incluas num commit.

## Documentação

- [Arquitetura](docs/arquitetura.md)
- [Requisitos](docs/requisitos.md)
- [Decisões arquiteturais](docs/decisoes.md)
- [Ética e privacidade](docs/etica.md)
- [Estrutura dos PDFs](docs/relatorio_estrutura_pdfs.md)
- [Fluxo assistido por IA](docs/fluxo_desenvolvimento_ia.md)
- [Instalação de software](docs/instalacao_software.md)
- [GitHub e Jira](docs/fluxo_github_jira.md)
- [Boas práticas](docs/boas_praticas_desenvolvimento.md)
- [Convenções de nomes](docs/convencoes_nomes.md)
- [Relatório desta atualização](docs/relatorio_atualizacao_documentacao_ia.md)

## Estado atual

O repositório contém a arquitetura, requisitos, especificações e guias de integração. A implementação funcional será desenvolvida pelas oito tarefas da equipa. Não confundas documentação pronta com fluxo funcional já implementado.
