# Onboarding — Pedro (P8: Integração, Tech Lead, QA e MLOps)

## O teu papel em linguagem simples

Tu és responsável por garantir que as peças de todos encaixam. Não significa fazer o trabalho dos colegas; significa definir contratos, proteger a arquitetura, rever PRs, organizar Jira e garantir que o projeto consegue rodar de ponta a ponta.

## O que vais construir ou coordenar

- `src/data/schemas.py`, em conjunto com Daniela;
- `src/data/dataset_builder.py`;
- `.github/workflows/python-tests.yml`;
- `main.py` ou `run_pipeline.py`;
- `artifacts/run_XXX/manifest.json`;
- documentação de requisitos, arquitetura, decisões e onboarding.

## Por que isto é importante academicamente

A disciplina não avalia apenas modelo. Ela avalia engenharia de software aplicada a IA. A tua função é tornar visível essa engenharia: modularização, rastreabilidade, testes, documentação, Git e reprodutibilidade.

Num projeto de grupo, a integração é frequentemente onde tudo falha. O teu papel demonstra capacidade de coordenação técnica, validação de interfaces e controlo de qualidade.

## O contrato que deves proteger

Fluxo central:

```text
RawDocument -> Acordao -> DatasetRow -> NumPy arrays -> PyTorch model -> metrics -> manifest -> inference
```

O `manifest.json` deve ligar todos os artefactos de uma execução:

```text
run_id: run_001
seed: 42
vectorizer: vectorizer/vocab.json
idf: vectorizer/idf.npy
labels: labels/id_to_label.json
model_config: model/model_config.json
weights: model/weights.pth
metrics: metrics.json
```

## O que deves estudar primeiro

1. O que é integração.
2. O que é CI/CD.
3. O que é contrato de dados.
4. O que é manifest.
5. O que é code review.
6. O que é rastreabilidade.
7. Como impedir data leakage.

## Como começar sem saber tudo

Primeiro garante as pastas e os contratos. Depois cria um `dataset_builder.py` mínimo que recebe 2 `Acordao` falsos e devolve 2 `DatasetRow`. Depois cria o workflow GitHub Actions para correr `python -m unittest`.

Não esperes o projeto inteiro para criar a integração. Usa mocks e dados pequenos.

## Teste mínimo esperado

Deves garantir que:

- `schemas.py` pode ser importado por todos;
- `dataset_builder.py` remove documentos sem label válida;
- o workflow roda `python -m unittest`;
- `manifest.json` aponta para ficheiros relativos;
- PRs que quebram testes não entram na `main`.

## O que não deves fazer

Não centralizes tudo em ti. Não deixes colegas passar dicionários soltos. Não aproves `torch.save(model)`. Não deixes `fit` do TF-IDF acontecer fora do treino. Não permitas dados reais identificáveis no repositório.

## Como explicar na apresentação

Podes dizer:

> A integração foi desenhada com contratos de dados e manifestos de execução. Isto garante que cada módulo pode ser desenvolvido por uma pessoa diferente, mas o sistema continua reprodutível, testável e coerente de ponta a ponta.

## Como usar IA na tua tarefa

Usa IA para comparar contratos, gerar checklists e encontrar riscos entre módulos, nunca para aprovar automaticamente um PR. Revê cada mudança arquitetural e protege dados e segredos. Os teus próprios PRs precisam de revisão por outro membro humano.
