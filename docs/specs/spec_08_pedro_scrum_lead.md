# Especificação: Liderança Técnica, QA, CI/CD e Requisitos

**Assignee:** Pedro (P7/P8 - Scrum Master e Tech Lead)
**Fase do SDD:** Specify

## 1. Contexto (O Porquê)
Enquanto a restante equipa avança na execução das trincheiras de código, é vital o papel de liderança para assegurar a visão geral e a aprovação global do projeto nos itens teóricos da grelha de avaliação (Design, Arquitetura, Requisitos). O Pedro é o guarda de controlo do repositório de forma a garantir que os pontos académicos (como Git, Tipagem e Qualidade de Código - equivalendo a ~45% do peso da nota na primeira fase) sejam cumpridos por todos sem exceção.

## 2. Tarefa Técnica (O Quê)
1. **QA e GitHub Actions:** Criar um *workflow* no repositório GitHub (`.github/workflows/python-tests.yml`). Este script deve obrigar o servidor do GitHub a correr o `python -m unittest` toda a vez que alguém tentar fazer merge para a `main`. Se os testes falharem, o Pull Request fica bloqueado.
2. **Linting de Tipos:** Configurar o `flake8` ou `mypy` no projeto para garantir e cobrar as Type Hints que a universidade exige.
3. **Gestão dos Specs:** O Pedro distribuirá através do sistema de Tickets do *Jira* os restantes 7 Documentos de Especificações (*Specifys* gerados) por cada um dos Assignees.
4. **Requisitos Teóricos:** Avançar a redação académica dos Requisitos da Entrega 5 (no ficheiro `docs/requirements.md`) documentando Formalmente as Restrições, Regras de Negócio, ADRs (Decision Records) e Estruturas da Base de Dados.

## 3. Inputs e Outputs
- **Input:** Relatórios de PR dos colegas na plataforma e atualizações teóricas.
- **Output:** Repositório estável (Verde nas *GitHub Actions*) e com o documento `requirements.md` formatado nos preceitos rígidos da Engenharia de Software ISO.

## 4. Regras e Restrições SDD
- **Tratamento de Exceção:** A conta do Lead é a única com estatuto administrativo na organização, sendo o único membro autorizado a sobrepor eventuais conflitos (Merge Conflicts pesados) de forma manual.
- Nenhum membro tem permissão direta à `main`.

## 5. Critérios de Aceitação (DoD)
- [ ] O repositório tem as Pull Requests blindadas pela obrigatoriedade de sucesso do CI/CD (Testes e Type Checks).
- [ ] Os 7 Specs estão registados nos *epics* corretos do Jira.
- [ ] Documento visionário escrito (`vision.md`) com a declaração ética de uso da Jurisprudência no que toca à Lei de Proteção de Dados (RGPD).

---

> **Instrução para Agente de IA:**
> Como companheiro IA do Scrum Master, foque-se inteiramente em não escrever código utilitário de MLOps. Confirme em contexto o ficheiro da Constituição (`constitution.md`).
> Realize a Fase `/speckit.plan`: Desenhe como deve ser estruturado o ficheiro `.yaml` para o servidor Cloud do GitHub proteger eficientemente a árvore de projetos do Jira.
