# Guia — Luciana (P6: modelo de referência, métricas e avaliação)

## O teu papel em linguagem simples

Tu respondes à pergunta científica mais importante: o modelo é realmente melhor do que uma estratégia simples? Para isso, comparas as previsões do modelo com as respostas verdadeiras e calculas métricas como exatidão e Macro-F1.

## O que vais construir

- `src/avaliacao/metricas.py`;
- `tests/test_metricas.py`.

Também vais produzir:

```text
artefactos/execucao_XXX/metricas.json
```

## Por que isto é importante academicamente

A disciplina exige avaliação experimental. Em IA, não basta treinar um modelo: é preciso provar, com métricas, que ele aprendeu algo útil.

A tua etapa é essencial porque dados jurídicos podem ser desequilibrados. Se 80% dos casos forem `MANTIDA`, um modelo que responde sempre `MANTIDA` pode parecer bom em exatidão, mas ser fraco cientificamente. Macro-F1 ajuda a avaliar melhor todas as classes.

## O contrato que deves respeitar

Entrada:

```python
categorias_reais = np.array([0, 1, 1, 2])
categorias_previstas = np.array([0, 1, 0, 2])
```

Saída:

```json
{
  "exatidao": 0.75,
  "macro_f1": 0.70,
  "macro_f1_referencia": 0.20
}
```

## O que deves estudar primeiro

1. O que é uma métrica.
2. O que é exatidão.
3. O que são precisão e sensibilidade.
4. O que é Macro-F1.
5. O que é um modelo de referência.
6. Por que classes desequilibradas podem enganar.

## Como começar sem saber software

Começa com matrizes inventadas. Não esperes pelo modelo do Helton. Cria uma função que recebe `categorias_reais` e `categorias_previstas` e devolve um dicionário.

Depois implementa o modelo de referência: descobre qual é a classe mais frequente no treino e prevê sempre essa classe.

## Teste mínimo esperado

O teu teste deve provar que:

- o modelo de referência encontra a classe maioritária;
- exatidão e Macro-F1 são calculadas;
- um caso desequilibrado mostra exatidão alta mas Macro-F1 baixa;
- `metricas.json` pode ser guardado.

Comando:

```bash
python -m unittest tests/test_metricas.py
```

## O que não deves fazer

Não uses só `print`. Não digas que o modelo é bom apenas porque tem exatidão alta. Não dependas de um modelo real para testar as funções.

## Como explicar na apresentação

Podes dizer:

> Avaliámos o modelo contra um modelo de referência de classe maioritária. Como o problema pode ter classes desequilibradas, usamos Macro-F1 para medir o desempenho de forma mais justa entre todas as classes.

## Como usar IA na tua tarefa

Pede à IA exemplos pequenos para explicar exatidão, Macro-F1 e modelo de referência. Confirma os valores com matrizes conhecidos. A IA não pode declarar que o modelo é bom sem evidência. Revê o relatório, executa os testes e declara o apoio de IA no PR.

## Especificações Técnicas Originais

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