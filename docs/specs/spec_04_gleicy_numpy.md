# Especificação: Vetorização Matemática e Split (NumPy puro)

**Assignee:** Gleicy (P4 - Engenheiro Feature e NumPy)
**Fase do SDD:** Specify

## 1. Contexto (O Porquê)
As redes neurais do PyTorch (P5) aceitam tensores e números, não aceitam as palavras da lei cruas. A tua responsabilidade é converter o texto limpo do Gustavo em Matrizes Matemáticas. Crucialmente, para garantir os **10% da nota académica** focada no rigor matricial, não podes usar atalhos como a classe `TfidfVectorizer` da biblioteca `scikit-learn`. Todo o Feature Engineering deve ser programado na unha com **NumPy**.

## 2. Tarefa Técnica (O Quê)
1. Criar o módulo `src/features/vectorizer.py`.
2. Implementar a classe `NumpyTFIDF` que recebe uma lista de *strings* limpas e devolve uma matriz Numpy 2D de floats (`np.ndarray`). A classe deve gerir o dicionário de Vocabulário.
3. Criar a função `stratified_split(X: np.ndarray, y: np.ndarray, test_size: float)` usando máscaras de indexação booleana do NumPy para garantir que o balanço entre "Mantida" e "Revogada" é preservado tanto no treino como no teste.

## 3. Inputs e Outputs
- **Input:** `List[str]` (corpus do dataset limpo) e `List[str]` (Labels).
- **Output:** Múltiplos Arrays do NumPy: `X_train`, `X_test`, `y_train`, `y_test`.
- **Tipo Exigido:** `np.ndarray` e conversão de classes string para Inteiros `0, 1, 2...` no vetor de saída.

## 4. Regras e Restrições SDD
- **Proibido Importar:** `sklearn`, `pandas` (para operações numéricas core).
- **Mandatório Importar:** `import numpy as np`.
- **Eficiência Vetorial:** O código TF-IDF deve usar broadcasting e arrays multidimensionais do numpy (ex: `np.log`, `np.sum(axis=0)`) evitando totalmente o uso de loops `for` lentos sobre as 10.000 amostras.

## 5. Critérios de Aceitação (DoD)
- [ ] Passagem em todos os `unittests` do ficheiro `tests/test_numpy.py`.
- [ ] Prova visual (`print`) da forma da matriz, ex: `X_train.shape = (8000, 5000)`.
- [ ] O TF-IDF do Numpy demora menos de 10 segundos a vetorizar as 10 mil sentenças.

---

> **Instrução para Agente de IA:**
> Leia a `constitution.md`.
> **Extremamente Crítico:** Este é o módulo académico do NumPy. Executa `/speckit.clarify` com a Gleicy para debater como vais fazer a contagem Term-Frequency sem estourar RAM com uma matriz densa se o vocabulário crescer para além de 10.000 palavras. Após o plano, gera o `/speckit.implement`.
