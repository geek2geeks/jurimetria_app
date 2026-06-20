# Guia — Daniela (P2: análise, esquemas e adaptação JSON)

## O teu papel em linguagem simples

Tu transformas texto em bruto em informação organizada. O Alessandro entrega texto extraído de PDFs ou ficheiros JSON em bruto; tu identificas onde estão o ECLI, o tribunal, o ano, o relator, os descritores, o sumário e a decisão em bruto.

O teu trabalho cria o contrato central do projeto: `Acordao`.

## O que vais construir

- `src/dados/esquemas.py`, em conjunto com Pedro;
- `src/pre_processamento/analisador_metadados.py`;
- `src/dados/carregador_acordaos_json.py`;
- `tests/test_analisador_metadados.py`.

## Por que isto é importante academicamente

A tua etapa demonstra análise, estruturação de dados, tipagem e separação de responsabilidades. Em engenharia de software, não basta ter dados: é preciso transformar dados brutos em objetos com significado.

Esta etapa também mostra maturidade científica. Se cada colega lesse os JSONs ou PDFs do seu jeito, o projeto quebraria na integração. Ao criar `Acordao`, tu crias uma linguagem comum para toda a equipa.

## O contrato que deves respeitar

Entrada principal:

```python
DocumentoBruto(
    nome_ficheiro="exemplo.pdf",
    caminho="dados/amostra/exemplo.pdf",
    texto="texto em bruto extraído",
    numero_paginas=12,
    origem="pdf"
)
```

Saída principal:

```python
Acordao(
    ecli="ECLI:PT:TRL:2015:...",
    tribunal="TRL",
    ano=2015,
    relator="Nome do Relator",
    numero_documento="...",
    data_acordao="09/07/2015",
    meio_processual="Apelação",
    decisao_bruta="improcedente",
    descritores=["prova pericial", "equidade"],
    sumario="texto do sumário",
    texto_integral="texto completo",
    origem="pdf"
)
```

## O que deves estudar primeiro

1. O que é uma classe de dados.
2. O que é uma expressão regular.
3. O que significa retornar `None`.
4. O que é um analisador.
5. O que é fuga de informação.

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
python -m unittest tests/test_analisador_metadados.py
```

## O que não deves fazer

Não adivinhes valores jurídicos. Não forces uma decisão quando ela não aparece. Não passes `dict` para Gustavo ou Gleicy. Não mistures limpeza de texto pesada nesta etapa; isso é do Gustavo.

## Como explicar na apresentação

Podes dizer:

> Criámos um contrato de dados chamado `Acordao` para isolar a complexidade dos PDFs e dos JSONs. A partir deste ponto, toda a equipa trabalha com a mesma estrutura, independentemente da origem do documento.

## Como usar IA na tua tarefa

Pede primeiro uma explicação dos contratos e das âncoras de análise. Usa apenas excertos sintéticos ou sanitizados. A IA não pode alterar os esquemas sem aprovação tua e do Pedro. Revê o diff, testa campos ausentes e declara o apoio de IA no PR.

## Especificações Técnicas Originais

## Responsável
Daniela — Análise posicional de metadados e adaptação (P2)

## Jira
`SCRUM-6`

## Objetivo em linguagem simples
A tua missão é transformar `DocumentoBruto` num objeto estruturado chamado `Acordao`. Irás colaborar com o responsável técnico para definir as classes em `esquemas.py`, criar expressões regulares para identificar secções do PDF e adaptar JSONs já estruturados.

## Porque é importante
Garante o isolamento do fluxo. Ao converter tudo para a classe `Acordao`, as tarefas seguintes de aprendizagem automática não precisam de saber se os dados vieram de um PDF sujo ou de um JSON perfeitamente extraído. O contrato passa a ser estável e seguro.

## Entradas
- Um objeto nativo: `DocumentoBruto` (da rota do PDF ou JSON em bruto).
- Um caminho de ficheiro `.json` para o adaptador estruturado.

## Saídas
- O objeto central do projeto: `Acordao`.

## Ficheiros a criar ou alterar
- `src/pre_processamento/analisador_metadados.py`
- `src/dados/esquemas.py` (copropriedade com o Pedro)
- `src/dados/carregador_acordaos_json.py`
- `tests/test_analisador_metadados.py`

## Lista de trabalho
- [ ] Lê a nova `constitution.md`.
- [ ] Revê com o P8 o `esquemas.py` (já existe uma versão de referência com os três contratos alinhados ao JSON real). Ajusta campos só por acordo dos dois (constituição §7).
- [ ] Em `analisador_metadados.py`, cria a função `analisar_documento_bruto(documento_bruto: DocumentoBruto) -> Acordao`. Extrai campos como `relator`, `ecli` e `sumario` do texto em bruto.
- [ ] Trata o *JSON estruturado*: Cria o `carregador_acordaos_json.py` para ler ficheiros JSON (que já têm os campos separados) e instanciá-los rapidamente como objetos `Acordao`. Isto vai acelerar o desenvolvimento do resto da equipa.
- [ ] Se uma chave no texto (Ex. *Decisão:*) não aparecer, define explicitamente esse campo como `None`.

## Exemplo
`acordaos = carregar_acordaos_json("amostra_estruturada.json")` devolve uma lista de instâncias de `Acordao`.

## Testes
Cria testes assertivos onde forces `None` em certos campos para garantir que o código não falha (`python -m unittest tests/test_analisador_metadados.py`).

## Critérios de conclusão
- A emissão para os módulos a jusante é estritamente uma instância de `Acordao`.
- Tolerância a erros (campos não encontrados = `None`).

## O que não fazer
- Não passes dicionários soltos (`dict`). Garante que a conversão para objeto ocorre imediatamente.

## Dependências
- Consomes o `DocumentoBruto` do P1. Coordenarás o ficheiro `esquemas.py` com o Pedro (P8).

## Fluxo Git
- Ramo sugerido: `funcionalidade/SCRUM-6-analisador-metadados`
- Commit: `[SCRUM-6] Adicionar análise de metadados e adaptação JSON`

## Comentários esperados
- Docstring obrigatória que explique como funciona o adaptador JSON.
- Comentários justificando as âncoras de pesquisa no texto (por exemplo, porque pesquisamos "Decisão Integral:").