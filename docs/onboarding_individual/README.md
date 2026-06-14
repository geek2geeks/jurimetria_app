# Onboarding Individual — JurisTriage PT

Este diretório contém um guia específico para cada membro da equipa. A ideia é que cada pessoa perceba, mesmo sem experiência prévia em software, três coisas:

1. qual é a sua responsabilidade;
2. por que essa etapa existe academicamente;
3. como começar sem bloquear os colegas.

## Ordem de leitura obrigatória

1. `constitution.md`
2. `docs/onboarding_for_beginners.md`
3. a tua spec em `docs/specs/`
4. o teu onboarding individual neste diretório
5. `docs/software_setup.md`
6. `docs/github_jira_workflow.md`
7. `docs/ai_development_workflow.md`, caso uses IA

## Guias individuais

| Pessoa | Papel | Guia |
|---|---|---|
| Alessandro | P1 — Ingestão de dados | [alessandro_p1_ingestao.md](alessandro_p1_ingestao.md) |
| Daniela | P2 — Parser e schemas | [daniela_p2_parser.md](daniela_p2_parser.md) |
| Gustavo | P3 — Limpeza e labels | [gustavo_p3_limpeza.md](gustavo_p3_limpeza.md) |
| Gleicy | P4 — NumPy e vetorização | [gleicy_p4_numpy.md](gleicy_p4_numpy.md) |
| Helton | P5 — PyTorch e treino | [helton_p5_pytorch.md](helton_p5_pytorch.md) |
| Luciana | P6 — Métricas e baseline | [luciana_p6_metricas.md](luciana_p6_metricas.md) |
| Sandro | P7 — Inferência | [sandro_p7_inferencia.md](sandro_p7_inferencia.md) |
| Pedro | P8 — Integração e liderança técnica | [pedro_p8_integracao.md](pedro_p8_integracao.md) |

## Regra comum para todos

Ninguém precisa saber tudo. Cada etapa foi desenhada para ter uma fronteira clara de entrada e saída. A qualidade académica do projeto vem justamente dessa separação: cada pessoa entrega uma parte pequena, testável e documentada de um sistema maior.

## Fluxo comum

1. Recebe o ticket Jira.
2. Cria uma branch com a chave real do ticket.
3. Implementa apenas o escopo da spec.
4. Executa todos os testes.
5. Abre um Pull Request.
6. Declara se usaste IA.
7. Pede revisão ao Pedro.

Quando Pedro for o autor, pode validar o próprio PR como administrador, documentando testes e decisão.
