# Onboarding — Luciana (P6: Baseline, Métricas e Avaliação)

## O teu papel em linguagem simples

Tu respondes à pergunta científica mais importante: o modelo é realmente melhor do que uma estratégia simples? Para isso, comparas as previsões do modelo com as respostas verdadeiras e calculas métricas como Accuracy e Macro-F1.

## O que vais construir

- `src/evaluation/metrics.py`;
- `tests/test_evaluation.py`.

Também vais produzir:

```text
artifacts/run_XXX/metrics.json
```

## Por que isto é importante academicamente

A disciplina exige avaliação experimental. Em IA, não basta treinar um modelo: é preciso provar, com métricas, que ele aprendeu algo útil.

A tua etapa é essencial porque dados jurídicos podem ser desequilibrados. Se 80% dos casos forem `MANTIDA`, um modelo que responde sempre `MANTIDA` pode parecer bom em Accuracy, mas ser fraco cientificamente. Macro-F1 ajuda a avaliar melhor todas as classes.

## O contrato que deves respeitar

Entrada:

```python
y_true = np.array([0, 1, 1, 2])
y_pred = np.array([0, 1, 0, 2])
```

Saída:

```json
{
  "accuracy": 0.75,
  "macro_f1": 0.70,
  "baseline_macro_f1": 0.20
}
```

## O que deves estudar primeiro

1. O que é uma métrica.
2. O que é Accuracy.
3. O que é Precision e Recall.
4. O que é Macro-F1.
5. O que é uma baseline.
6. Por que classes desequilibradas podem enganar.

## Como começar sem saber software

Começa com arrays inventados. Não esperes pelo modelo do Helton. Cria uma função que recebe `y_true` e `y_pred` e devolve um dicionário.

Depois implementa a baseline: descobrir qual é a classe mais frequente no treino e prever sempre essa classe.

## Teste mínimo esperado

O teu teste deve provar que:

- a baseline encontra a classe maioritária;
- Accuracy e Macro-F1 são calculadas;
- um caso desequilibrado mostra Accuracy alta mas Macro-F1 baixa;
- `metrics.json` pode ser guardado.

Comando:

```bash
python -m unittest tests/test_evaluation.py
```

## O que não deves fazer

Não uses só `print`. Não digas que o modelo é bom apenas porque tem Accuracy alta. Não dependas de um modelo real para testar as funções.

## Como explicar na apresentação

Podes dizer:

> Avaliámos o modelo contra uma baseline de classe maioritária. Como o problema pode ter classes desequilibradas, usamos Macro-F1 para medir desempenho de forma mais justa entre todas as classes.

## Como usar IA na tua tarefa

Pede à IA exemplos pequenos para explicar Accuracy, Macro-F1 e baseline. Confirma os valores com arrays conhecidos. A IA não pode declarar que o modelo é bom sem evidência. Revê o relatório, executa os testes e declara o apoio de IA no PR.
