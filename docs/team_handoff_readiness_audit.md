# Auditoria de Prontidão para Entrega à Equipa (Team Handoff Readiness Audit)

**Projeto:** JurisTriage PT
**Disciplina:** Engenharia de Software para IA e Frameworks Profundos
**Auditor:** revisão técnica + Scrum + documental + académica (read-only)
**Data:** 15/06/2026
**Estado do repositório auditado:** após o commit `68a66eb [SCRUM-12] Adotar nomes descritivos em português (#4)`, working tree limpa e sincronizada com `origin/main`.

> **Aviso de método.** Não assumi a documentação como correta — verifiquei ficheiro a ficheiro, corri a suíte de testes e validei links públicos online. Não editei documentos core, não corri código de produção (ainda não existe) e não fiz commits. Este ficheiro e os ficheiros de apoio são os únicos artefactos criados.

> **Nota crítica de contexto.** O pedido de auditoria descreve o repositório **antes** da migração de nomes (caminhos ingleses como `docs/onboarding_individual/`, `docs/specs/`, `create_jira_tasks.py`, `artifacts/`, e o contrato `RawDocument → Acordao → DatasetRow`). Esses caminhos **já não existem**: hoje são `docs/guias_individuais/`, `docs/especificacoes/`, `criar_tarefas_jira.py`, `artefactos/`, e o contrato é `DocumentoBruto → Acordao → RegistoClassificacao`. A auditoria foi feita sobre a estrutura **atual**. O facto de referências externas (e o próprio briefing) já estarem desatualizadas face ao repositório é, em si, um sinal de risco de comunicação (ver Inconsistências).

---

## Resumo executivo

**Veredicto: Quase pronto para entrega (Almost ready).**

A base documental é forte e invulgarmente cuidada para um projeto académico: contratos de dados, uma especificação e um guia por pessoa, política de IA com revisão humana, template de PR, CODEOWNERS, CI (GitHub Actions), `.gitignore` robusto e uma convenção de nomes imposta por teste automático. A suíte de testes passa (**9 testes OK**) e a migração para nomes em português ficou coerente e commitada.

**O que ainda bloqueia uma entrega produtiva imediata:**

1. **`src/dados/esquemas.py` não existe.** É o único artefacto de que **todos** dependem (P1 emite `DocumentoBruto`, P3 consome `Acordao`, P4 consome `RegistoClassificacao`). Está atribuído em copropriedade (P2+P8), mas não está materializado nem há mandato explícito de "fazer primeiro". Sem ele, os mocks de cada pessoa divergem e a integração falha. **(Bloqueante.)**
2. **Contradição de entrada da inferência.** O modelo treina com `descritores + sumario` (constituição §5, RF04), mas a inferência recebe **só o `sumario`** (RF11, `especificacao_07`, guia do Sandro). Isto produz desalinhamento de features entre treino e inferência. **(Bloqueante para o contrato P4↔P7.)**
3. **O mapa "expressão jurídica → classe" precisa de aprovação do Pedro** antes de o Gustavo (P3) o implementar (a constituição §6 fixa as 5 classes, mas o dicionário em si fica "a rever por Pedro").

Resolvidos estes três pontos (estimativa: poucas horas de trabalho do Pedro + Daniela), o projeto está pronto para 8 colegas de nível iniciante/intermédio começarem em paralelo na 5ª feira.

---

## Avaliação do Pedro como Scrum Master / organizador

**Pontuação: 8 / 10.**

### Pontos fortes (com evidência)
- **Contratos de dados como espinha dorsal** (`constitution.md` §3, `arquitetura.md`): isola responsabilidades e permite trabalho paralelo.
- **Uma especificação + um guia por pessoa**, com entradas/saídas, ficheiros, testes, fluxo Git e fluxo de IA (`docs/especificacoes/`, `docs/guias_individuais/`).
- **Estratégia mock-first explícita** (guias de P5, P6, P7, P8 mandam começar com dados/manifesto falsos): excelente para desbloquear paralelismo.
- **Governança de qualidade real, não decorativa:** `.github/pull_request_template.md` (cobre ticket, IA, validação humana, leakage, segredos), `CODEOWNERS`, workflow `testes-python.yml`, `.gitignore` que protege segredos, dados e artefactos.
- **Convenção de nomes imposta por teste** (`tests/test_configuracao_repositorio.py` valida a §9 da constituição) — raríssimo e muito maduro.
- **Ética e data leakage levados a sério** (`etica.md`, `decisoes.md` ADR-02, `boas_praticas_desenvolvimento.md` §13).
- **Política de IA honesta:** não afirma que o professor autorizou IA; trata a saída da IA como rascunho; exige revisão humana.

