# Spec 06 — Evaluation, Metrics and Baseline (Métricas e Avaliação MLOps)

## Assignee
Luciana — Baseline, métricas e avaliação (P6)

## Jira
`SCRUM-10`

## Plain-language goal
A verdadeira prova matemática do projeto reside na tua análise. Vais cruzar as respostas dadas pela rede do Helton (P5) com as respostas verdadeiras fornecidas pela Gleicy (P4). Além disso, crias uma Baseline Cega de controlo. No final do processo, deves exportar os resultados numéricos gerados pela comparação para um ficheiro estático `metrics.json` de modo a que fiquem enraizados no Manifest.

## Why this matters
Garante o escrutínio e prova empírica. Num dataset desequilibrado, avaliar apenas com `Accuracy` pode apresentar valores artificialmente elevados. O projeto precisa do teu raciocínio usando `Macro-F1`. Além de provares isso no código, exportares a tua análise em `.json` imortaliza as métricas daquele `run` de modelo na pipeline.

## Inputs
- Array de previsões do teu modelo (`y_pred`).
- Array de realidades verdadeiras do teste (`y_true`).

## Outputs
- Registo da avaliação `metrics.json`.

## Files to create or edit
- `src/evaluation/metrics.py`
- `tests/test_evaluation.py`

## Step-by-step checklist
- [ ] Confirma as exigências de baseline e isolamento da biblioteca sklearn na `constitution.md`.
- [ ] Desenha a classe `MajorityClassBaseline` - a estratégia cega que prevê sempre o número mais prevalente no treino.
- [ ] Importa as tuas métricas autorizadas da sklearn: `accuracy_score`, `f1_score`.
- [ ] Cria a rotina `evaluate_run(y_true, y_pred) -> dict` que irá formatar o dicionário dos resultados (Macro F1 incluído).
- [ ] Exporta esses resultados `json.dump` na diretoria correspondente dos artefactos.

## Example
Exemplo da tua exportação:
`{"accuracy": 0.81, "macro_f1": 0.66, "baseline_macro_f1": 0.20}`

## Tests
Cria `tests/test_evaluation.py` para garantires assertivamente que a tua baseline funciona devidamente com *mock arrays*.

## Definition of Done
- Provas unitárias criadas que comparam e provam as limitações de usar a métrica Accuracy sozinha.
- Módulo exporta um `.json` funcional localmente.

## What not to do
- Não programes as métricas unicamente com "prints" transitórios no ecrã. O relatório MLOps tem de gravar.

## Dependencies
- Consomes os outputs de modelo e de verificação. Ajudas o Tech Lead (P8) a aglomerar estas informações de forma acessível no sistema.

## Git workflow
- Branch: `feature/SCRUM-10-metrics-baseline`
- Commit: `[SCRUM-10] Implement baseline model and export metric calculation`

## Commenting expectations
- Docstrings objetivas nas funções matemáticas descrevendo o formato pretendido do `y`.
- Justifica com notas simples as escolhas algorítmicas ao nível de avaliação contra distribuições assimétricas.
