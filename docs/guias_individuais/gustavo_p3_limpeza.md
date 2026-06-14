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

Pede um plano para regras pequenas e testáveis. Não deixes a IA inventar interpretações jurídicas: o mapa de categorias foi aprovado pelo Pedro e casos ambíguos devem ser revistos. Usa exemplos sintéticos, executa os testes e declara o apoio de IA no PR.