### Pontos fracos (com evidência)
- **O artefacto mais crítico (`esquemas.py`) não existe** e os campos dos contratos estão dispersos pelos guias em vez de num só sítio autoritário (ver INC-2). É o calcanhar de Aquiles da organização.
- **Contradição treino/inferência** não detetada (INC-1).
- **Critérios de avaliação académica desapareceram.** A versão anterior (roadmap) mapeava deliverables→peso da nota; os documentos atuais só têm RF/RNF. Para um trabalho avaliado, falta a ligação explícita "o que vale quanto e quem entrega".
- **Requisito do enunciado "comparar ≥2 configurações"** (com curva de perda) não está em `requisitos.md` nem na spec do Helton.
- **Excesso de pontos de entrada documentais com três ordens de leitura diferentes** (INC-5) pode sobrecarregar iniciantes.
- **Relatórios desatualizados** (`relatorio_atualizacao_documentacao_ia.md`, `relatorio_revisao_ficheiros.md`) ainda descrevem estado antigo (nomes ingleses, PR1, convites pendentes, CI por faturação).

### O projeto está sobre-organizado, sub-organizado ou adequado?
**Adequadamente organizado, com leve tendência a sobre-documentação.** O risco não é falta de estrutura — é um iniciante perder-se na quantidade de documentos antes de chegar ao seu guia. Um "quick start de 1 página por pessoa" resolveria.

### Recomendação
Pedro fez um bom trabalho de Scrum Master/Tech Lead. Antes de entregar, deve fechar os 3 bloqueantes do resumo executivo (sobretudo materializar `esquemas.py`) e repor os critérios de avaliação. Com isso, sobe confortavelmente para 9/10.

---

## Scorecard de prontidão

| Área | Nota 0-10 | Estado | Notas |
|---|---:|---|---|
| Estrutura do repositório | 9 | ✅ | `src/` (pastas PT) + `tests/` + `artefactos/` + `notebooks/` + `.github/` alinhados com a arquitetura. |
| Documentação | 8 | ✅ | Completa e coerente após migração; falta rubrica de avaliação. |
| Workflows individuais | 8 | 🟡 | Claros e beginner-friendly; herdam INC-1 e dependem de `esquemas.py`. |
| Alinhamento académico | 7 | 🟡 | Bem coberto, mas faltam pesos de avaliação e "≥2 configurações". |
| Apoio a iniciantes | 8 | 🟡 | Muito bom; 3 ordens de leitura e excesso de docs penalizam. |
| Workflow de IA | 9 | ✅ | SDD, OpenCode, DeepSeek, Spec Kit, revisão humana, chave fora do Git. |
| Dependências | 8 | 🟡 | Coerentes; `PyPDF2` e `tqdm` presentes mas não documentados/usados. |
| Validade dos links | 9 | ✅ | Públicos validados online; privados revistos estaticamente. |
| Organização Scrum | 8 | ✅ | Forte; falta `esquemas.py` e rubrica. |
| **Prontidão para entrega** | **7.5** | 🟡 | **Quase pronto**: 3 bloqueantes pequenos por fechar. |

---

## Revisão de workflow individual

Legenda: cada pessoa pode arrancar **hoje** com mocks; o que muda é o que precisam de ter resolvido para **integrar**.

| Pessoa | Pronto? | Risco principal | Instrução em falta | Melhoria sugerida |
|---|---|---|---|---|
| P1 Alessandro | 🟡 | Depende de `esquemas.py` para emitir `DocumentoBruto` | Stub local de `DocumentoBruto` enquanto P2/P8 não publicam | Mini-amostra de 2 PDFs (1 válido, 1 corrompido) versionada |
| P2 Daniela | 🟡 | **Caminho crítico**: dona (com P8) de `esquemas.py` | Mandato de publicar `esquemas.py` no dia 1; campos completos do `Acordao` | Lista canónica de campos do `Acordao` com tipos |
| P3 Gustavo | 🟡 | Dicionário decisão→classe ainda por aprovar | Mapa inicial aprovado pelo Pedro | Tabela seed de ~20 expressões→classe |
| P4 Gleicy | 🟡 | INC-1 (que texto recebe?) + campos de `RegistoClassificacao` | Composição final do texto (descritores+sumário) | Exemplo de cálculo TF-IDF passo a passo |
| P5 Helton | ✅ | Nenhum (usa tensores dummy) | — | Exemplo de `configuracao_modelo.json` |
| P6 Luciana | ✅ | Nenhum (usa arrays inventados) | — | Exemplo de `metricas.json` preenchido |
| P7 Sandro | 🟡 | INC-1 propaga-se à inferência | Composição do texto = a do treino | `manifesto.exemplo.json` concreto |
| P8 Pedro | 🟡 | **Caminho crítico** com P2 | Materializar `esquemas.py` + `construtor_registos.py` | `executar_fluxo.py` mínimo ponta-a-ponta com mocks |

