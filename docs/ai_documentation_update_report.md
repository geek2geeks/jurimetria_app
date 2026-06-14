# Relatório da atualização de documentação sobre IA

## Resumo

A documentação passou a explicar um fluxo opcional e controlado de desenvolvimento assistido por IA. Não afirma que o professor autorizou IA. Todo código gerado deve ser compreendido, testado, declarado no PR e revisto por uma pessoa.

## Novos ficheiros

- `docs/ai_development_workflow.md`
- `docs/software_setup.md`
- `docs/development_best_practices.md`
- `docs/github_jira_workflow.md`
- `docs/ai_documentation_update_report.md`
- `.github/workflows/python-tests.yml`
- `.github/pull_request_template.md`
- `.github/CODEOWNERS`
- `jira_assignees.example.json`
- `tests/test_repository_setup.py`

## Principais ficheiros atualizados

- `constitution.md`
- `README.md`
- `.env.example`
- `.gitignore`
- `requirements.txt`
- `create_jira_tasks.py`
- `docs/onboarding_for_beginners.md`
- `docs/onboarding_individual/README.md`
- os oito onboardings individuais;
- as oito specs;
- documentos de requisitos, decisões, ética, visão e inspeção dos PDFs.

## Políticas adicionadas

- IA é opcional e depende das regras académicas.
- A resposta de IA é sempre um rascunho.
- Revisão humana é obrigatória.
- Pedro revê os PRs dos colegas.
- Pedro pode validar os próprios PRs como administrador, documentando testes, riscos e decisão.
- O uso de IA deve ser declarado.
- Dados jurídicos reais, dados pessoais e segredos não podem ser enviados a serviços externos.
- OpenCode, DeepSeek e Spec Kit são recomendações, não requisitos académicos.

## Instalação documentada

Foram adicionadas instruções para Windows e macOS:

- Anaconda/conda com Python 3.11;
- OpenCode `>=1.14.24`;
- ligação ao DeepSeek por `/connect`;
- DeepSeek V4 Pro;
- uv;
- GitHub Spec Kit fixado em `v0.10.2`;
- comandos de teste e diagnóstico.

## Segurança

- Nenhuma chave real foi escrita em ficheiros.
- `.env`, `auth.json`, `*.key` e configurações Jira locais estão ignorados.
- O token Jira colocado numa conversa deve ser considerado exposto e revogado.
- A chave DeepSeek partilhada deve ter limites, rotação e revogação.

## GitHub e Jira

- As alterações estão publicadas na branch `codex/onboarding-ai-workflow` e no Pull Request 1.
- Pedro e um colega já têm acesso; seis convites GitHub aguardam aceitação.
- A branch `main` está protegida e exige uma aprovação humana.
- As oito tarefas foram criadas pelo Atlassian CLI: `SCRUM-5` a `SCRUM-12`.
- `SCRUM-12` está atribuída ao Pedro. Os emails dos restantes colegas foram recebidos, mas as contas ainda não estão disponíveis no site Jira para atribuição.
- A autenticação utilizou OAuth; o token exposto não foi reutilizado.

## Riscos pendentes

- O professor ainda não confirmou se aceita IA na programação.
- O repositório é público; amostras e logs exigem revisão antes do commit.
- O projeto Jira e os acessos dos colegas ainda precisam de confirmação autenticada.
- A implementação funcional ainda não existe.
- O GitHub Actions está bloqueado por um problema de faturação da conta; os testes locais passam.

## Próximas ações

1. Revogar e substituir o token Jira exposto.
2. Convidar ou ativar os sete colegas no site Jira e atribuir `SCRUM-5` a `SCRUM-11`.
3. Confirmar que todos os colegas conseguem abrir as respetivas tarefas.
4. Pedro valida e faz merge do Pull Request 1, documentando o bypass do CI bloqueado pela faturação.
5. Resolver o bloqueio de faturação do GitHub Actions.
6. Convidar os colegas.
7. Cada membro instala o ambiente, lê o onboarding e começa pela sua spec.
