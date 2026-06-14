# Especificação: Baseline e ML Ops

**Assignee:** Luciana (P6 - Especialista MLOps - Parte 1)
**Fase do SDD:** Specify

## 1. Contexto (O Porquê)
Na universidade, e no mercado de trabalho, de nada serve treinar um modelo de PyTorch se ele adivinhar resultados de forma ingénua. Se 80% das sentenças em Portugal forem "MANTIDA", uma rede neuronal defeituosa que preveja sempre "MANTIDA" terá um Accuracy brilhante de 80%, mas 0 Inteligência Artificial real. A Luciana será responsável pelo ceticismo metodológico, a Baseline e o pipeline de Métricas Definitivo do PyTorch.

## 2. Tarefa Técnica (O Quê)
1. Construir `src/evaluation/metrics.py`.
2. Desenhar a Baseline Cega (`MajorityClassBaseline`): uma classe/script que observa o vetor de treino `y_train` (criado de forma "Dummy Data" na Semana 1), descobre a classe que mais se repete e prevê **apenas e sempre essa classe** para o Test Set.
3. Desenvolver o motor métrico: Calcular e imprimir as métricas `Accuracy` e `Macro-F1 Score`. A F1 Macro é o verdadeiro critério de sucesso porque penaliza algoritmos cegos num contexto de classes desequilibradas.

## 3. Inputs e Outputs
- **Input (MOCK / Fase 1):** O vetor `y_true` de Teste (Dummy) e o `y_pred` de Teste (que o Helton ou a Baseline produzirão). Ambos `np.ndarray` ou Tensores.
- **Output:** Um dicionário ou dicionário impresso (`stdout`) de performance. `{"Accuracy": 0.80, "Macro_F1": 0.25}`. E guardar os plots em `docs/metrics_report.md`.

## 4. Regras e Restrições SDD
- **Transparência Absoluta:** O código tem a autorização explícita para usar as métricas do pacote `scikit-learn.metrics` (pois o numpy foi restrito apenas à feature engineering da Gleicy), usando `f1_score(average="macro")`.

## 5. Critérios de Aceitação (DoD)
- [ ] Ao enviar o Dummy Data desequilibrado para a Baseline, a métrica Macro-F1 deve demonstrar estar drasticamente inferior à Accuracy Geral (confirmando o perigo estatístico).
- [ ] Módulo com `unittests` em `tests/test_evaluation.py`.

---

> **Instrução para Agente de IA:**
> Leia a Constituição em `docs/`.
> Invoque `/speckit.plan`: Planeie o desenho arquitetural do avaliador (`evaluator`), detalhando como irá ler o ficheiro `.pt` do PyTorch que o Helton gravar no disco e passá-lo pelas métricas de Teste de forma modularizada sem estourar o GPU.
