# Proposta — SCRUM-40 · Revisão de requisitos de inferência, segurança e serviços externos

**Autor:** Sandro Tarabay (P7)
**Ticket Jira:** SCRUM-40 — [ENTREGA 5] P7 — Validar inferência, segurança e serviços externos
**Escopo:** revisão de `docs/requisitos.md`. Sem alteração de código.

Espelha o comentário submetido no card SCRUM-40. Aplicação em `docs/requisitos.md` pendente do owner do documento (Pedro, P8/Tech Lead).

## Nota

Divergências abaixo estão em `docs/requisitos.md` pós-SCRUM-41 (commit `e916aed`). Por ordem de autoridade do guardrail mestre §2 (constitution → especificações → guias → decisoes.md → esquemas → código), `docs/decisoes.md` e `docs/especificacoes/` têm precedência sobre `docs/requisitos.md`. A correção é sempre no requisitos.md.

## 1. MANTER

- RF11 já usa a mesma composição do treino (descritores+sumário).
- RF12 já separa núcleo obrigatório de LLM opcional.
- RST04/RST05 já existem como secção de Restrição, separada dos RNF.
- Validado em execução real: inferência classifica sem LLM, `distribuicao` estruturada por classe.

## 2. CORRIGIR

| Item | Onde | Problema | Diverge de | Ação |
|---|---|---|---|---|
| RF11 "ou texto bruto" | requisitos.md, RF11 | Ambíguo — reabre a composição de entrada | especificacao_07 (fixa `Acordao.texto_caracteristicas()`) | Fixar via `Acordao.texto_caracteristicas()` |
| RF11 "confiança" | requisitos.md, RF11 | Softmax não calibrada chamada de confiança | ADR-03 (decisoes.md) e guia P7 | Trocar por "distribuição de probabilidades" |
| RF12 sem cláusula | requisitos.md, RF12 | Falta restrição de conteúdo da LLM | ADR-03 | Transportar frase do ADR-03 |
| CA15 | requisitos.md, CA15 | Cita "RNF06" que já não é sobre segurança desde o e916aed | requisitos.md, versão pré-SCRUM-41 | Localizar novo destino da regra de segredos em commits |
| RST04 | requisitos.md, RST04 | Falta JSONs reais/texto_integral/decisao_bruta/artefactos identificáveis | gr4ml_caderno (RNF-GR-06, b2a4f3a) | Alinhar à lista do caderno |

Nota: `src/inferencia/motor_inferencia.py:190-192` e `formatador_saida.py:85-87` também rotulam a saída como "confiança" — reforça que é o requisito (não o código, fora de escopo aqui) que deve alinhar com o ADR-03.

## 3. TEXTO PROPOSTO

**RF11:**
> O sistema deve fornecer um módulo de inferência (`MotorInferencia`) que recebe um novo `Acordao`, constrói a entrada exclusivamente via `Acordao.texto_caracteristicas()` (descritores + sumário, conforme especificacao_07), consulta o modelo por `id_execucao` e devolve a classe prevista com a distribuição de probabilidades (softmax) — nunca apresentada como confiança calibrada (ADR-03) — 100% local.

**Acrescentar ao RF12** (de ADR-03):
> O texto gerado pela LLM deve ser identificado como conteúdo gerado, não constitui parecer jurídico nem explicabilidade validada, e a sua ausência ou falha não pode impedir a devolução da classe prevista.

**RST04** (alinhado a RNF-GR-06 do caderno GR4ML):
> Nomes de pessoas singulares, PDFs brutos, JSONs reais, `texto_integral`, `decisao_bruta`, segredos de justiça, chaves de API e artefactos identificáveis (vocabulário, pesos, manifesto) nunca vão para APIs externas nem para o histórico de commits.

## 4. Critérios de aceitação

| CA | Critério |
|---|---|
| CA13 (existe) | Inferência funciona sem rede/chaves. Validado em execução real. |
| CA17 (novo) | Manifesto nunca mistura artefactos de `id_execucao` diferentes. |
| CA18 (novo) | LLM ausente/timeout não impede devolução de classe+distribuição. |
| CA19 (novo) | Texto da LLM sempre rotulado "gerado, não é parecer jurídico". |

## 5. RNF vs RESTRIÇÃO

| Regra | Onde | Fonte |
|---|---|---|
| Sem LLM obrigatória | Restrição RST05 | Já correto |
| Dados reais não vão para LLM externa | Restrição RST04 | Alinhar com RNF-GR-06 |
| Segredos fora do histórico de commits | Restrição (RST04, a confirmar) | RNF06 pré-SCRUM-41, órfã |
| Macro-F1 > baseline | RNF06 atual | Já correto |

## 6. Dúvidas/Bloqueios

- Destino da regra "chaves fora do histórico de commits" após e916aed.
- RST04 vs RNF-GR-06: divergência intencional ou lapso da consolidação?
- Alterações em requisitos.md fora do domínio P7 — ownership: Pedro (P8).

## Alterações de código

Nenhuma. Saúde do repo validada: 125 testes OK, main.py e inferência end-to-end confirmados.

## Apoio de IA

Sim. Cruzamento de requisitos.md (pré/pós SCRUM-41) contra ADR-03, especificações, guias, caderno GR4ML e código real de src/inferencia/. Redação final revista pelo autor.