**Notas por pessoa**

- **Alessandro (P1):** Papel e importância académica claros (camada de ingestão, `yield`, OOM). Entradas/saídas e ficheiros (`src/dados/carregador_pdf.py`, `carregador_json_bruto.py`) claros. Único bloqueio: `esquemas.py`. Tarefa adequada para iniciante.
- **Daniela (P2):** Núcleo do projeto. Guia e spec excelentes (parsing posicional, `None` em campos ausentes, adaptador JSON). É co-dona do contrato — precisa de coordenar e **publicar primeiro**. Tarefa de dificuldade média-alta, bem suportada.
- **Gustavo (P3):** Muito claro (limpeza + normalização para 5 classes). Depende do dicionário aprovado pelo Pedro. Tabela de exemplos já incluída no guia. Adequado.
- **Gleicy (P4):** Forte (TF-IDF só com NumPy, `fit` só no treino). O guia é o único sítio onde os campos de `RegistoClassificacao` aparecem enumerados. Sofre da INC-1 e da INC-3 (`config.json` vs `configuracao.json`). Tarefa desafiante mas bem explicada.
- **Helton (P5):** Totalmente desbloqueado (tensores dummy). Regras corretas: só `state_dict`, sem GPU. Adequado.
- **Luciana (P6):** Totalmente desbloqueada (arrays inventados). Macro-F1 vs baseline bem motivado. Adequado.
- **Sandro (P7):** Bem desenhado (carregar por `id_execucao`/`manifesto.json`, limpeza consistente, sem internet). Bloqueio conceptual: a inferência recebe só sumário (INC-1). Adequado depois de resolver INC-1.
- **Pedro (P8):** Caminho crítico. Tem de materializar contratos, construtor e integração. O guia diz "usa mocks e não centralizes tudo em ti" — bom. Carga elevada; ver se acumular Scrum+Tech Lead+QA+integração não o torna gargalo.

---

## Matriz de cobertura dos requisitos académicos

| Requisito académico | Coberto? | Onde | Risco |
|---|---|---|---|
| Carregamento de dados | ✅ | RF01, `especificacao_01`, guia P1 | — |
| Pré-processamento | ✅ | RF05, `especificacao_03`, guia P3 | — |
| NumPy (real) | ✅ | RF08, ADR-01, `especificacao_04` | — |
| PyTorch | ✅ | RF09, `especificacao_05` | — |
| Treino do modelo | ✅ | `especificacao_05`, guia P5 | — |
| Avaliação + baseline | ✅ | RF10, `especificacao_06` | — |
| Modularização | ✅ | RNF01, `src/` por responsabilidade | — |
| Type hints | ✅ | RNF02, constituição §9/§10, boas práticas | — |
| Testes unittest | ✅ | RNF03, workflow CI, todas as specs | — |
| Requisitos | ✅ | `requisitos.md` | — |
| Arquitetura | ✅ | `arquitetura.md`, `decisoes.md` | — |
| Git / colaboração | ✅ | `fluxo_github_jira.md`, PR template, CODEOWNERS | — |
| Reprodutibilidade | ✅ | RNF04 (semente 42), manifesto | — |
| Ética de dados / RGPD | ✅ | `etica.md`, `visao.md`, `.gitignore` | Link Drive público (ver Stream E) |
| Data leakage explicado | ✅ | ADR-02, constituição §5, boas práticas §13 | — |
| Macro-F1 justificado | ✅ | RNF08, `especificacao_06`, guia P6 | — |
| LLM marcado como opcional | ✅ | RF12, ADR-03, constituição §2 | — |
| **Comparar ≥2 configurações** | ❌ | Ausente em `requisitos.md` e na spec do P5 | Requisito do enunciado (etapa 7) não rastreado |
| **Pesos de avaliação / rubrica** | ❌ | Ausente | Não há mapa deliverable→nota→pessoa |
| **Apresentação final** | 🟡 | Mencionada, sem guião/estrutura | Falta `plano_apresentacao.md` / `guiao_demo.md` |

