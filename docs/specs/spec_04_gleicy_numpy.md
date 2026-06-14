# Spec 04 — NumPy Vectorizer (Vetorização)

## Assignee
Gleicy — Vetorização NumPy e Split dos Dados (P4)

## Plain-language goal
A tua missão é transformar palavras em números (TF-IDF Vectorization). O Pedro fornece-te uma lista estruturada de instâncias `DatasetRow`. Tu deves dividir este conjunto (em Treino e Teste) usando exclusivamente código teu (NumPy), aplicar a magia do TF-IDF para encontrares os pesos das palavras e converter as descrições textuais em matrizes dimensionais para treinar o PyTorch.

## Why this matters
O TF-IDF tem de ser programado usando apenas `NumPy` como requisito da disciplina. Além disso, a separação clara e isolada entre `fit` e `transform` é obrigatória para evitar "Data Leakage" académico.

## Inputs
Uma lista agregada final de objetos `DatasetRow`.

## Outputs
- `X_train`, `X_test`, `y_train`, `y_test` (Matrizes NumPy Arrays).
- Exportação dos artefactos MLOps da tua componente: `vocab.json`, `idf.npy` e `label_to_id.json`.

## Files to create or edit
- `src/features/vectorizer.py`
- `tests/test_numpy.py`

## Step-by-step checklist
- [ ] Revê a regra MLOps de Data Leakage na `constitution.md`.
- [ ] Cria a tua função de split (divisão treino/teste) baseada numa `seed` estática em NumPy puro. **Não podes** usar o `train_test_split` da biblioteca sklearn.
- [ ] Escreve o Vectorizador (`class NumPyTFIDF`).
- [ ] **REGRA CRÍTICA:** O `fit` (aprendizagem do vocabulário) ocorre ESTRITAMENTE e APENAS no `X_train`! A validação e o teste só podem passar por `transform`.
- [ ] Guarda o teu trabalho no disco usando `json.dump` e `np.save()` para a pasta de artefactos. Estes ficheiros são fulcrais para a Inferência e Reconstrução do Modelo.

## Example
Exportação local dos artefactos:
- `vocab.json`: O dicionário de tokens mapeados.
- `idf.npy`: A matriz numpy com os pesos.

## Tests
Comando: `python -m unittest tests/test_numpy.py`. Cobre o cálculo exato do TF-IDF para uma frase curta.

## Definition of Done
- NumPy nativo (nada de dependências scikit-learn).
- Ficheiros bem guardados na hierarquia MLOps estipulada.
- Seed matemática controlada para que os splits sejam reproduzíveis.

## What not to do
- Não carregues documentos sozinhos; consome a lista que a pipeline central te envia.
- Não apliques `fit` sobre os dados todos antes do split.

## Dependencies
- Consomes a lista de `DatasetRow` providenciada pela integração de P8.
- Gravas os dados para P5 (Helton) alimentar a rede neural, e disponibilizas os teus artefactos para P7 (Sandro).

## Git workflow
- Branch sugerida: `feature/<JIRA-KEY>-numpy-vector`
- Commit: `[<JIRA-KEY>] Implement custom NumPy TFIDF vectorizer and split logic`

## Commenting expectations
- Adiciona docstrings a detalhar o formato e dimensões ("Shapes") exatos de `X` e `y`.
- Justifica com um comentário claro a restrição de executar o `fit` só no treino.
