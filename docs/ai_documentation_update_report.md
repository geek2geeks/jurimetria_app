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
- PRs do Pedro precisam de outro revisor.
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

- O GitHub remoto existe, mas estas alterações ainda precisam de ser publicadas.
- Pedro e um colega já têm acesso; seis convites GitHub aguardam aceitação.
- O script Jira foi preparado para criar oito tarefas de forma idempotente.
- A execução real requer um token novo, email da conta administradora e `accountId` dos oito membros.

## Riscos pendentes

- O professor ainda não confirmou se aceita IA na programação.
- O repositório é público; amostras e logs exigem revisão antes do commit.
- O projeto Jira e os acessos dos colegas ainda precisam de confirmação autenticada.
- A implementação funcional ainda não existe.
- A branch `main` ainda precisa de proteção.

## Próximas ações

1. Revogar e substituir o token Jira exposto.
2. Configurar os responsáveis Jira localmente.
3. Executar a simulação e depois criar as tarefas.
4. Publicar a documentação no GitHub.
5. Proteger `main`.
6. Convidar os colegas.
7. Cada membro instala o ambiente, lê o onboarding e começa pela sua spec.