---

## Relatório de validação de links

| URL | Onde aparece | Estado | Recomendação |
|---|---|---|---|
| `github.com/github/spec-kit @v0.10.2` | README, `instalacao_software.md`, constituição | ✅ Tag existe (release "Spec Kit - 0.10.2", 11/06/2026) | Pin correto; manter. |
| `opencode.ai/install` | `instalacao_software.md` | ✅ Resolve (307 → `raw.githubusercontent.com/anomalyco/opencode/.../install`) | Coerente com o tap Homebrew `anomalyco/tap/opencode`. |
| `anaconda.com/download` | `instalacao_software.md` | ✅ Carrega | Manter. |
| `git-scm.com/download/win` | `instalacao_software.md` | 🟡 Não fetched (revisão estática) | URL oficial e estável; baixo risco. |
| `api.deepseek.com` | `.env.example` | 🟡 Endpoint de API, não navegável | Não validar via browser; correto como base URL. |
| `youtube.com/watch?v=a9eR1xsfvHg` | `instalacao_software.md` | 🟡 Não fetched | Material complementar; verificar manualmente uma vez. |
| `drive.google.com/file/d/1n3...` (dataset) | `.env.example` (`DATASET_URL`) | ⚠️ **Não fetched (privacidade)** | **Risco:** link público para dados jurídicos. Restringir a "qualquer pessoa com link" ou mover para acesso controlado. Ver Inconsistências. |
| `fixola198.atlassian.net` | `.env.example` (`JIRA_BASE_URL`) | 🟡 Privado, não testado | Confirmar acessos dos 8 membros manualmente. |

**Links efetivamente verificados online:** 3 (spec-kit tag, opencode/install, anaconda). Restantes: revisão estática por serem privados, endpoints de API ou de baixo risco.

---

## Relatório de alinhamento de dependências (`requirements.txt`)

| Dependência | Justificada? | Onde é referida | Observação |
|---|---|---|---|
| `python-dotenv==1.0.0` | ✅ | `.env`, instalação | OK. |
| `tqdm==4.66.1` | 🟡 | Não documentada | Barra de progresso plausível para loaders; documentar ou remover. |
| `PyPDF2==3.0.1` | ❌ | Docs só mencionam `pdfplumber` | Provável dependência **não usada**; remover ou justificar. |
| `pdfplumber==0.11.5` | ✅ | `especificacao_01`, guia P1, `inspecionar_pdfs.py` | OK. |
| `numpy>=1.24.0,<2.0` | ✅ | ADR-01, teste de setup | Limite `<2.0` por compatibilidade com scikit-learn 1.3. |
| `torch>=2.0.0` | ✅ | `especificacao_05` | OK. |
| `scikit-learn==1.3.0` | ✅ | ADR-01, `especificacao_06`, boas práticas §10 | **Restrito a métricas** (f1_score); proibido em TF-IDF/split — bem documentado. |
| `requests==2.31.0` | ✅ | LLM opcional (P7) | OK. |

**Riscos:** (1) `PyPDF2` aparenta ser dependência morta; (2) `tqdm` não documentada. Ambos de baixo impacto, mas convém alinhar para a avaliação de "gestão de dependências".

---

## Inconsistências encontradas

| # | Severidade | Ficheiro(s) | Problema | Correção proposta |
|---|---|---|---|---|
| INC-1 | 🔴 Alta | `requisitos.md` (RF04 vs RF11), `especificacao_07`, `guias_individuais/sandro_p7_inferencia.md` | Treino usa `descritores+sumario`; inferência usa só `sumario` → desalinhamento de features | Decidir em grupo; inferência passa a receber a **mesma composição** do treino; atualizar RF11, spec 07 e guia |
| INC-2 | 🔴 Alta | `src/dados/esquemas.py` (inexistente); campos dispersos por guias | Contrato de que todos dependem não existe; campos não centralizados | P2+P8 committam `esquemas.py` (3 dataclasses, campos+tipos) no dia 1 |
| INC-3 | 🟠 Média | `guias_individuais/gleicy_p4_numpy.md` (`vetorizador/config.json`) vs `constitution.md` §4 / `arquitetura.md` (`configuracao.json`) | Nome do ficheiro de config do vetorizador divergente | Uniformizar para `configuracao.json` |
| INC-4 | 🟠 Média | `especificacao_04`/`05` (só treino/teste) | Sem conjunto de validação, mas "≥2 configurações" exige comparação sem contaminar o teste | Decidir: aceitar limitação ou acrescentar split de validação |
| INC-5 | 🟡 Baixa | `README.md`, `guia_iniciantes.md`, `guias_individuais/README.md` | Três ordens de leitura diferentes | Definir uma ordem canónica única |
| INC-6 | 🟡 Baixa | `relatorio_atualizacao_documentacao_ia.md`, `relatorio_revisao_ficheiros.md` | Snapshots antigos (nomes ingleses, PR1, convites/CI/token) | Marcar como históricos com data ou atualizar |
| INC-7 | 🟡 Baixa | Briefing/arquitetura externa vs repo | `DatasetRow`/nomes ingleses referenciados fora do repo já estão desatualizados | Comunicar à equipa a fonte de verdade atual (repo PT) |

