# Backlog de Valor Acrescentado

Documento de apoio à auditoria ([team_handoff_readiness_audit.md](team_handoff_readiness_audit.md)). Sugestões para reforçar o projeto sem o complicar. Nada aqui foi aplicado — é uma proposta para o Pedro decidir.

Classificação: **Valor** (Alto/Médio/Baixo) · **Esforço** (Pequeno/Médio/Grande) · **Antes da entrega?**

| # | Item | Valor | Esforço | Antes da entrega? | Notas |
|---|---|---|---|---|---|
| 1 | `src/dados/esquemas.py` (esqueleto dos 3 contratos) | Alto | Pequeno | **Sim** | Destranca toda a cadeia (INC-2). |
| 2 | Resolver INC-1 na documentação (inferência = treino) | Alto | Pequeno | **Sim** | Contrato P4↔P7. |
| 3 | `docs/criterios_avaliacao.md` | Alto | Pequeno | **Sim** | Mapa deliverable→peso→pessoa; estava no roadmap antigo e perdeu-se. |
| 4 | `artefactos/exemplos/manifesto.exemplo.json` | Alto | Pequeno | Sim | Exemplo concreto para P7/P8. |
| 5 | `data/README.md` | Alto | Pequeno | Sim | Onde colocar dados, amostra segura, `DATA_DIR`. |
| 6 | Uniformizar `config.json`→`configuracao.json` | Médio | Pequeno | Sim | INC-3. |
| 7 | Acrescentar "comparar ≥2 configurações" (etapa 7) | Médio | Pequeno | Sim | Requisito do enunciado em falta. |
| 8 | Quick start de 1 página por pessoa | Médio | Médio | Recomendado | Reduz sobrecarga documental para iniciantes. |
| 9 | Ordem de leitura única (corrigir INC-5) | Médio | Pequeno | Recomendado | README, guia_iniciantes e guias_individuais divergem. |
| 10 | `docs/glossario.md` consolidado | Médio | Pequeno | Recomendado | Hoje os glossários estão dispersos. |
| 11 | `tests/README.md` | Médio | Pequeno | Não | Como correr/escrever testes. |
| 12 | `docs/plano_apresentacao.md` | Médio | Médio | Não | Estrutura da apresentação final (5%). |
| 13 | `docs/guiao_demo.md` | Médio | Médio | Não | Roteiro da demo ponta-a-ponta. |
| 14 | `docs/registo_riscos.md` | Médio | Pequeno | Não | Risk register formal. |
| 15 | `AGENTS.md` (raiz) para OpenCode/agentes | Médio | Pequeno | Não | Regras de agente alinhadas com a constituição. |
| 16 | Issue templates (`.github/ISSUE_TEMPLATE/`) | Baixo | Pequeno | Não | Polimento. |
| 17 | Marcar relatórios antigos como históricos | Baixo | Pequeno | Não | INC-6. |
| 18 | Limpar `requirements.txt` (`PyPDF2`, `tqdm`) | Baixo | Pequeno | Não | Higiene de dependências. |

## Sequência recomendada
**Antes da entrega:** 1 → 2 → 3 → 4 → 5 → 6 → 7.
**Primeira semana:** 8 → 9 → 10 → 11.
**Quando houver implementação:** 12 → 13 → 14 → 15 → 16 → 17 → 18.
