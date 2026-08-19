# Próximos Passos do Projeto — JurisTriage PT

Este documento define a sequência operacional do projeto a partir da Entrega 5. O objetivo é evitar antecipação de trabalho: cada fase só deve ser executada quando chegar a data prevista no calendário da disciplina.

## Regra principal

- Trabalhar apenas na fase ativa.
- Não antecipar tarefas de arquitetura, Git final, treino final ou apresentação.
- Cada responsável deve trabalhar sobretudo no módulo que já conhece.
- Tarefas devem ser pequenas, verificáveis e escritas de forma que um colega com menor experiência técnica consiga executá-las sem depender de conhecer o projeto inteiro.
- Dúvidas devem ser registadas no Jira em vez de serem resolvidas por alterações fora do escopo.

## Fase atual — Entrega 5: Requisitos

Estado: **ATIVA**.

Objetivo do professor: entregar documentação de requisitos contendo requisitos funcionais, requisitos não funcionais, restrições e critérios de aceitação, com escopo e rastreabilidade claros.

### Alessandro — P1 Ingestão

Jira: `SCRUM-33`.

Responsabilidade: validar RF01/RF02, ingestão incremental, comportamento perante PDFs/JSON inválidos e critérios de aceitação da camada de entrada.

Não alterar código nesta fase.

### Daniela — P2 Metadados e contratos

Jira: `SCRUM-34`.

Responsabilidade: validar contratos `DocumentoBruto -> Acordao`, RF03/RF04, campos opcionais, JSON como source of truth e requisitos de dados.

Não redesenhar contratos sem aprovação do Pedro.

### Gustavo — P3 Limpeza e categorias

Jira: `SCRUM-35`.

Responsabilidade: validar RF05/RF06, limpeza, normalização para as cinco classes e tratamento de decisões vazias, não reconhecidas ou ambíguas.

Casos ambíguos não devem receber classe inventada.

### Gleicy — P4 NumPy / TF-IDF

Jira: `SCRUM-36`.

Responsabilidade: validar RF07/RF08, composição do dataset, `fit` do TF-IDF apenas no treino, reproducibilidade, shapes e prevenção de leakage.

Não alterar a pipeline nesta fase.

### Helton — P5 PyTorch

Jira: `SCRUM-37`.

Responsabilidade: validar RF09 e requisitos relativos a `nn.Module`, forward, loss, optimizer, treino, validação, persistência e comparação de pelo menos duas configurações experimentais.

Não corrigir agora inconsistências de implementação; apenas documentá-las como requisitos ou questões a tratar na fase adequada.

### Luciana — P6 Avaliação

Jira: `SCRUM-39`.

Responsabilidade: validar RF10/RNF08, Macro-F1, baseline de classe maioritária e mensurabilidade dos critérios de aceitação.

Não aceitar metas numéricas inventadas sem evidência ou aprovação.

### Sandro — P7 Inferência

Jira: `SCRUM-40`.

Responsabilidade: validar RF11/RF12, inferência com os mesmos artefactos e composição de entrada do treino, operação sem LLM externa e restrições de privacidade.

A LLM externa deve permanecer opcional e nunca ser requisito para a classificação principal.

### Pedro — P8 Integração

Jira: `SCRUM-41`.

Responsabilidade: consolidar RF/RNF/RD/restrições/critérios de aceitação, eliminar duplicações, corrigir classificações incorretas e construir a matriz de rastreabilidade.

Revisões cruzadas recomendadas: Daniela para contratos; Luciana para critérios mensuráveis.

## Gate para fechar a Entrega 5

A fase termina apenas quando:

1. todos os RF têm identificador e texto testável;
2. todos os RNF estão claramente separados de restrições;
3. existem requisitos de dados quando necessários;
4. existem restrições explícitas para leakage, privacidade, corpus e dependências externas;
5. cada requisito importante tem pelo menos um critério de aceitação verificável;
6. existe matriz de rastreabilidade entre objetivo, requisito e critério de aceitação;
7. `docs/requisitos.md` contém a versão consolidada;
8. não existem afirmações de desempenho real baseadas nos dados simulados atuais.

## 21/08/2026 — Entrega 6: Design, Arquitetura e Git

**Não executar antes de 21/08/2026.**

Quando esta fase abrir, criar tickets Jira próprios em vez de reutilizar os da Entrega 5.

Distribuição prevista:

