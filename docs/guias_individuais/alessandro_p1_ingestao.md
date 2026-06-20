# Guia — Alessandro (P1: carregamento de dados)

## O teu papel em linguagem simples

Tu és responsável por abrir os ficheiros do projeto e entregá-los ao resto da equipa num formato seguro. O teu trabalho é o primeiro elo da corrente: se os dados não forem carregados corretamente, ninguém consegue fazer análise, limpeza, NumPy, PyTorch ou avaliação.

## O que vais construir

Vais criar carregadores em `src/dados/`:

- `carregador_pdf.py` para ler PDFs;
- `carregador_json_bruto.py` para ler JSONs que contenham texto bruto;
- testes em `tests/test_carregadores.py`.

A tua saída principal é o contrato `DocumentoBruto`.

## Por que isto é importante academicamente

A disciplina avalia carregamento de dados, modularização, tipagem e testes. A tua parte demonstra que um projeto de IA não começa no modelo: começa na capacidade de ler dados reais de forma controlada. Em engenharia de software, isto chama-se camada de ingestão.

O aspeto mais académico da tua tarefa é mostrar que sabes lidar com escala. O corpus pode ter milhares de PDFs. Se tentares ler tudo de uma vez, o computador pode ficar sem memória. Por isso, vais usar iteradores com `yield`, entregando um documento de cada vez.

## O contrato que deves respeitar

Recebes um caminho local, por exemplo:

```text
dados/amostra/
```

Deves emitir objetos do tipo:

```python
DocumentoBruto(
    nome_ficheiro="exemplo.pdf",
    caminho="dados/amostra/exemplo.pdf",
    texto="texto extraído do PDF",
    numero_paginas=12,
    origem="pdf"
)
```

## O que deves estudar primeiro

1. O que é um ficheiro PDF.
2. O que é uma função em Python.
3. O que é `yield`.
4. O que é uma classe de dados.
5. O que é um teste unitário.

## Como começar sem saber software

Começa pequeno. Não tentes ler 10 mil PDFs. Cria uma pasta com 2 PDFs: um válido e um problemático. O teu objetivo inicial é conseguir imprimir o nome do ficheiro e o número de páginas.

Depois adiciona o texto. Depois adiciona o tratamento de erro.

## Teste mínimo esperado

O teu teste deve provar que:

- um ficheiro válido gera `DocumentoBruto`;
- um ficheiro inválido não para o programa;
- o campo `origem` fica corretamente preenchido.

Comando:

```bash
python -m unittest tests/test_carregadores.py
```

## O que não deves fazer

Não guardes todos os documentos numa lista gigante. Não transformes ficheiros JSON estruturados em dicionários soltos. Não alteres o esquema central sem falar com Pedro e Daniela.

## Como explicar na apresentação

Podes dizer:

> A ingestão foi desenhada para ser incremental, usando iteradores, para evitar consumo excessivo de memória. Esta camada separa o problema de leitura dos ficheiros do problema de interpretação jurídica dos metadados.

## Como usar IA na tua tarefa

Pede à IA para ler a tua especificação e explicar `yield` antes de escrever código. Solicita um plano pequeno e testes com PDFs sintéticos ou simulados. Nunca envies PDFs reais. Revê o diff, executa todos os testes e declara o apoio de IA no PR.

## Especificações Técnicas Originais

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

## Especificações Técnicas Originais

## Responsável
Sandro — Motor de inferência e modelo de linguagem opcional (P7)

## Jira
`SCRUM-11`

## Objetivo em linguagem simples
A tua missão foca-se na reconstrução realística do projeto, contendo duas vertentes:
Vertente principal: vais construir um programa que recebe um identificador de execução (`id_execucao`). A partir de `manifesto.json`, reconstrói o vetorizador, o mapa de categorias e o modelo para classificar novos sumários. Antes da vetorização, deve usar a mesma rotina de limpeza do Gustavo, garantindo que a inferência avalia texto normalizado.
Vertente secundária: opcionalmente, podes adicionar uma ligação REST a um modelo de linguagem, como o DeepSeek, para apresentar o resultado em texto legível.

## Porque é importante
Se a nossa plataforma não puder ser invocada isoladamente em inferência, de nada nos serve ter criado modelos poderosos. Este passo assegura também consistência através do carregamento de parâmetros do `manifesto` - prevenindo misturas perigosas entre versões da rede e do dicionário NumPy!

## Entradas
- Um argumento de linha de comandos que indica a diretoria do modelo por meio do identificador da execução (`execucao_001`).
- O texto do novo documento na **mesma composição do treino**: descritores + sumário (ver `Acordao.texto_caracteristicas()`). Numa demonstração simples aceita-se só o sumário, mas avisa que omitir os descritores degrada as características face ao treino.

## Saídas
- O terminal apresenta a previsão final para esse sumário.
- Opcionalmente, um texto gerado pelo modelo de linguagem descreve a previsão, sem valor de parecer jurídico nem de explicação validada.

## Ficheiros a criar ou alterar
- `src/inferencia/motor_inferencia.py`
- `tests/test_motor_inferencia.py`

## Lista de trabalho
- [ ] Confirma na `constitution.md` os limites aplicáveis a chaves de API.
- [ ] No ficheiro `motor_inferencia.py`, constrói a classe `MotorInferencia` que recebe `id_execucao` e lê o manifesto.
- [ ] Importa apenas as dependências necessárias dos módulos anteriores: limpeza de texto P3, vetorizador P4 e rede neuronal P5.
- [ ] Cria o fluxo de previsão: limpeza de texto -> `transform` do vetorizador NumPy -> passagem direta em PyTorch -> remapeamento com `id_para_categoria`.

## Exemplo
**Inferência com o programa:** `motor_inferencia.py execucao_001 "Acórdão criminal provido..."`
O teu código retorna de imediato:
`Previsão: REVOGADA (probabilidade softmax: 0,78)`

Não chamar a esta probabilidade "confiança" sem calibração e validação próprias.

## Testes
Cria testes unitários em `tests/test_motor_inferencia.py`. Podes usar manifestos e pastas temporárias para testar o carregamento de artefactos.

## Critérios de conclusão
- A inferência limpa, transforma e prevê consistentemente, lendo caminhos orientados apenas pelo seu manifesto estático, abstendo-se de codificar caminhos absolutos ("fixos no código") para dicionários de treino.
- Nenhuma submissão do módulo contém senhas, chaves ou segredos para serviços.

## O que não fazer
- Não esqueças a limpeza! Processar texto sujo diretamente na inferência gera incongruências nos resultados em comparação ao treino.
- Foca-te primeiro no motor de inferência local. A ligação remota ao modelo de linguagem é um acrescento secundário.

## Dependências
- O teu módulo consome implicitamente o trabalho dos restantes alunos, desde as funções lógicas do P3 e P4, ao manifesto e artefactos de P5 e P8.

## Fluxo Git
- Ramo: `funcionalidade/SCRUM-11-motor-inferencia`
- Commit: `[SCRUM-11] Adicionar motor de inferência orientado pelo manifesto`

## Comentários esperados
- Avisos explícitos contra chaves de API fixas no código.
- Comentários orientativos sobre como simular ou instanciar os caminhos da infraestrutura de teste.