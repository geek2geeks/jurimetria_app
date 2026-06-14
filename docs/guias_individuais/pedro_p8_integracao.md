# Guia — Pedro (P8: integração, responsabilidade técnica, qualidade e MLOps)

## O teu papel em linguagem simples

Tu és responsável por garantir que as peças de todos encaixam. Não significa fazer o trabalho dos colegas; significa definir contratos, proteger a arquitetura, rever pedidos de integração, organizar o Jira e garantir que o projeto funciona de ponta a ponta.

## O que vais construir ou coordenar

- `src/dados/esquemas.py`, em conjunto com Daniela;
- `src/dados/construtor_registos.py`;
- `.github/workflows/testes-python.yml`;
- `executar_fluxo.py`;
- `artefactos/execucao_XXX/manifesto.json`;
- documentação de requisitos, arquitetura, decisões e guia de integração.

## Por que isto é importante academicamente

A disciplina não avalia apenas modelo. Ela avalia engenharia de software aplicada a IA. A tua função é tornar visível essa engenharia: modularização, rastreabilidade, testes, documentação, Git e reprodutibilidade.

Num projeto de grupo, a integração é frequentemente onde tudo falha. O teu papel demonstra capacidade de coordenação técnica, validação de interfaces e controlo de qualidade.

## O contrato que deves proteger

Fluxo central:

```text
DocumentoBruto -> Acordao -> RegistoClassificacao -> matrizes NumPy -> modelo PyTorch -> métricas -> manifesto -> inferência
```

O `manifesto.json` deve ligar todos os artefactos de uma execução:

```text
id_execucao: execucao_001
semente: 42
vetorizador: vetorizador/vocabulario.json
idf: vetorizador/idf.npy
categorias: categorias/id_para_categoria.json
configuracao_modelo: modelo/configuracao_modelo.json
pesos: modelo/pesos.pth
metricas: metricas.json
```

## O que deves estudar primeiro

1. O que é integração.
2. O que é integração contínua.
3. O que é contrato de dados.
4. O que é manifesto.
5. O que é revisão de código.
6. O que é rastreabilidade.
7. Como impedir fuga de informação.

## Como começar sem saber tudo

Primeiro garante as pastas e os contratos. Depois cria um `construtor_registos.py` mínimo que recebe duas instâncias simuladas de `Acordao` e devolve duas instâncias de `RegistoClassificacao`. Em seguida, cria o fluxo do GitHub Actions para executar `python -m unittest`.

Não esperes o projeto inteiro para criar a integração. Usa simulados e dados pequenos.

## Teste mínimo esperado

Deves garantir que:

- `esquemas.py` pode ser importado por todos;
- `construtor_registos.py` remove documentos sem categoria válida;
- o fluxo automático executa `python -m unittest`;
- `manifesto.json` aponta para ficheiros relativos;
- pedidos de integração que quebram testes não entram na `main`.

## O que não deves fazer

Não centralizes tudo em ti. Não deixes colegas passar dicionários soltos. Não aproves `torch.save(model)`. Não deixes `fit` do TF-IDF acontecer fora do treino. Não permitas dados reais identificáveis no repositório.

## Como explicar na apresentação

Podes dizer:

> A integração foi desenhada com contratos de dados e manifestos de execução. Isto garante que cada módulo pode ser desenvolvido por uma pessoa diferente, mas o sistema continua reprodutível, testável e coerente de ponta a ponta.

## Como usar IA na tua tarefa

Usa IA para comparar contratos, gerar listas de verificação e encontrar riscos entre módulos. Revê cada mudança arquitetural e protege dados e segredos. Podes validar os teus próprios pedidos de integração como administrador, mas tens de documentar os testes, riscos e decisão.
