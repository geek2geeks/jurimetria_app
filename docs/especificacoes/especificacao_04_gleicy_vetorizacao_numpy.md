# Especificação 04 — Vetorização TF-IDF com NumPy

## Responsável
Gleicy — Vetorização NumPy e divisão dos dados (P4)

## Jira
`SCRUM-8`

## Objetivo em linguagem simples
A tua missão é transformar palavras em números por meio de TF-IDF. O Pedro fornece-te uma lista estruturada de instâncias de `RegistoClassificacao`. Deves dividir este conjunto em treino e teste usando exclusivamente NumPy, calcular os pesos das palavras e converter os textos em matrizes para treinar o modelo PyTorch.

## Porque é importante
O TF-IDF tem de ser programado usando apenas `NumPy`, como requisito da disciplina. Além disso, a separação clara entre `fit` e `transform` é obrigatória para evitar fuga de informação.

## Entradas
Uma lista agregada final de objetos `RegistoClassificacao`.

## Saídas
- `caracteristicas_treino`, `caracteristicas_teste`, `categorias_treino` e `categorias_teste` (matrizes NumPy).
- Exportação dos artefactos MLOps da tua componente: `vocabulario.json`, `idf.npy` e `categoria_para_id.json`.

## Ficheiros a criar ou alterar
- `src/caracteristicas/vetorizador_tfidf.py`
- `tests/test_vetorizador_tfidf.py`

## Lista de trabalho
- [ ] Revê a regra MLOps de fuga de informação na `constitution.md`.
- [ ] Cria uma função própria de divisão treino/teste baseada numa `semente` fixa e em NumPy puro. **Não podes** usar `train_test_split` da biblioteca scikit-learn.
- [ ] Escreve o vetorizador (`class VetorizadorTfidfNumPy`).
- [ ] **REGRA CRÍTICA:** o `fit` ocorre estritamente e apenas nos textos de treino. A validação e o teste só podem passar por `transform`.
- [ ] Guarda o trabalho no disco usando `json.dump` e `np.save()` na pasta de artefactos. Estes ficheiros são necessários para a inferência e a reconstrução do modelo.

## Exemplo
Exportação local dos artefactos:
- `vocabulario.json`: dicionário de tokens mapeados.
- `idf.npy`: matriz NumPy com os pesos.

## Testes
Comando: `python -m unittest tests/test_vetorizador_tfidf.py`. Cobre o cálculo exato do TF-IDF para uma frase curta.

## Critérios de conclusão
- NumPy nativo (nada de dependências scikit-learn).
- Ficheiros bem guardados na hierarquia MLOps estipulada.
- Semente controlada para que as divisões sejam reproduzíveis.

## O que não fazer
- Não carregues documentos diretamente; consome a lista enviada pelo fluxo central.
- Não apliques `fit` sobre todos os dados antes da divisão.

## Dependências
- Consomes a lista de `RegistoClassificacao` providenciada pela integração de P8.
- Gravas os dados para P5 (Helton) alimentar a rede neural, e disponibilizas os teus artefactos para P7 (Sandro).

## Fluxo Git
- Ramo sugerido: `funcionalidade/SCRUM-8-vetorizador-tfidf`
- Commit: `[SCRUM-8] Adicionar vetorizador TF-IDF e divisão dos dados`

## Comentários esperados
- Adiciona docstrings que detalhem o formato e as dimensões de `caracteristicas` e `categorias`.
- Justifica com um comentário claro a restrição de executar o `fit` só no treino.
