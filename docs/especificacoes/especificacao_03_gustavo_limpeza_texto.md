# Especificação 03 — Limpeza de texto e normalização de categorias

## Responsável
Gustavo — Limpeza de texto e normalização de categorias (P3)

## Jira
`SCRUM-7`

## Objetivo em linguagem simples
A tua missão é limpar o texto recebido para que a equipa de aprendizagem automática o possa utilizar corretamente. Recebes um objeto `Acordao`. O sumário pode conter ruído como "Powered By TCPDF" ou formatação irregular. O teu dever é removê-lo e normalizar a decisão em bruto (por exemplo, "julgado totalmente improcedente") numa das cinco categorias fixas: `MANTIDA`, `REVOGADA`, `ANULADA`, `NAO_CONHECIDA` ou `OUTRA`.

## Porque é importante
Sem um bom pré-processamento de texto, a vetorização matemática da equipa vai aprender lixo. Além disso, mapear as dezenas de variantes de "decisões de escrivães" para as 5 categorias fixas é o que torna o problema resolvível para o modelo.

## Entradas
A função recebe uma instância de `Acordao`. Embora a estrutura já venha organizada, o conteúdo textual ainda pode estar em bruto e precisar de limpeza.

## Saídas
Funções que devolvem texto limpo e a categoria normalizada. Vais coordenar-te com o Pedro para garantir que o resultado final é usado na criação de `RegistoClassificacao`.

## Ficheiros a criar ou alterar
- `src/pre_processamento/limpeza_texto.py`
- `tests/test_limpeza_texto.py`

## Lista de trabalho
- [ ] Usa o mapa de expressões **já decidido** em `docs/esquema_json_corpus.md` §5 (ADR-05): regras ordenadas (inadmissibilidade → anulação → manter → revogar → outra), tolerância ao `�`, e `improced` antes de `proced`. Descarta `decisao` vazia ou não reconhecida (não adivinhar).
- [ ] Cria dicionários com os sinónimos (por exemplo negado provimento -> MANTIDA).
- [ ] Escreve funções claras: `limpar_texto(texto: str) -> str` e `normalizar_categoria(decisao_bruta: str) -> str`.
- [ ] Ajuda o Pedro a garantir que a conversão de `Acordao` para `RegistoClassificacao` exclui decisões nulas ou irreconhecíveis.

## Exemplo
**Entrada:** `acordao.decisao_bruta = "julgado totalmente improcedente o rec."`
**Saída da função:** `"MANTIDA"`

## Testes
Comando: `python -m unittest tests/test_limpeza_texto.py`. Cobre casos em que as decisões cruas sejam estranhas.

## Critérios de conclusão
- As funções devolvem texto devidamente preparado para aprendizagem automática, sem ruído conhecido.
- O mapeamento baseia-se num dicionário escalável.

## O que não fazer
- Não alteres o esquema (`esquemas.py`). O teu trabalho é focar a transformação do texto, não reestruturar as classes de dados.

## Dependências
- O teu trabalho consome `Acordao` (P2) e ajuda a alimentar o `RegistoClassificacao` (P8).

## Fluxo Git
- Ramo sugerido: `funcionalidade/SCRUM-7-limpeza-texto`
- Commit: `[SCRUM-7] Adicionar limpeza de texto e normalização de categorias`

## Comentários esperados
- Justifica com comentários breves as regras mais difíceis de mapeamento jurídico (ex: por que "parcialmente provido" mapeia para REVOGADA?).
