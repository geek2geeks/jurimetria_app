# Fluxo de desenvolvimento assistido por IA

## Posição do projeto

O professor aprovou a equipa de oito membros, mas não concedeu uma autorização específica para código gerado por IA. Cada aluno continua responsável por cumprir as regras da disciplina.

Se o uso de IA for permitido e o aluno decidir utilizá-la, deve seguir este fluxo. A IA é uma ferramenta de apoio, não a autoridade final.

> A IA pode escrever código, mas uma pessoa é responsável pelo código.

## Por que usar um fluxo controlado

Uma IA pode:

- explicar sintaxe e conceitos desconhecidos;
- ajudar a compreender uma spec;
- propor planos pequenos;
- criar rascunhos de código, testes e documentação;
- encontrar erros e sugerir refatorações.

Também pode:

- inventar requisitos;
- alterar contratos sem perceber o impacto;
- produzir testes fracos;
- introduzir data leakage;
- expor segredos ou dados pessoais;
- gerar código que parece correto, mas não funciona.

Por isso, toda a saída de IA é um rascunho.

## Fluxo obrigatório

1. Ler `constitution.md`, a spec da tarefa, `docs/architecture.md` e este documento.
2. Confirmar o ticket Jira e criar uma branch.
3. Usar `/speckit.clarify` para identificar dúvidas.
4. Rever as respostas com uma pessoa.
5. Usar `/speckit.plan`.
6. Confirmar que o plano é pequeno e respeita os contratos.
7. Usar `/speckit.tasks`.
8. Usar `/speckit.analyze` ou `/speckit.checklist`.
9. Só depois usar `/speckit.implement`.
10. Ler o diff linha a linha.
11. Executar os testes.
12. Abrir um Pull Request e declarar o apoio de IA.
13. Obter revisão humana antes do merge.

Nunca dês à IA autorização para fazer merge automático em `main`.

## Revisão humana obrigatória

O autor deve:

- compreender as entradas, saídas e dependências;
- confirmar a implementação contra a spec;
- verificar `constitution.md`;
- verificar type hints e testes;
- executar:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

- confirmar que não existem segredos nem dados reais no diff;
- abrir um Pull Request.

Pedro é o revisor obrigatório dos PRs dos outros membros. Quando Pedro for o autor, outro membro deve rever. Autoaprovação não é revisão humana.

## O que a IA pode fazer

- explicar specs;
- criar um plano;
- gerar rascunhos de código;
- propor e escrever testes;
- melhorar docstrings;
- explicar erros;
- rever código;
- refatorar dentro do escopo aprovado;
- escrever documentação.

## O que a IA não pode fazer

- inventar contratos do projeto;
- alterar `RawDocument`, `Acordao` ou `DatasetRow` sem Pedro e Daniela;
- decidir sozinha novas dependências;
- contornar testes;
- efetuar merge em `main`;
- usar `decisao_raw`, texto dispositivo, ECLI, URL ou `full_text` como feature;
- receber PDFs, JSONs reais, dados pessoais, `.env`, chaves ou artefactos identificáveis;
- apresentar texto gerado como aconselhamento jurídico ou explicabilidade científica.

## Prompt recomendado

```text
Estou a trabalhar no projeto académico JurisTriage PT.

Lê primeiro:
- constitution.md
- a minha spec em docs/specs/
- docs/architecture.md
- docs/ai_development_workflow.md

A minha tarefa é: [descrever a tarefa e indicar o ticket Jira]

Antes de editar:
1. Explica a tarefa em linguagem simples.
2. Identifica entradas e saídas.
3. Identifica dependências de outros membros.
4. Aponta ambiguidades.
5. Propõe um plano pequeno.
6. Propõe testes unittest.
7. Espera pela minha confirmação.

Regras:
- Respeita RawDocument, Acordao e DatasetRow.
- Usa type hints e unittest.
- Não uses dados jurídicos reais nos prompts ou testes.
- Não adiciones segredos.
- Não faças merge.
- Não alteres ficheiros fora do escopo.
```

## GitHub Spec Kit

O projeto fixa o Spec Kit em `v0.10.2`. A instalação completa está em `docs/software_setup.md`.

Comandos principais:

```text
/speckit.constitution
/speckit.specify
/speckit.clarify
/speckit.plan
/speckit.tasks
/speckit.analyze
/speckit.checklist
/speckit.implement
```

As specs existentes em `docs/specs/` continuam a ser a referência das tarefas. Pedro deve inicializar ou atualizar a integração do Spec Kit uma única vez e rever todos os ficheiros gerados antes de os publicar.

## Declaração no Pull Request

Usa uma frase objetiva:

```text
Apoio de IA: Sim.
Ferramenta: OpenCode com DeepSeek V4 Pro.
Utilização: esclarecimento da spec, plano, rascunho de testes e revisão.
Validação humana: li o diff, executei os testes e compreendo as alterações.
```

Se não foi usada IA, escreve `Apoio de IA: Não`.
