# Revisão ficheiro a ficheiro

**Data:** 15 de junho de 2026
**Escopo:** prontidão para distribuir o projeto à equipa.

## Resultado geral

A documentação de arquitetura, instalação, GitHub, Jira, IA e responsabilidades individuais está preparada localmente. O pipeline funcional ainda não está implementado; será construído pelas oito tarefas.

O projeto só deve ser distribuído depois de:

1. obter revisão e integrar o pedido de integração 1;
2. convidar os sete colegas para GitHub e Jira;
3. criar e atribuir as oito tarefas Jira;
4. rodar o token Jira que foi exposto numa conversa;
5. resolver o bloqueio de faturação do GitHub Actions.

## Raiz

| Item | Estado | Observação |
|---|---|---|
| `constitution.md` | OK | Política de IA, revisão, etiquetas, privacidade e fuga de informação explícitas. |
| `README.md` | OK | Ordem de leitura, instalação e estado real do projeto. |
| `requirements.txt` | OK | NumPy limitado a `<2.0` para compatibilidade com scikit-learn 1.3. |
| `.env.example` | OK | Apenas placeholders; inclui DeepSeek e Jira. |
| `.gitignore` | OK | Ignora segredos, autenticação, responsáveis Jira locais e relatório com caminhos privados. |
| `criar_tarefas_jira.py` | OK local | API v3, simulação por defeito, atribuição e prevenção de duplicados. |
| `pdf_inspection_results.json` | Não publicar | Contém caminhos locais e está ignorado. |

## GitHub

| Item | Estado | Observação |
|---|---|---|
| Repositório remoto | Existe | `geek2geeks/jurimetria_app`, público, com o ramo principal `main`. |
| Conteúdo remoto | Em revisão | Alterações publicadas no ramo histórico `codex/onboarding-ai-workflow` e no pedido de integração 1. |
| Acessos | Parcial | Pedro e um colega têm acesso; existem seis convites de escrita pendentes. |
| Modelo de pedido de integração | Em revisão | Inclui ticket, testes, IA, privacidade e fuga de informação. |
| CODEOWNERS | Em revisão | Solicita revisão a `@geek2geeks`. |
| Integração contínua | Bloqueada externamente | Fluxo válido com Python 3.11, mas o GitHub não iniciou o executor porque a conta está bloqueada por um problema de faturação. |
| Proteção de `main` | Ativa | Exige PR, uma aprovação, histórico linear e resolução de conversas. |

## Jira

| Item | Estado | Observação |
|---|---|---|
| Site configurado | Confirmado | `fixola198.atlassian.net`. |
| Projeto | Confirmado | Chave `SCRUM`, nome `My Software Team`. |
| Tarefas | Criadas | `SCRUM-5` a `SCRUM-12`, uma por membro. |
| Responsáveis | OK | `SCRUM-5` a `SCRUM-12` estão atribuídas aos oito responsáveis. |
| Autenticação | OK | Atlassian CLI autenticado por OAuth; o token exposto não foi reutilizado. |

## Documentação

| Documento | Estado |
|---|---|
| `docs/instalacao_software.md` | Windows e macOS, Anaconda, OpenCode, DeepSeek, uv e Spec Kit. |
| `docs/fluxo_github_jira.md` | Fluxo diário completo para iniciantes. |
| `docs/fluxo_desenvolvimento_ia.md` | Uso condicional de IA, SDD e revisão humana. |
| `docs/boas_praticas_desenvolvimento.md` | Ramos, commits, testes, privacidade, MLOps e fuga de informação. |
| `docs/guia_iniciantes.md` | Reescrito com comandos seguros. |
| `docs/guias_individuais/*.md` | Cada membro tem instruções práticas e nomes públicos definidos. |

## Inconsistências corrigidas

- Python 3.10 versus requisito atual do Spec Kit: padronizado em Python 3.11.
- Jira `JPT-00X` versus projeto `SCRUM`: documentação usa a chave real produzida pelo Jira.
- `git add .` e `git reset` para iniciantes: substituídos por comandos controlados.
- Execução de zero testes: descoberta explícita e teste mínimo de configuração.
- LLM apresentada como explicabilidade: corrigida para texto opcional gerado.
- Probabilidade softmax apresentada como confiança: corrigida.
- Generalizações estatísticas da amostra PDF: removidas.
- `texto_integral` explicitamente proibido como característica.

## Pendências humanas

- Confirmar com o professor se o uso de IA é permitido para a avaliação.
- Pedir aos seis colegas com convite pendente que aceitem o acesso ao GitHub.
- Revogar a chave Jira exposta, mesmo não tendo sido reutilizada.
- Confirmar que os sete colegas aceitaram os convites Jira e conseguem abrir as tarefas.
- Resolver o bloqueio de faturação do GitHub e relançar o fluxo.
