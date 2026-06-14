# Revisão ficheiro a ficheiro

**Data:** 15 de junho de 2026
**Escopo:** prontidão para distribuir o projeto à equipa.

## Resultado geral

A documentação de arquitetura, instalação, GitHub, Jira, IA e responsabilidades individuais está preparada localmente. O pipeline funcional ainda não está implementado; será construído pelas oito tarefas.

O projeto só deve ser distribuído depois de:

1. obter revisão e fazer merge do Pull Request 1;
2. convidar os sete colegas para GitHub e Jira;
3. criar e atribuir as oito tarefas Jira;
4. rodar o token Jira que foi exposto numa conversa;
5. resolver o bloqueio de faturação do GitHub Actions.

## Raiz

| Item | Estado | Observação |
|---|---|---|
| `constitution.md` | OK | Política de IA, revisão, labels, privacidade e data leakage explícitas. |
| `README.md` | OK | Ordem de leitura, instalação e estado real do projeto. |
| `requirements.txt` | OK | NumPy limitado a `<2.0` para compatibilidade com scikit-learn 1.3. |
| `.env.example` | OK | Apenas placeholders; inclui DeepSeek e Jira. |
| `.gitignore` | OK | Ignora segredos, autenticação, responsáveis Jira locais e relatório com caminhos privados. |
| `create_jira_tasks.py` | OK local | API v3, simulação por defeito, atribuição e prevenção de duplicados. Falta executar com credenciais novas. |
| `pdf_inspection_results.json` | Não publicar | Contém caminhos locais e está ignorado. |

## GitHub

| Item | Estado | Observação |
|---|---|---|
| Repositório remoto | Existe | `geek2geeks/jurimetria_app`, público, branch principal `main`. |
| Conteúdo remoto | Em revisão | Alterações publicadas na branch `codex/onboarding-ai-workflow` e no Pull Request 1. |
| Acessos | Parcial | Pedro e um colega têm acesso; existem seis convites de escrita pendentes. |
| Pull Request template | Em revisão | Inclui ticket, testes, IA, privacidade e leakage. |
| CODEOWNERS | Em revisão | Solicita revisão a `@geek2geeks`. |
| CI | Bloqueado externamente | Workflow válido com Python 3.11, mas o GitHub não iniciou o runner porque a conta está bloqueada por um problema de faturação. |
| Proteção de `main` | Ativa | Exige PR, uma aprovação, histórico linear e resolução de conversas. |

## Jira

| Item | Estado | Observação |
|---|---|---|
| Site configurado | Indício local | `fixola198.atlassian.net`. |
| Projeto esperado | Indício local | Chave `SCRUM`; ainda precisa de confirmação autenticada. |
| Tarefas | Criadas | `SCRUM-5` a `SCRUM-12`, uma por membro. |
| Responsáveis | Parcial | Pedro está atribuído a `SCRUM-12`; os sete emails foram recebidos, mas as contas ainda precisam de acesso ao site Jira. |
| Autenticação | OK | Atlassian CLI autenticado por OAuth; o token exposto não foi reutilizado. |

## Documentação

| Documento | Estado |
|---|---|
| `docs/software_setup.md` | Windows e macOS, Anaconda, OpenCode, DeepSeek, uv e Spec Kit. |
| `docs/github_jira_workflow.md` | Fluxo diário completo para iniciantes. |
| `docs/ai_development_workflow.md` | Uso condicional de IA, SDD e revisão humana. |
| `docs/development_best_practices.md` | Branches, commits, testes, privacidade, MLOps e leakage. |
| `docs/onboarding_for_beginners.md` | Reescrito com comandos seguros. |
| `docs/onboarding_individual/*.md` | Cada membro tem instruções práticas para IA. |

## Inconsistências corrigidas

- Python 3.10 versus requisito atual do Spec Kit: padronizado em Python 3.11.
- Jira `JPT-00X` versus projeto `SCRUM`: documentação usa a chave real produzida pelo Jira.
- `git add .` e `git reset` para iniciantes: substituídos por comandos controlados.
- Execução de zero testes: descoberta explícita e teste mínimo de configuração.
- LLM apresentada como explicabilidade: corrigida para texto opcional gerado.
- Probabilidade softmax apresentada como confiança: corrigida.
- Generalizações estatísticas da amostra PDF: removidas.
- `full_text` ausente da regra de leakage: agora explicitamente proibido.

## Pendências humanas

- Confirmar com o professor se o uso de IA é permitido para a avaliação.
- Pedir aos seis colegas com convite pendente que aceitem o acesso ao GitHub.
- Revogar a chave Jira exposta, mesmo não tendo sido reutilizada.
- Convidar ou ativar os sete colegas no site Jira e atribuir `SCRUM-5` a `SCRUM-11`.
- Pedro valida e faz merge do Pull Request 1, documentando o bypass do CI bloqueado pela faturação.
- Resolver o bloqueio de faturação do GitHub e relançar o workflow.
