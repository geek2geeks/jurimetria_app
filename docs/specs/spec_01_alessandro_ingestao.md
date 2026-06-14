# Spec 01 — Data Loader (Ingestão de Dados PDF e JSON Raw)

## Assignee
Alessandro — Ingestão de dados / Data Loader (P1)

## Jira
`SCRUM-5`

## Plain-language goal
A tua missão é carregar os ficheiros das pastas de dados num formato estruturado inicial para entregar à equipa de parsing. Vais focar-te em duas rotas: uma que abre `.pdf` bruto e extrai a string longa de texto, e outra que lê `.json` caso ele não esteja previamente estruturado. Ambas as rotas emitem o contrato base `RawDocument`.

## Why this matters
Gerir corretamente a leitura de dados evita estrangulamentos de memória. Sem funções iteradoras (`yield`), tentar carregar 10 mil PDFs de uma vez pode esgotar a RAM do computador.

## Inputs
Um caminho local para a diretoria alvo: `"data/sample/"`.

## Outputs
Objetos da classe `RawDocument(filename, path, text, page_count, source)` emitidos de forma sequencial pelo iterador.

## Files to create or edit
- `src/data/pdf_loader.py`
- `src/data/json_raw_loader.py`
- `tests/test_loader.py`

## Step-by-step checklist
- [ ] Confirma o formato dos contratos em `constitution.md`.
- [ ] Usa o *Spec Kit IA* para clarificares a utilidade de `yield` ao ler milhares de ficheiros.
- [ ] No `pdf_loader.py`, usa a biblioteca `pdfplumber`. Extrai o texto total, preenche os campos e devolve `yield RawDocument(...)` onde o campo source é `"pdf"`.
- [ ] No `json_raw_loader.py`, lê JSONs que apenas contenham texto bruto, e devolve `RawDocument(...)` onde o source é `"json"`.
- [ ] Garante que qualquer falha (PDF corrompido) cai num bloco `except` seguro, registando o erro sem parar o ciclo `for`.
- [ ] Cria testes em `test_loader.py` simulando um PDF válido e um corrompido.

## Example
```python
for raw_doc in carregar_pdfs("data/sample/"):
    print(raw_doc.source) # "pdf" ou "json"
```

## Tests
Comando base: `python -m unittest tests/test_loader.py`.

## Definition of Done
- O iterador devolve instâncias de `RawDocument`.
- Type hints aplicados e tratamento de exceções funcional.

## What not to do
- Não convertas JSONs "estruturados" (que já tenham labels e sumários prontos) aqui. Isso pertence ao adaptador da Daniela. O teu loader é focado em texto bruto.
- Não guardes todos os documentos numa lista gigante em memória RAM.

## Dependencies
- Vais consumir os esquemas base em `schemas.py`.
- Entregas o `RawDocument` à Daniela (P2) que vai aplicar as regras de extração.

## Git workflow
- Branch sugerida: `feature/SCRUM-5-loader`
- Commit sugerido: `[SCRUM-5] Add generator loaders for PDF and Raw JSON`

## Commenting expectations
- Docstring a explicar o uso do Iterador (Yield) para controlo de memória.
- Comentário explicativo no bloco Try/Except justificando a continuação do loop em ficheiros corrompidos.
