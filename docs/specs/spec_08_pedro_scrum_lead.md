# Spec 08 — Scrum Lead, Integração, MLOps e Manifest

## Assignee
Pedro — Tech Lead, Integração, Requisitos, e MLOps (P8)

## Jira
`SCRUM-12`

## Plain-language goal
Como responsável técnico do fluxo, assumes o papel de garantir que todos os blocos de código encaixam na perfeição. Trabalhas na génese dos contratos de dados (`schemas.py` com a Daniela) para assegurar formatos consistentes, construindo o motor integrador do projeto (`dataset_builder.py`). Este script processa as dezenas de `Acordaos`, passa-os pelo módulo de limpeza, e solidifica-os sob a forma do dataset pronto: `DatasetRow`. Além de dominares a esteira do CI/CD com o Github Actions, tens a incumbência final de emitir o `manifest.json`.

## Why this matters
Garante que o repositório é funcional de ponta a ponta. Se as pipelines de conversão quebrassem na estrutura (`Acordao` para `DatasetRow`), nenhum aluno subsequente poderia trabalhar. O manifesto MLOps serve como a "Certidão de Nascimento" do modelo, garantindo o registo seguro das suas componentes (vocabulário, treino e pesos da rede) para a reprodução futura da experiência.

## Inputs
- Os módulos limpos e funcionais do ecossistema.
- Os objetos instanciados do fluxo inicial de `Acordao`.

## Outputs
- As definições lógicas essenciais de `schemas.py` desenhadas e afinadas.
- O script integrador global: `dataset_builder.py` a exportar instâncias limpas de `DatasetRow`.
- O empacotamento MLOps final (manifest script) a compilar para a pasta local os dados do `manifest.json`.

## Files to create or edit
- `src/data/schemas.py` (Copropriedade com P2)
- `src/data/dataset_builder.py`
- `.github/workflows/python-tests.yml`
- Pipeline runner (e.g. `main.py` ou `run_pipeline.py`)

## Step-by-step checklist
- [ ] Confirma e garante o rastreio rigoroso dos contratos (Data Loader, Schema, etc.) estipulados na `constitution.md`.
- [ ] Estabelece em Python as Dataclasses base fortes: `RawDocument`, `Acordao` e `DatasetRow`.
- [ ] Desenvolve a base iteradora do construtor. Para cada objeto lido, executa a purificação associada à limpeza da decisão e a emissão final sob a forma unitária orientada ao ML (`DatasetRow`).
- [ ] Prepara o YML Actions que rodará ciclicamente a pasta `tests/` confirmando a higidez do código face aos sucessivos PRs dos teus colegas.
- [ ] Quando efetuares as extrações para treino, garante que escreves fisicamente a `seed` base do teu teste, links e resultados estatísticos num objeto e o guardas com o registo de metadata total em formato JSON na sub-pasta daquele `run_XXX`.

## Example
Modelo do Manifest que deves guardar em `artifacts/run_XXX/manifest.json`:
```json
{
  "run_id": "run_001",
  "seed": 42,
  "vectorizer": "vectorizer/vocab.json",
  "weights": "model/weights.pth",
  "labels": "labels/id_to_label.json"
}
```

## Tests
Mantém uma bateria de testes rígida que possa processar rapidamente pequenas amostras no Github Actions sem onerar os recursos da equipa. Os Unittests provam a integridade dos módulos aglomerados.

## Definition of Done
- Esquemas de classes bem formatados e em produção limpa nas etapas do pipeline.
- GitHub Actions ativado e reprodutibilidade preservada nos manifestos gerados.

## What not to do
- Mantém o foco no controlo de integridade de data leakage. Se notares falhas ou passagem de `Decisão Integral` indevida a jusante da Pipeline, intervém junto do grupo.
- Evita aprovar Pull Requests de código solto sem a devida cobertura de documentação dos outros alunos.

## Dependencies
- Assumes um papel de vigilância e coordenação. Afinas com a Daniela os schemas, monitorizas as filtragens do Gustavo, recebes e atestas os ficheiros do Helton e Gleicy e crias as referências do manifest usadas futuramente pela inferência.

## Git workflow
- Garante o code review na main e monitoriza as interações gerais do grupo ao submeter as suas branches funcionais.
- Usa uma branch `feature/SCRUM-12-integracao`. Podes validar o teu próprio PR como administrador, documentando os testes, riscos e decisão.

## Commenting expectations
- Nos teus ficheiros de Pipeline (`main.py` e construtores), o foco dos comentários assenta em demarcar limites de módulos (por que limitámos os campos nulos ali, justificação das sementes, etc.).
