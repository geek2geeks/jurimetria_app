# Onboarding — Daniela (P2: Parser, Schemas e Adaptação JSON)

## O teu papel em linguagem simples

Tu transformas texto bruto em informação organizada. O Alessandro entrega texto extraído de PDFs ou JSONs crus; tu identificas onde estão o ECLI, o tribunal, o ano, o relator, os descritores, o sumário e a decisão bruta.

O teu trabalho cria o contrato central do projeto: `Acordao`.

## O que vais construir

- `src/data/schemas.py`, em conjunto com Pedro;
- `src/preprocessing/metadata_parser.py`;
- `src/data/json_acordao_loader.py`;
- `tests/test_parser.py`.

## Por que isto é importante academicamente

A tua etapa demonstra parsing, estruturação de dados, tipagem e separação de responsabilidades. Em engenharia de software, não basta ter dados: é preciso transformar dados brutos em objetos com significado.

Esta etapa também mostra maturidade científica. Se cada colega lesse os JSONs ou PDFs do seu jeito, o projeto quebraria na integração. Ao criar `Acordao`, tu crias uma linguagem comum para toda a equipa.

## O contrato que deves respeitar

Entrada principal:

```python
RawDocument(
    filename="exemplo.pdf",
    path="data/sample/exemplo.pdf",
    text="texto bruto extraído",
    page_count=12,
    source="pdf"
)
```

Saída principal:

```python
Acordao(
    ecli="ECLI:PT:TRL:2015:...",
    tribunal="TRL",
    year=2015,
    relator="Nome do Relator",
    numero_documento="...",
    data_acordao="09/07/2015",
    meio_processual="Apelação",
    decisao_raw="improcedente",
    descritores=["prova pericial", "equidade"],
    sumario="texto do sumário",
    full_text="texto completo",
    source="pdf"
)
```

## O que deves estudar primeiro

1. O que é uma dataclass.
2. O que é uma expressão regular.
3. O que significa retornar `None`.
4. O que é um parser.
5. O que é data leakage.

## Como começar sem saber software

Começa por um único PDF. Copia um pequeno trecho de texto para dentro de um teste. Primeiro extrai só o ECLI. Depois extrai o tribunal. Depois o sumário. Não tentes resolver todos os campos no primeiro dia.

Para JSON estruturado, o teu objetivo é adaptar, não reinventar. Se o JSON já tem os campos separados, converte diretamente para `Acordao`.

## Teste mínimo esperado

O teu teste deve provar que:

- um texto normal vira `Acordao`;
- campos ausentes viram `None`;
- JSON estruturado vira `Acordao`;
- nenhum dicionário solto segue para os colegas.

Comando:

```bash
python -m unittest tests/test_parser.py
```

## O que não deves fazer

Não adivinhes valores jurídicos. Não forces uma decisão quando ela não aparece. Não passes `dict` para Gustavo ou Gleicy. Não mistures limpeza de texto pesada nesta etapa; isso é do Gustavo.

## Como explicar na apresentação

Podes dizer:

> Criámos um contrato de dados chamado `Acordao` para isolar a complexidade dos PDFs e dos JSONs. A partir deste ponto, toda a equipa trabalha com a mesma estrutura, independentemente da origem do documento.

## Como usar IA na tua tarefa

Pede primeiro uma explicação dos contratos e das âncoras de parsing. Usa apenas excertos sintéticos ou sanitizados. A IA não pode alterar os schemas sem aprovação tua e do Pedro. Revê o diff, testa campos ausentes e declara o apoio de IA no PR.
