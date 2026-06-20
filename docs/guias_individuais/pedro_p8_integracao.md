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

## Especificações Técnicas Originais

## Responsável
Pedro — responsável técnico, integração, requisitos e MLOps (P8)

## Jira
`SCRUM-12`

## Objetivo em linguagem simples
Como responsável técnico, garantes que os módulos funcionam em conjunto. Trabalhas nos contratos de dados (`esquemas.py` com a Daniela) e constróis o integrador do projeto (`construtor_registos.py`). Este módulo processa instâncias de `Acordao`, aplica a limpeza e cria o conjunto de instâncias de `RegistoClassificacao`. Também manténs o fluxo do GitHub Actions e emites `manifesto.json`.

## Porque é importante
Garante que o repositório é funcional de ponta a ponta. Se os fluxos de conversão quebrassem na estrutura (`Acordao` para `RegistoClassificacao`), nenhum aluno subsequente poderia trabalhar. O manifesto MLOps serve como a "Certidão de Nascimento" do modelo, garantindo o registo seguro das suas componentes (vocabulário, treino e pesos da rede) para a reprodução futura da experiência.

## Entradas
- Os módulos limpos e funcionais do ecossistema.
- Os objetos instanciados do fluxo inicial de `Acordao`.

## Saídas
- As definições lógicas essenciais de `esquemas.py` desenhadas e afinadas.
- O script integrador global: `construtor_registos.py` a exportar instâncias limpas de `RegistoClassificacao`.
- O empacotamento MLOps final (módulo de manifesto) a compilar para a pasta local os dados do `manifesto.json`.

## Ficheiros a criar ou alterar
- `src/dados/esquemas.py` (copropriedade com P2)
- `src/dados/construtor_registos.py`
- `.github/workflows/testes-python.yml`
- `executar_fluxo.py`

## Lista de trabalho
- [ ] Confirma e garante o rastreio rigoroso dos contratos (Carregamento de dados, esquema, etc.) estipulados na `constitution.md`.
- [ ] Estabelece em Python as classes de dados: `DocumentoBruto`, `Acordao` e `RegistoClassificacao`.
- [ ] Desenvolve a base iteradora do construtor. Para cada objeto lido, executa a purificação associada à limpeza da decisão e a emissão final sob a forma unitária orientada ao ML (`RegistoClassificacao`).
- [ ] Prepara o fluxo do GitHub Actions que executa a pasta `tests/` em cada pedido de integração.
- [ ] Quando efetuares as extrações para treino, garante que escreves fisicamente a `semente` base do teu teste, links e resultados estatísticos num objeto e o guardas com o registo de metadados completos em formato JSON na subpasta `execucao_XXX`.

## Exemplo
Modelo do Manifesto que deves guardar em `artefactos/execucao_XXX/manifesto.json`:
O manifesto referencia **todos** os artefactos de que a inferência (P7) precisa para reconstruir o vetorizador e o modelo. Segue o layout de `docs/arquitetura.md` §2:

```json
{
  "id_execucao": "execucao_001",
  "semente": 42,
  "vetorizador": {
    "vocabulario": "vetorizador/vocabulario.json",
    "idf": "vetorizador/idf.npy",
    "configuracao": "vetorizador/configuracao.json"
  },
  "categorias": {
    "categoria_para_id": "categorias/categoria_para_id.json",
    "id_para_categoria": "categorias/id_para_categoria.json"
  },
  "modelo": {
    "pesos": "modelo/pesos.pth",
    "configuracao": "modelo/configuracao_modelo.json"
  },
  "metricas": "metricas.json"
}
```

## Testes
Mantém uma bateria de testes rígida que possa processar rapidamente pequenas amostras no GitHub Actions sem onerar os recursos da equipa. Os testes unitários provam a integridade dos módulos aglomerados.

## Critérios de conclusão
- Esquemas de classes bem formatados e em produção limpa nas etapas do fluxo.
- GitHub Actions ativado e reprodutibilidade preservada nos manifestos gerados.

## O que não fazer
- Mantém o foco no controlo de integridade de fuga de informação. Se notares falhas ou passagem de `Decisão Integral` indevida a jusante do fluxo, intervém junto do grupo.
- Evita aprovar pedidos de integração com código sem os respetivos testes e documentação.

## Dependências
- Assumes um papel de vigilância e coordenação. Afinas com a Daniela os esquemas, monitorizas as filtragens do Gustavo, recebes e atestas os ficheiros do Helton e Gleicy e crias as referências do manifesto usadas futuramente pela inferência.

## Fluxo Git
- Garante a revisão de código na `main` e monitoriza os ramos da equipa.
- Usa `funcionalidade/SCRUM-12-integracao`. Podes validar o teu próprio PR como administrador, documentando os testes, riscos e decisão.

## Comentários esperados
- Nos ficheiros do fluxo (`executar_fluxo.py` e construtores), usa comentários apenas para explicar decisões que não sejam evidentes, como limites de campos nulos e escolha de sementes.