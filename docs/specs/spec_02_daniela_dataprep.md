# Spec 02 — Positional Metadata Parser (Data Validation e Mapeamento)

## Assignee
Daniela — Parsing posicional de metadados e Adaptação (P2)

## Plain-language goal
A tua missão é transformar o texto bruto (`RawDocument`) num objeto bem definido e estruturado chamado `Acordao`. Irás colaborar com o Tech Lead para definir as classes em `schemas.py`, criar as expressões regulares para identificar secções do PDF, e criar um adaptador (`json_acordao_loader.py`) capaz de converter diretamente JSONs já estruturados (bypass) no formato `Acordao`.

## Why this matters
Garante o isolamento do pipeline. Ao converter tudo para a classe `Acordao`, as tarefas seguintes de Machine Learning não precisam de saber se os dados vieram de um PDF sujo ou de um JSON perfeitamente extraído. O contrato passa a ser estável e seguro.

## Inputs
- Um objeto nativo: `RawDocument` (da rota do PDF ou JSON cru).
- Um caminho de ficheiro `.json` para o adaptador estruturado.

## Outputs
- O objeto central do projeto: `Acordao`.

## Files to create or edit
- `src/preprocessing/metadata_parser.py`
- `src/data/schemas.py` (Copropriedade com o Pedro)
- `src/data/json_acordao_loader.py`
- `tests/test_parser.py`

## Step-by-step checklist
- [ ] Lê a nova `constitution.md`.
- [ ] Define em conjunto com o P8 o `schemas.py`, contendo as classes `@dataclass RawDocument`, `Acordao` e `DatasetRow`.
- [ ] Em `metadata_parser.py`, cria a função `parse_raw_document(doc: RawDocument) -> Acordao`. Extrai os campos como `relator`, `ecli` e `sumario` do texto bruto.
- [ ] Trata o *JSON estruturado*: Cria o `json_acordao_loader.py` para ler ficheiros JSON (que já têm os campos separados) e instanciá-los rapidamente como objetos `Acordao`. Isto vai acelerar o desenvolvimento do resto da equipa.
- [ ] Se uma chave no texto (Ex. *Decisão:*) não aparecer, define explicitamente esse campo como `None`.

## Example
`adapter = load_acordaos_from_json("amostra_estruturada.json")` -> Devolve uma lista de instâncias `Acordao`.

## Tests
Cria testes assertivos onde forces `None` em certos campos para garantir que o código não falha (`python -m unittest tests/test_parser.py`).

## Definition of Done
- A emissão para os módulos a jusante é estritamente a dataclass `Acordao`.
- Tolerância a erros (campos não encontrados = `None`).

## What not to do
- Não passes dicionários soltos (`dict`). Garante que a conversão para objeto ocorre imediatamente.

## Dependencies
- Consomes o `RawDocument` do P1. Coordenarás o ficheiro `schemas.py` com o Pedro (P8).

## Git workflow
- Branch sugerida: `feature/<JIRA-KEY>-metadata-parser`
- Commit: `[<JIRA-KEY>] Implement Parser and Struct JSON Adapter`

## Commenting expectations
- Docstring obrigatória explicando como o adaptador JSON funciona.
- Comentários justificando as âncoras de pesquisa no texto (e.g., porque pesquisamos "Decisão Integral:").
