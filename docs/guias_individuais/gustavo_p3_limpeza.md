# Guia — Gustavo (P3: limpeza de texto e normalização de categorias)

## O teu papel em linguagem simples

Tu preparas o texto para que ele possa ser usado por matemática. Recebes um `Acordao`, limpas ruído textual e transformas a decisão bruta numa classe padronizada, como `MANTIDA` ou `REVOGADA`.

## O que vais construir

- `src/pre_processamento/limpeza_texto.py`;
- `tests/test_limpeza_texto.py`.

As tuas funções principais serão algo como:

```python
def limpar_texto(texto: str) -> str:
    ...

def normalizar_categoria(decisao_bruta: str | None) -> str | None:
    ...
```

## Por que isto é importante academicamente

A disciplina avalia pré-processamento e qualidade de fluxo. Em IA, os modelos não aprendem diretamente a realidade: aprendem padrões nos dados que lhes damos. Se o texto tiver rodapés, contactos do CSM, páginas, símbolos repetidos ou categorias inconsistentes, o modelo aprende ruído.

A tua etapa mostra que aprendizagem automática depende fortemente da qualidade do pré-processamento. Também mostra que problemas reais raramente vêm prontos num CSV limpo.

## O contrato que deves respeitar

Entrada:

```python
Acordao(
    descritores=["prova pericial", "equidade"],
    sumario="Sumário com ruído e rodapés...",
    decisao_bruta="improcedente",
    ...
)
```

Saída esperada das tuas funções:

```python
texto_limpo = "prova pericial equidade sumário limpo"
categoria = "MANTIDA"
```

## O que deves estudar primeiro

1. O que é limpeza de texto.
2. O que são stop-words.
3. O que é uma categoria.
4. O que é normalização.
5. Por que classes demais dificultam o treino.

## Como começar sem saber software

Começa por uma função pequena que remove uma frase fixa, por exemplo `Powered by TCPDF`. Depois adiciona remoção de linhas de rodapé. Só depois trabalha nas regras jurídicas da decisão.

Cria uma tabela simples com exemplos:

| Texto bruto | Classe |
|---|---|
| improcedente | MANTIDA |
| negado provimento | MANTIDA |
| procedente | REVOGADA |
| anulada | ANULADA |

## Teste mínimo esperado

O teu teste deve provar que:

- `Powered by TCPDF` é removido;
- espaços duplicados são normalizados;
- `improcedente` vira `MANTIDA`;
- `concedido provimento` vira `REVOGADA`;
- entrada nula não rebenta o programa.

Comando:

```bash
python -m unittest tests/test_limpeza_texto.py
```

## O que não deves fazer

Não alteres `esquemas.py`. Não uses o campo `Decisão` como parte do texto de entrada do modelo. Não prometas que as heurísticas jurídicas são perfeitas; documenta que são uma primeira aproximação.

## Como explicar na apresentação

Podes dizer:

> A limpeza transforma texto jurídico extraído de PDFs num formato mais estável para vetorização. A normalização da decisão reduz expressões jurídicas variadas para um conjunto controlado de classes, tornando o problema tratável para o modelo.

## Como usar IA na tua tarefa

Pede um plano para regras pequenas e testáveis. Não deixes a IA inventar interpretações jurídicas: o mapa de categorias está decidido e documentado em `docs/esquema_json_corpus.md` §5 (ADR-05); casos ambíguos devem ser descartados ou revistos, nunca adivinhados. Usa exemplos sintéticos, executa os testes e declara o apoio de IA no PR.

## Especificações Técnicas Originais

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