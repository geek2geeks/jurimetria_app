# Especificação 06 — Modelo de referência, métricas e avaliação

## Responsável
Luciana — Modelo de referência, métricas e avaliação (P6)

## Jira
`SCRUM-10`

## Objetivo em linguagem simples
A verdadeira prova matemática do projeto reside na tua análise. Vais comparar as previsões da rede do Helton (P5) com as categorias reais fornecidas pela Gleicy (P4). Além disso, crias um modelo de referência que prevê sempre a classe maioritária. No final, deves exportar os resultados para `metricas.json` e referenciá-los no manifesto.

## Porque é importante
Garante o escrutínio e a prova empírica. Num conjunto de dados desequilibrado, avaliar apenas com exatidão pode apresentar valores artificialmente elevados. O projeto precisa também de `Macro-F1`. A exportação em JSON preserva as métricas daquela execução no fluxo reprodutível.

## Entradas
- Vetor de previsões do modelo (`categorias_previstas`).
- Vetor de categorias reais do teste (`categorias_reais`).

## Saídas
- Registo da avaliação `metricas.json`.

## Ficheiros a criar ou alterar
- `src/avaliacao/metricas.py`
- `tests/test_metricas.py`

## Lista de trabalho
- [ ] Confirma as exigências de modelo de referência e isolamento da biblioteca sklearn na `constitution.md`.
- [ ] Desenha a classe `ModeloReferenciaClasseMaioritaria` - a estratégia cega que prevê sempre o número mais prevalente no treino.
- [ ] Importa as tuas métricas autorizadas da sklearn: `accuracy_score`, `f1_score`.
- [ ] Cria a rotina `avaliar_execucao(categorias_reais, categorias_previstas) -> dict` que irá formatar o dicionário dos resultados (Macro F1 incluído).
- [ ] Exporta esses resultados `json.dump` na diretoria correspondente dos artefactos.

## Exemplo
Exemplo da tua exportação:
`{"exatidao": 0.81, "macro_f1": 0.66, "macro_f1_referencia": 0.20}`

## Testes
Cria `tests/test_metricas.py` para garantir que o modelo de referência funciona devidamente com matrizes simuladas.

## Critérios de conclusão
- Provas unitárias criadas que comparam e provam as limitações de usar a métrica exatidão sozinha.
- Módulo exporta um `.json` funcional localmente.

## O que não fazer
- Não apresentes as métricas apenas com impressões transitórias no terminal. O relatório deve ser guardado.

## Dependências
- Consomes as saídas do modelo e da verificação. Ajudas o responsável técnico (P8) a agregar estas informações de forma acessível no sistema.

## Fluxo Git
- Ramo: `funcionalidade/SCRUM-10-metricas-referencia`
- Commit: `[SCRUM-10] Adicionar modelo de referência e métricas`

## Comentários esperados
- Docstrings objetivas nas funções matemáticas, descrevendo o formato de `categorias_reais` e `categorias_previstas`.
- Justifica com notas simples as escolhas algorítmicas ao nível de avaliação contra distribuições assimétricas.
