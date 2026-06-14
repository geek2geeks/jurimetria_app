# Onboarding — Gleicy (P4: NumPy, TF-IDF e Split)

## O teu papel em linguagem simples

Tu transformas texto em números. Computadores não entendem palavras como pessoas; por isso, o teu módulo converte cada documento em uma linha de uma matriz NumPy. Essa matriz é o que o PyTorch vai receber depois.

## O que vais construir

- `src/features/vectorizer.py`;
- `tests/test_numpy.py`.

A tua classe principal será algo como:

```python
class NumPyTFIDF:
    def fit(self, textos: list[str]) -> None:
        ...

    def transform(self, textos: list[str]) -> np.ndarray:
        ...
```

## Por que isto é importante academicamente

O projeto precisa demonstrar uso real de NumPy. Num projeto de texto, isso não acontece automaticamente. A tua etapa é a evidência académica de que a equipa sabe transformar dados simbólicos em matrizes numéricas.

Também és responsável por evitar uma forma importante de erro científico: data leakage. O vocabulário e os pesos IDF devem ser aprendidos apenas no treino. Teste e inferência só podem usar `transform`.

## O contrato que deves respeitar

Entrada:

```python
DatasetRow(
    document_id="doc_001",
    text="prova pericial equidade indemnização",
    label_normalized="MANTIDA",
    tribunal="TRL",
    year=2015
)
```

Saída:

```python
X_train: np.ndarray
X_test: np.ndarray
y_train: np.ndarray
y_test: np.ndarray
```

Também deves guardar:

```text
artifacts/run_XXX/vectorizer/vocab.json
artifacts/run_XXX/vectorizer/idf.npy
artifacts/run_XXX/vectorizer/config.json
artifacts/run_XXX/labels/label_to_id.json
artifacts/run_XXX/labels/id_to_label.json
```

## O que deves estudar primeiro

1. O que é uma matriz.
2. O que é NumPy.
3. O que é Bag-of-Words.
4. O que é TF-IDF.
5. O que é treino/teste.
6. O que é data leakage.

## Como começar sem saber software

Não comeces com 10 mil documentos. Começa com 3 frases:

```python
textos = [
    "juiz nega recurso",
    "tribunal concede recurso",
    "juiz mantém decisão"
]
```

Constrói primeiro um vocabulário simples. Depois transforma cada frase numa linha de números. Depois adiciona TF-IDF.

## Teste mínimo esperado

O teu teste deve provar que:

- o vocabulário é criado só com dados de treino;
- `transform` mantém o mesmo número de colunas;
- labels são convertidas para números;
- os ficheiros `vocab.json` e `idf.npy` podem ser guardados e relidos.

Comando:

```bash
python -m unittest tests/test_numpy.py
```

## O que não deves fazer

Não uses `TfidfVectorizer` do scikit-learn. Não faças `fit` em todos os dados antes do split. Não leias PDFs diretamente. Não mudes a ordem das labels sem guardar os mapas.

## Como explicar na apresentação

Podes dizer:

> A vetorização NumPy converte texto jurídico em uma matriz numérica. Usámos `fit` apenas no treino para evitar vazamento estatístico e guardámos vocabulário, IDF e mapas de labels para permitir reprodutibilidade na inferência.

## Como usar IA na tua tarefa

Pede à IA para explicar cada fórmula de TF-IDF e as shapes antes da implementação. Exige testes numéricos pequenos e confirma manualmente os resultados. Rejeita qualquer proposta de `TfidfVectorizer` ou `train_test_split`. Revê, testa e declara o apoio de IA no PR.