**Verificação de "strings suspeitas":** todas as ocorrências de `torch.save(model`, `train_test_split`, `TfidfVectorizer`, `model.pt`, "DeepSeek obrigatório" aparecem em contexto de **proibição/estudo** (o que **não** fazer), e o `.pt` em `inspecionar_pdfs.py` é `csm.org.pt` (falso positivo). **Não há violações reais** — coerente com o facto de ainda não existir código de implementação. Não foram encontradas as strings "6 pessoas" nem "máximo 6".

---

## Itens em falta antes da entrega

### Bloqueante (corrigir antes de entregar)
1. Criar e committar `src/dados/esquemas.py` com `DocumentoBruto`, `Acordao`, `RegistoClassificacao` (campos + tipos). **(INC-2)**
2. Resolver a contradição de entrada da inferência. **(INC-1)**
3. Pedro aprovar o dicionário inicial decisão→classe para o Gustavo.

### Importante mas não bloqueante
4. Repor o mapeamento de **critérios de avaliação** (deliverable → peso → pessoa).
5. Acrescentar o requisito **"comparar ≥2 configurações"** (etapa 7) a `requisitos.md` e à spec do P5.
6. Uniformizar `config.json` → `configuracao.json`. **(INC-3)**
7. Limpar dependências (`PyPDF2`, `tqdm`).
8. Restringir/rever o link público do dataset no Drive (RGPD).
9. Marcar os dois relatórios antigos como históricos.

### Nice to have
10. `esquemas.py` à parte: `manifesto.exemplo.json`, `data/README.md`, `tests/README.md`.
11. Quick start de 1 página por pessoa; ordem de leitura única.
12. `docs/glossario.md` consolidado; `plano_apresentacao.md`; `guiao_demo.md`; `registo_riscos.md`; `AGENTS.md`.

---

## Recomendações de valor acrescentado (priorizadas)

| Prioridade | Item | Valor | Esforço | Antes da entrega? |
|---|---|---|---|---|
| 1 | `src/dados/esquemas.py` (esqueleto dos 3 contratos) | Alto | Pequeno | **Sim** |
| 2 | Resolver INC-1 (inferência = treino) na doc | Alto | Pequeno | **Sim** |
| 3 | `docs/criterios_avaliacao.md` (rubrica→pessoa) | Alto | Pequeno | **Sim** |
| 4 | `artefactos/exemplos/manifesto.exemplo.json` | Alto | Pequeno | Sim |
| 5 | `data/README.md` (onde pôr dados + amostra segura) | Alto | Pequeno | Sim |
| 6 | Uniformizar `config.json`→`configuracao.json` | Médio | Pequeno | Sim |
| 7 | Quick start de 1 página por pessoa | Médio | Médio | Recomendado |
| 8 | `docs/glossario.md` consolidado | Médio | Pequeno | Recomendado |
| 9 | `plano_apresentacao.md` + `guiao_demo.md` | Médio | Médio | Não |
| 10 | `tests/README.md`, `AGENTS.md`, `registo_riscos.md`, issue templates | Baixo-Médio | Pequeno | Não |

---

## Recomendação final

**Quase pronto para entrega (Almost ready for handoff).**

A engenharia de processo está bem acima da média para um trabalho académico e os colegas de nível iniciante/intermédio têm caminho claro do onboarding à implementação. Faltam **três correções pequenas mas decisivas** — materializar `esquemas.py`, resolver a entrada da inferência e aprovar o dicionário de classes — sem as quais o paralelismo prometido pelos mocks colapsa na integração. Fechadas essas, mais a reposição da rubrica de avaliação, o projeto pode ser entregue com confiança.
