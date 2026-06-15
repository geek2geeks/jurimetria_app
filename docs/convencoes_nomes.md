# Guia prático de nomes

A secção 9 de `constitution.md` contém as regras obrigatórias. Este guia reúne exemplos para consulta rápida.

## Regras

- Classes usam `PascalCase`: `DocumentoBruto`, `RegistoClassificacao`.
- Funções, variáveis, módulos e pastas usam `snake_case`: `carregar_pdfs`, `decisao_bruta`.
- Os identificadores não têm acentos, cedilhas nem espaços.
- Evita abreviaturas vagas como `doc`, `obj`, `tmp`, `res`, `val` ou `data`.
- Uma variável deve revelar o conteúdo: `documento_bruto`, `valores_previstos`, `caminho_manifesto`.
- Um booleano deve formular uma condição: `tem_sumario`, `modelo_carregado`.
- Uma função deve começar por um verbo: `limpar_texto`, `avaliar_execucao`, `guardar_manifesto`.
- Mantêm-se os nomes oficiais de bibliotecas, formatos, métricas e APIs: JSON, PDF, TF-IDF, NumPy, PyTorch, Jira e `state_dict`.

## Vocabulário comum

| Conceito | Nome adotado |
|---|---|
| Documento acabado de carregar | `DocumentoBruto` |
| Acórdão estruturado | `Acordao` |
| Registo pronto para classificação | `RegistoClassificacao` |
| Decisão original | `decisao_bruta` |
| Texto completo | `texto_integral` |
| Categoria final | `categoria_normalizada` |
| Identificador de uma execução | `id_execucao` |
| Semente aleatória | `semente` |
| Manifesto da execução | `manifesto.json` |

## Estrutura principal

```text
src/
├── dados/
├── pre_processamento/
├── caracteristicas/
├── modelos/
├── treino/
├── avaliacao/
└── inferencia/
```

Exemplos de módulos:

```text
carregador_pdf.py
carregador_json_bruto.py
esquemas.py
analisador_metadados.py
limpeza_texto.py
vetorizador_tfidf.py
rede_neuronal.py
treinar_modelo.py
metricas.py
motor_inferencia.py
```

Os testes mantêm o prefixo `test_`, necessário para descoberta automática, seguido de um nome português: `test_carregador_pdf.py`.

## Estabilidade de caminhos (links do quickstart distribuído)

O `quickstart.pdf` enviado à equipa (14/06/2026) aponta para ficheiros através de links GitHub `blob/main/<caminho>` e de menções a caminhos em texto. Como o GitHub mostra sempre a versão **atual** de cada caminho mas **não redireciona ficheiros movidos**, estes caminhos estão **congelados**: atualiza-se o conteúdo, nunca o local. Ver `ADR-06` em `docs/decisoes.md`.

**Não mover, renomear nem apagar:**

- Guias individuais: `docs/guias_individuais/alessandro_p1_ingestao.md`, `daniela_p2_metadados.md`, `gustavo_p3_limpeza.md`, `gleicy_p4_numpy.md`, `helton_p5_pytorch.md`, `luciana_p6_metricas.md`, `sandro_p7_inferencia.md`, `pedro_p8_integracao.md`.
- Documentos: `constitution.md`, `README.md`, `docs/quickstart.md`, `docs/instalacao_software.md`, `docs/fluxo_github_jira.md`, `docs/esquema_json_corpus.md`, `docs/criterios_avaliacao.md`, `docs/guia_iniciantes.md`, `data/README.md`, `src/dados/esquemas.py`.
- Pastas: `docs/guias_individuais/`, `docs/especificacoes/`, `src/` (e subpastas), `tests/`, `data/`, `artefactos/`.

**Atualizar documentação em segurança:**

1. Edita o ficheiro **no mesmo caminho**.
2. Cria uma branch, faz commit e abre PR para `main`.
3. Depois do merge, o link `blob/main/...` do quickstart passa a mostrar a versão nova — sem mudar o link nem re-enviar o PDF.

**Exceção:** se for mesmo necessário mover ou renomear um destes ficheiros, é preciso re-emitir o `quickstart.pdf` (`python construir_quickstart_pdf.py`) e redistribuí-lo, e atualizar o `ADR-06`.
