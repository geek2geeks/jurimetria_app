# Spec 03 — Text Cleaner & Label Normalizer (Limpezas)

## Assignee
Gustavo — Text Cleaner and Label Normalizer (P3)

## Plain-language goal
A tua missão é limpar o texto recebido para que a equipa de Machine Learning o possa utilizar corretamente. Recebes o objeto `Acordao`. O Sumário dentro deste objeto pode estar minado de ruído como "Powered By TCPDF" ou formatação estranha. O teu dever é limpar isto e, mais importante, normalizar a decisão solta (e.g., "julgado totalmente improcedente") numa das 5 Classes Matemáticas fixas: MANTIDA, REVOGADA, ANULADA, NAO_CONHECIDA, OUTRA.

## Why this matters
Sem um bom pré-processamento de texto, a vetorização matemática da equipa vai aprender lixo. Além disso, mapear as dezenas de variantes de "decisões de escrivães" para as 5 categorias fixas é o que torna o problema resolvível para o modelo.

## Inputs
A função recebe a dataclass `Acordao`. Nota: Embora a estrutura já venha organizada, o conteúdo de texto ainda pode estar "cru" e precisar de limpeza.

## Outputs
Funções que devolvem strings de texto limpo e a label normalizada. Vais coordenar-te com o Pedro para garantir que o resultado final é injetado na classe limpa `DatasetRow`.

## Files to create or edit
- `src/preprocessing/cleaner.py`
- `tests/test_cleaner.py`

## Step-by-step checklist
- [ ] Confirma as cinco classes e o mapa de expressões aprovado pelo Pedro.
- [ ] Cria dicionários com os sinónimos (e.g. negado provimento -> MANTIDA).
- [ ] Escreve funções claras: `clean_texto(texto: str) -> str` e `normalizar_label(decisao_raw: str) -> str`.
- [ ] Ajuda o Pedro a garantir que a conversão de `Acordao` para `DatasetRow` exclui decisões nulas ou irreconhecíveis.

## Example
**Input:** `acordao.decisao_raw = "julgado totalmente improcedente o rec."`
**Saída da função:** `"MANTIDA"`

## Tests
Comando: `python -m unittest tests/test_cleaner.py`. Cobre casos em que as decisões cruas sejam estranhas.

## Definition of Done
- As tuas funções devolvem strings perfeitamente prontas para ML, sem lixo.
- O mapeamento baseia-se num dicionário escalável.

## What not to do
- Não alteres o esquema (`schemas.py`). O teu trabalho é focar na operação do texto, não em reestruturar as Dataclasses.

## Dependencies
- O teu trabalho consome `Acordao` (P2) e ajuda a alimentar o `DatasetRow` (P8).

## Git workflow
- Branch sugerida: `feature/<JIRA-KEY>-text-cleaner`
- Commit: `[<JIRA-KEY>] Add text cleaner and decision label normalizer`

## Commenting expectations
- Justifica com comentários breves as regras mais difíceis de mapeamento jurídico (ex: por que "parcialmente provido" mapeia para REVOGADA?).
