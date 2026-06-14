# Onboarding — Alessandro (P1: Ingestão de Dados)

## O teu papel em linguagem simples

Tu és responsável por abrir os ficheiros do projeto e entregá-los ao resto da equipa num formato seguro. O teu trabalho é o primeiro elo da corrente: se os dados não forem carregados corretamente, ninguém consegue fazer parsing, limpeza, NumPy, PyTorch ou avaliação.

## O que vais construir

Vais criar loaders em `src/data/`:

- `pdf_loader.py` para ler PDFs;
- `json_raw_loader.py` para ler JSONs que contenham texto bruto;
- testes em `tests/test_loader.py`.

A tua saída principal é o contrato `RawDocument`.

## Por que isto é importante academicamente

A disciplina avalia carregamento de dados, modularização, tipagem e testes. A tua parte demonstra que um projeto de IA não começa no modelo: começa na capacidade de ler dados reais de forma controlada. Em engenharia de software, isto chama-se camada de ingestão.

O aspeto mais académico da tua tarefa é mostrar que sabes lidar com escala. O corpus pode ter milhares de PDFs. Se tentares ler tudo de uma vez, o computador pode ficar sem memória. Por isso, vais usar iteradores com `yield`, entregando um documento de cada vez.

## O contrato que deves respeitar

Recebes um caminho local, por exemplo:

```text
data/sample/
```

Deves emitir objetos do tipo:

```python
RawDocument(
    filename="exemplo.pdf",
    path="data/sample/exemplo.pdf",
    text="texto extraído do PDF",
    page_count=12,
    source="pdf"
)
```

## O que deves estudar primeiro

1. O que é um ficheiro PDF.
2. O que é uma função em Python.
3. O que é `yield`.
4. O que é uma dataclass.
5. O que é um teste unitário.

## Como começar sem saber software

Começa pequeno. Não tentes ler 10 mil PDFs. Cria uma pasta com 2 PDFs: um válido e um problemático. O teu objetivo inicial é conseguir imprimir o nome do ficheiro e o número de páginas.

Depois adiciona o texto. Depois adiciona o tratamento de erro.

## Teste mínimo esperado

O teu teste deve provar que:

- um ficheiro válido gera `RawDocument`;
- um ficheiro inválido não para o programa;
- o campo `source` fica corretamente preenchido.

Comando:

```bash
python -m unittest tests/test_loader.py
```

## O que não deves fazer

Não guardes todos os documentos numa lista gigante. Não transformes JSONs estruturados em dicionários soltos. Não alteres o schema central sem falar com Pedro e Daniela.

## Como explicar na apresentação

Podes dizer:

> A ingestão foi desenhada para ser incremental, usando iteradores, para evitar consumo excessivo de memória. Esta camada separa o problema de leitura dos ficheiros do problema de interpretação jurídica dos metadados.

## Como usar IA na tua tarefa

Pede à IA para ler a tua spec e explicar `yield` antes de escrever código. Solicita um plano pequeno e testes com PDFs sintéticos ou mocks. Nunca envies PDFs reais. Revê o diff, executa todos os testes e declara o apoio de IA no PR.
