# Especificação 01 — Carregamento de dados PDF e JSON em bruto

## Responsável
Alessandro — Carregamento de dados (P1)

## Jira
`SCRUM-5`

## Objetivo em linguagem simples
A tua missão é carregar os ficheiros das pastas de dados num formato estruturado inicial para entregar à equipa de análise. Vais focar-te em duas rotas: uma que abre ficheiros `.pdf` em bruto e extrai o texto, e outra que lê ficheiros `.json` ainda não estruturados. Ambas as rotas emitem o contrato base `DocumentoBruto`.

## Porque é importante
Gerir corretamente a leitura de dados evita estrangulamentos de memória. Sem funções iteradoras (`yield`), tentar carregar 10 mil PDFs de uma vez pode esgotar a RAM do computador.

## Entradas
Um caminho local para a diretoria alvo: `"dados/amostra/"`.

## Saídas
Objetos da classe `DocumentoBruto(nome_ficheiro, caminho, texto, numero_paginas, origem)` emitidos sequencialmente pelo iterador.

## Ficheiros a criar ou alterar
- `src/dados/carregador_pdf.py`
- `src/dados/carregador_json_bruto.py`
- `tests/test_carregadores.py`

## Lista de trabalho
- [ ] Confirma o formato dos contratos em `constitution.md`.
- [ ] Usa o *Spec Kit IA* para clarificares a utilidade de `yield` ao ler milhares de ficheiros.
- [ ] No `carregador_pdf.py`, usa a biblioteca `pdfplumber`. Extrai o texto total, preenche os campos e devolve `yield DocumentoBruto(...)` onde o campo origem é `"pdf"`.
- [ ] No `carregador_json_bruto.py`, lê ficheiros JSON que apenas contenham texto em bruto e devolve `DocumentoBruto(...)` em que a origem é `"json"`.
- [ ] Garante que qualquer falha (PDF corrompido) cai num bloco `except` seguro, registando o erro sem parar o ciclo `for`.
- [ ] Cria testes em `test_carregadores.py` simulando um PDF válido e um corrompido.

## Exemplo
```python
for documento_bruto in carregar_pdfs("dados/amostra/"):
    print(documento_bruto.origem)  # "pdf" ou "json"
```

## Testes
Comando base: `python -m unittest tests/test_carregadores.py`.

## Critérios de conclusão
- O iterador devolve instâncias de `DocumentoBruto`.
- Anotações de tipo aplicadas e tratamento de exceções funcional.

## O que não fazer
- Não convertas JSONs "estruturados" (que já tenham categorias e sumários prontos) aqui. Isso pertence ao adaptador da Daniela. O teu carregador é focado em texto bruto.
- Não guardes todos os documentos numa lista gigante em memória RAM.

## Dependências
- Vais consumir os esquemas base em `esquemas.py`.
- Entregas o `DocumentoBruto` à Daniela (P2) que vai aplicar as regras de extração.

## Fluxo Git
- Ramo sugerido: `funcionalidade/SCRUM-5-carregadores`
- Commit sugerido: `[SCRUM-5] Adicionar carregadores incrementais de PDF e JSON`

## Comentários esperados
- Docstring a explicar o uso do iterador com `yield` para controlo de memória.
- Comentário explicativo no bloco `try`/`except` que justifique a continuação do ciclo em ficheiros corrompidos.
