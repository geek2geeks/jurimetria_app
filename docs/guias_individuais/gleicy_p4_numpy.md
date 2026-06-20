# Guia — Gleicy (P4: NumPy, TF-IDF e divisão)

## O teu papel em linguagem simples

Tu transformas texto em números. Computadores não entendem palavras como pessoas; por isso, o teu módulo converte cada documento numa linha de uma matriz NumPy. Essa matriz é o que o PyTorch vai receber depois.

## O que vais construir

- `src/caracteristicas/vetorizador_tfidf.py`;
- `tests/test_vetorizador_tfidf.py`.

A tua classe principal será algo como:

```python
class VetorizadorTfidfNumPy:
    def fit(self, textos: list[str]) -> None:
        ...

    def transform(self, textos: list[str]) -> np.ndarray:
        ...
```

## Por que isto é importante academicamente

O projeto precisa demonstrar uso real de NumPy. Num projeto de texto, isso não acontece automaticamente. A tua etapa é a evidência académica de que a equipa sabe transformar dados simbólicos em matrizes numéricas.

Também és responsável por evitar uma forma importante de erro científico: fuga de informação. O vocabulário e os pesos IDF devem ser aprendidos apenas no treino. Teste e inferência só podem usar `transform`.

## O contrato que deves respeitar

Entrada:

```python
RegistoClassificacao(
    id_documento="documento_001",
    texto="prova pericial equidade indemnização",
    categoria_normalizada="MANTIDA",
    tribunal="TRL",
    ano=2015
)
```

Saída:

```python
caracteristicas_treino: np.ndarray
caracteristicas_teste: np.ndarray
categorias_treino: np.ndarray
categorias_teste: np.ndarray
```

Também deves guardar:

```text
artefactos/execucao_XXX/vetorizador/vocabulario.json
artefactos/execucao_XXX/vetorizador/idf.npy
artefactos/execucao_XXX/vetorizador/configuracao.json
artefactos/execucao_XXX/categorias/categoria_para_id.json
artefactos/execucao_XXX/categorias/id_para_categoria.json
```

## O que deves estudar primeiro

1. O que é uma matriz.
2. O que é NumPy.
3. O que é Bag-of-Words.
4. O que é TF-IDF.
5. O que é treino/teste.
6. O que é fuga de informação.

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
- categorias são convertidas para números;
- os ficheiros `vocabulario.json` e `idf.npy` podem ser guardados e relidos.

Comando:

```bash
python -m unittest tests/test_vetorizador_tfidf.py
```

## O que não deves fazer

Não uses `TfidfVectorizer` do scikit-learn. Não faças `fit` em todos os dados antes da divisão. Não leias PDFs diretamente. Não mudes a ordem das categorias sem guardar os mapas.

## Como explicar na apresentação

Podes dizer:

> A vetorização NumPy converte texto jurídico numa matriz numérica. Usámos `fit` apenas no treino para evitar vazamento estatístico e guardámos vocabulário, IDF e mapas de categorias para permitir reprodutibilidade na inferência.

## Como usar IA na tua tarefa

Pede à IA para explicar cada fórmula de TF-IDF e as dimensões antes da implementação. Exige testes numéricos pequenos e confirma manualmente os resultados. Rejeita qualquer proposta de `TfidfVectorizer` ou `train_test_split`. Revê, testa e declara o apoio de IA no pedido de integração.

## Especificações Técnicas Originais

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
- Exportação dos artefactos MLOps da tua componente, na pasta da execução (layout em `docs/arquitetura.md` §2): `vetorizador/vocabulario.json`, `vetorizador/idf.npy`, `vetorizador/configuracao.json`, `categorias/categoria_para_id.json` e `categorias/id_para_categoria.json`. O mapa inverso `id_para_categoria.json` é o que o P7 usa para descodificar o índice previsto na classe.

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