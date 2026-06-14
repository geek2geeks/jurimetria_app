# Projeto de Jurimetria - Constituição (Spec-Driven Development)

Este documento define os princípios, diretrizes técnicas e as regras inquebráveis do projeto. Qualquer membro da equipe (Alessandro, Daniela, Gleicy, Gustavo, Helton, Luciana, Sandro) ou agente de IA que atuar neste repositório **deve** seguir este documento.

## 1. Princípios de Engenharia e Metodologia (SDD - Spec Kit)
1. **Zero Vibe-Coding:** É estritamente proibido gerar código sem estrutura prévia. O desenvolvimento deve seguir o Pipeline do Spec Kit do GitHub.
2. **Especificação é Lei:** Nenhum código pode ser iniciado sem que a Especificação (Specify) e o Plano Técnico (Plan) estejam documentados, clarificados (Clarify) e validados pelo Lead (Pedro).
3. **Validação Contínua:** Antes de cada commit, o desenvolvedor deve realizar validação cruzada para garantir que o código cumpre o Checklist.

## 2. Regras Arquiteturais e Padrões de Código
A arquitetura visa o cumprimento dos requisitos acadêmicos da disciplina:
- **Linguagem:** Python 3.10+
- **Tipagem Forte:** O uso de Type Hints (`typing`) é **obrigatório** em todas as funções e assinaturas de métodos.
- **Stack Tecnológica:**
  - `NumPy`: Manipulação vetorial e de matrizes no pré-processamento.
  - `PyTorch` (`torch.nn`, `TensorDataset`, `DataLoader`): Modelagem preditiva.
  - `unittest` nativo do Python para testes automatizados.
- **Estrutura de Diretórios Inviolável:**
  - `data/` (Arquivos brutos e amostras JSON/PDF. Ignorados no git).
  - `docs/` (Specs do SDD e manuais).
  - `src/data/` (Scripts de Ingestão).
  - `src/preprocessing/` (Conversão NumPy e limpeza).
  - `src/models/` (Arquitetura do modelo PyTorch).
  - `src/training/` (Laços de treinamento e otimização).
  - `src/inference/` (Integração LLM).
  - `src/utils/` (Utilitários globais).
  - `tests/` (Unittests cobrindo todos os módulos).

## 3. Gestão de Repositório e Jira
1. O repositório oficial é `geek2geeks/jurimetria_app` no GitHub.
2. O **Jira** será utilizado para rastreabilidade de todas as tarefas.
3. O desenvolvimento de novas Specs é feito numa branch `feature/[jira-id]-[nome-da-spec]`.
4. A branch `main` só recebe código que passa em todos os testes unitários.

## 4. Integração Analítica (DeepSeek 4 Pro)
O fluxo final utilizará o modelo PyTorch para prever a decisão (ex: "rejeitado" ou "concedido") e a API do **DeepSeek 4 Pro** para justificar a previsão com base no `sumario_texto`, garantindo Interpretabilidade da IA.
