# Spec 07 — Inference Interface & Optional LLM

## Assignee
Sandro — Interface de Inferência MLOps e LLM Auxiliar Opcional (P7)

## Plain-language goal
A tua missão foca-se na reconstrução realística do projeto, contendo duas vertentes:
Vertente Principal (Must Have): Vais construir um script que recebe um ID de treino (`run_id`). Lendo o `manifest.json` com essa identificação, reconstróis perfeitamente a lógica da equipa (Vectorizador, Mapas de Rótulos, e Modelo) para classificar de forma estanque e isolada novos sumários de PDF da rua. Antes de aplicares a matemática do vector, deves importar a mesma rotina de limpeza do teu colega Gustavo, garantindo que a Inferencia avalia textos padronizados.
Vertente Secundária (Could Have): Opcionalmente, podes adicionar uma ponte de acesso REST para um LLM (ex. DeepSeek) por forma a formatar o parecer em texto humano compreensível.

## Why this matters
Se a nossa plataforma não puder ser invocada isoladamente em inferência, de nada nos serve ter criado modelos poderosos. Este passo assegura também consistência através do carregamento de parâmetros do `manifest` - prevenindo misturas perigosas entre versões da rede e do dicionário NumPy!

## Inputs
- Um argumento de consola indicando a diretoria do teu modelo, via o ID de Run (`run_001`).
- Um fragmento de sumário cru em string, pronto a processar.

## Outputs
- O terminal apresenta a predição estática final para esse sumário.
- (Opcional): Um texto gerado por LLM que descreve a predição, sem valor de parecer jurídico ou prova de explicabilidade.

## Files to create or edit
- `src/inference/predict.py`
- `tests/test_inference.py`

## Step-by-step checklist
- [ ] Confirma o formato e os limites de exportação das API keys na `constitution.md`.
- [ ] No teu ficheiro `predict.py`, constrói a `class InferenceEngine(run_id)`. Lê a estrutura do JSON base.
- [ ] Garante que tens os imports necessários das áreas upstream: o método de limpeza P3 e a instanciação da rede neuronal P5.
- [ ] Cria a pipeline de previsão: (1) Limpeza de string -> (2) Transform NumPy do Vectorizador -> (3) Forward pass Pytorch -> (4) Remapeamento com o ID_To_Label.

## Example
**Inferencia com o Script:** `predict.py run_001 "Acórdão criminal provido..."`
O teu código retorna de imediato:
`[PyTorch Core Predict]: REVOGADA (probabilidade softmax: 0.78)`

Não chamar a esta probabilidade "confiança" sem calibração e validação próprias.

## Tests
Cria testes unitários no ficheiro `tests/test_inference.py`. Podes usar "Fake manifests" simulados num mock folder da tua class de teste para aferir a robustez de imports.

## Definition of Done
- A inferência limpa, transforma e prevê consistentemente, lendo caminhos orientados apenas pelo seu manifesto estático, abstendo-se de codificar caminhos absolutos ("hardcoded") para dicionários de treino.
- Nenhuma submissão do módulo contém senhas, keys ou segredos para serviços.

## What not to do
- Não esqueças a limpeza! Processar texto sujo diretamente na inferência gera incongruências nos resultados em comparação ao treino.
- Foca-te primeiro na Inference Engine offline. A ligação web LLM é um acrescento secundário.

## Dependencies
- O teu módulo consome implicitamente o trabalho dos restantes alunos, desde as funções lógicas do P3 e P4, ao manifesto e artefatos de P5 e P8.

## Git workflow
- Branch: `feature/<JIRA-KEY>-inference-engine`
- Commit: `[<JIRA-KEY>] Implement manifest-driven inference pipeline`

## Commenting expectations
- Avisos expressos a avisar os outros alunos contra o hardcoding de API Keys.
- Comentários orientativos sobre como simular ou instanciar os caminhos da infraestrutura de teste.
