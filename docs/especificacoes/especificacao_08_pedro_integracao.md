# Especificação 08 — Liderança técnica, integração, MLOps e manifesto

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
```json
{
  "id_execucao": "execucao_001",
  "semente": 42,
  "vetorizador": "vetorizador/vocabulario.json",
  "pesos": "modelo/pesos.pth",
  "categorias": "categorias/id_para_categoria.json"
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
