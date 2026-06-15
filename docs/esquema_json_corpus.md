# Schema do JSON do corpus (Source of Truth da extração)

Cada PDF do corpus vem acompanhado de um ficheiro JSON com o **mesmo nome**, na
mesma pasta `TRIBUNAL/ANO/`. Esse JSON foi produzido por um extrator com
`extraction_success = true` e é a **source of truth** da extração.

Consequências para o projeto:

1. **Desbloqueador.** A rota `JSON → carregar_acordaos_json → Acordao`
   ([src/dados/carregador_acordaos_json.py](../src/dados/carregador_acordaos_json.py))
   entrega `Acordao` limpos imediatamente. P3, P4, P5, P6, P7 e P8 não precisam
   de esperar pelo parser posicional de PDF.
2. **Oráculo de validação.** O parser posicional de PDF do P2 deve ser
   **testado contra** o JSON do mesmo documento: o output do parser deve bater
   certo com os campos do JSON. O JSON é o gabarito.

> O corpus real **não é versionado** (constituição §8, `.gitignore`). Os
> exemplos abaixo são ilustrativos/sintéticos.

## 1. Campos do JSON (45, presentes em 100% da amostra)

| Campo JSON | Tipo | → `Acordao` | Uso |
|---|---|---|---|
| `ecli` | str | `ecli` | **Fuga** (contém tribunal) |
| `jurisprudencia_url` | str | `url` | **Fuga** |
| `court_code` | str | `tribunal` | **Fuga** / metadado de análise |
| `year` | int | `ano` | Metadado |
| `relator` | str | `relator` | Metadado |
| `numero_documento` | str | `numero_documento` | Metadado |
| `data_acordao` | str | `data_acordao` | Metadado |
| `meio_processual` | str | `meio_processual` | Metadado (opcionalmente X) |
| `votacao` | str | `votacao` | Metadado |
| `area_tematica` | str | `area_tematica` | Metadado |
| `descritores` | str (sep. `;`) | `descritores: list[str]` | **X (entrada)** |
| `sumario_texto` | str | `sumario` | **X (entrada)** |
| `decisao` | str | `decisao_bruta` | **Alvo Y** (origem do rótulo) / **fuga como X** |
| `decisao_integral_texto` | str \| null | `texto_integral` | **Fuga** (decisão dispositiva) |
| `sumario_exists` | bool | — | Diagnóstico |
| `sumario_page_start` | int | — | Diagnóstico |
| `decisao_integral_exists` | bool | — | Diagnóstico |
| `decisao_integral_page_start` | int \| null | — | Diagnóstico |
| `total_pages` | int | (→ `numero_paginas` no `DocumentoBruto`) | Metadado |
| `file_hash` | str | — | Deduplicação |
| `extraction_success` | bool | `extracao_bem_sucedida` | Qualidade |
| `extraction_method`, `extraction_errors`, `ocr_used`, `ocr_confidence_score` | — | — | Diagnóstico |
| `original_filename`, `case_identifier`, `apenso`, `data`, `recurso`, `votacao`, `tribunal_recurso`, `processo_recurso`, `referencia_processo_recurso`, `nivel_acesso`, `indicacoes_eventuais`, `referencias_internacionais`, `jurisprudencia_nacional`, `legislacao_comunitaria`, `legislacao_estrangeira`, `data_decisao_sumaria`, `pdf_creation_date`, `pdf_modification_date`, `file_size_bytes`, `extraction_timestamp` | str/int | — | Metadados adicionais (não usados no MVP) |

## 2. Características autorizadas (X) vs proibidas (fuga)

- **X (entrada do modelo):** apenas `descritores` + `sumario`, após limpeza (P3).
  A composição canónica está em `Acordao.texto_caracteristicas()` — **fonte
  única** partilhada por treino (P4) e inferência (P7).
- **Proibidas como X** (`esquemas.CAMPOS_FUGA_INFORMACAO`): `ecli`, `url`,
  `tribunal`, `texto_integral`, `decisao_bruta`.

**Nota sobre soft-leakage.** O texto do `sumario` pode mencionar a sigla do
tribunal (ex.: "STJ") ou palavras do desfecho (ex.: "rejeitado"). Isto é
**correlação ao nível do texto**, diferente da fuga determinística do campo
`ecli`/`court_code`. Não a removemos artificialmente, mas declaramo-la como
limitação e é uma das razões para reportar **Macro-F1** e comparar com a
baseline (ADR-02, `etica.md`).

## 3. Encoding (atenção, P1/P3)

Os JSON têm caracteres de substituição **U+FFFD (`�`) gravados nos bytes** — a
extração corrompeu `ç/ã/ó/í` (ex.: `coloca��o`, `senten�a`, `P�blico`). Não é
recuperável a 100%. O carregador lê em utf-8 com recurso a cp1252/latin-1 e
nunca interrompe o lote. A limpeza (P3) deve tolerar/normalizar o `�`.

## 4. Separador de descritores

`descritores` é uma string separada por `;` (100% da amostra). O adaptador
divide por `;`, faz `strip` e descarta vazios.

## 5. Distribuição real de `decisao` e mapa-seed para as 5 classes (P3)

Numa amostra de 1500 documentos: **~9,5% têm `decisao` vazia → descartar do
treino**. Existem ~256 expressões brutas distintas; as mais frequentes:
`provido`, `nega provimento`, `negado provimento`, `negada a revista`,
`confirmada`, `improcedente`, `procedente`, `revogada`, `rejeitado`,
`decidido não tomar conhecimento`, `extinção da instância`.

Mapa-seed proposto (a **confirmar pelo Pedro**, constituição §6). O matching
deve ignorar acentos e tolerar `�`:

| Classe | Stems (substring, sem acentos) |
|---|---|
| `MANTIDA` | `nega provimento`, `negado provimento`, `negada a revista`, `negada`, `nao provido`, `confirmada`, `improcedente`, `indeferi`, `apelacao improcedente` |
| `REVOGADA` | `provido`, `concedida a revista`, `concedida`, `procedente`, `revogada`, `alterada a decis`, `parcialmente procedente`, `provido parcial` |
| `ANULADA` | `anulada`, `nulidade` |
| `NAO_CONHECIDA` | `nao tomar conhecimento`, `nao conhecido`, `rejei`, `rejeitado` |
| `OUTRA` | `extin`, e qualquer expressão reconhecida mas fora das anteriores |
| (vazio) | sem categoria → **descartado** do treino, não é `OUTRA` |

> Cuidado: `procedente` é substring de `improcedente`. A ordem das regras
> importa — testar `improcedente` antes de `procedente` (cobertura no
> `tests/test_limpeza_texto.py` do P3).

## 6. Recomendação de fluxo

```text
JSON (oráculo)  ─┐
                 ├─ carregar_acordaos_json ─► Acordao ─► [P3 limpeza] ─► RegistoClassificacao ─► ...
PDF  ─ parser ───┘            (P2, validado contra o JSON)
```

Arrancar pela rota JSON; afinar o parser de PDF em paralelo, comparando-o com o
JSON do mesmo ficheiro.
