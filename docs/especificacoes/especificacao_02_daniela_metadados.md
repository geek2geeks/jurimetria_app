# Especificação 02 — Validação e análise posicional de metadados

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