- Alessandro: documentar camada de ingestão, interfaces e erros da entrada.
- Daniela: documentar contratos de dados e fluxo `DocumentoBruto -> Acordao`.
- Gustavo: documentar responsabilidade da limpeza e normalização.
- Gleicy: documentar camada NumPy/TF-IDF e transformação do dataset.
- Helton: documentar arquitetura PyTorch, treino, validação e persistência.
- Luciana: documentar avaliação, baseline, métricas e artefactos de resultados.
- Sandro: documentar inferência, carregamento de artefactos e comportamento offline.
- Pedro: integrar diagrama geral, decisões de arquitetura, responsabilidades dos módulos e fluxo Git.

Nesta fase também deve ser feita a auditoria Git: identidade correta dos autores, branches, PRs, commits por membro, links Jira e README do fluxo de colaboração.

## 29/08/2026 — Consolidação e preparação da entrega final

**Não executar antes de 29/08/2026.**

Objetivo: transformar os componentes já produzidos numa execução end-to-end verificável.

Distribuição prevista:

- Alessandro: validar ingestão real numa amostra controlada.
- Daniela: validar contratos e equivalência PDF/JSON.
- Gustavo: validar limpeza, classes e casos ambíguos.
- Gleicy: fechar pipeline NumPy e separação treino/validação/teste.
- Helton: fechar treino PyTorch e persistência.
- Luciana: executar avaliação final, baseline, Macro-F1, tabelas e gráficos.
- Sandro: validar inferência end-to-end com artefactos da execução final.
- Pedro: integração, testes, README, documentação, QA e gate de release académico.

Problemas técnicos já conhecidos a tratar apenas nesta fase ou na fase adequada:

- ligar `Acordao` real a `RegistoClassificacao`;
- eliminar dependência do gerador de dados simulados no caminho final;
- separar treino, validação e teste;
- integrar Macro-F1 e baseline no fluxo principal;
- rever a experiência A/B para garantir que a descrição corresponde ao modelo realmente executado;
- eliminar caminhos de treino redundantes/TODOs não necessários;
- executar a suite completa de `unittest` num ambiente reproduzível;
- gerar métricas e artefactos finais com dados reais/sanitizados conforme as restrições do projeto.

## 29/08/2026 em diante — Preparação da apresentação

Cada membro prepara uma parte curta relacionada com o trabalho que realmente realizou:

- Pedro: problema, requisitos, arquitetura e conclusão.
- Alessandro: dados e ingestão.
- Daniela: estruturação e contratos.
- Gustavo: pré-processamento e normalização.
- Gleicy: NumPy/TF-IDF.
- Helton: PyTorch e treino.
- Luciana: avaliação e resultados.
- Sandro: inferência e demonstração.

A apresentação final deve ser condensada para o tempo definido pelo professor e deve mostrar contribuições reais, não apenas slides genéricos.

## 12/09/2026 — Apresentação final

Objetivo: demonstrar o sistema e explicar tema, motivação, utilizadores/contexto, requisitos, arquitetura, pipeline de dados, PyTorch, testes, Git, resultados experimentais, demonstração, contribuições, dificuldades e melhorias futuras.

Antes da apresentação, confirmar:

- repositório organizado;
- README executável;
- documentação de requisitos e arquitetura atualizada;
- testes automatizados com evidência;
- modelo treinado ou instruções reproduzíveis de treino;
- resultados experimentais reais devidamente identificados;
- demonstração de inferência funcional;
- contribuições individuais rastreáveis.

## Regras de coordenação

- Pedro atua como integrador e evita que vários colegas editem o mesmo documento central simultaneamente.
- Cada colega pode entregar a proposta no Jira; Pedro consolida quando houver risco de conflitos Git.
- Alterações fora do escopo da fase devem ser registadas como descoberta futura, não implementadas imediatamente.
- Não usar `git add .` sem rever o diff.
- Não versionar corpus real, segredos, `.env`, textos jurídicos identificáveis ou artefactos proibidos.
- Dados jurídicos reais não devem ser enviados para serviços externos de IA.
- A classificação principal deve permanecer independente de LLM externa.

## Pendências administrativas

- Confirmar e guardar evidência da autorização do professor para a equipa de oito pessoas, dado que o `Projeto.pdf` refere um máximo de seis pessoas.
- Rodar/revogar a chave API que apareceu acidentalmente no output de uma ferramenta durante a inspeção do `.env`.
- Manter o PR de normalização de line endings separado do trabalho funcional.

## Princípio de execução

Planeamos o projeto completo, mas executamos uma fase de cada vez. Uma tarefa futura só se torna trabalho ativo quando a data/fase correspondente chegar.