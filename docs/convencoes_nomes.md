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
