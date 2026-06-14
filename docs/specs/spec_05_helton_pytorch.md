# Especificação: Arquitetura Neuronal (PyTorch)

**Assignee:** Helton (P5 - Arquiteto PyTorch)
**Fase do SDD:** Specify

## 1. Contexto (O Porquê)
O modelo preditivo (PyTorch) é a máquina que descobrirá padrões subjacentes entre as palavras usadas num recurso e a probabilidade dele ser rejeitado ou revogado pelos juízes em Portugal. Nesta 1ª Semana, o módulo da Gleicy (NumPy) ainda não estará 100% pronto. Portanto, o Helton construirá o esqueleto robusto da rede neural recorrendo a "Fake Data" / Tensores gerados aleatoriamente pelo PyTorch. 

## 2. Tarefa Técnica (O Quê)
1. Criar os módulos `src/models/classifier.py` e `src/training/train.py`.
2. Desenhar a classe `class JurisNet(nn.Module)`. Exigência: uma Rede Neuronal Multilayer Perceptron (MLP) limpa, com camadas Lineares (`nn.Linear`), funções de ativação ReLu e um bom regulador como Dropout.
3. Montar as super classes `Dataset` (para herdar a classe abstrata do torch) e usar o `DataLoader` (para gerir *mini-batches*).
4. O loop de treino deve calcular o `CrossEntropyLoss` e permitir otimização via `Adam`.

## 3. Inputs e Outputs
- **Input (MOCK / Fase 1):** Tensores aleatórios simulando a saída da Gleicy. `X_dummy = torch.randn(100, 5000)` e `y_dummy = torch.randint(0, 4, (100,))`.
- **Output:** O modelo treinado guardado em formato PyTorch: `model_weights.pt` e o log de métricas das Epochs (Training Loss e Validation Loss).

## 4. Regras e Restrições SDD
- **Uso Estrito:** Exclusividade da framework PyTorch (`import torch`, `torch.nn`).
- **Reproducibilidade Académica:** Configurar uma Seed global fixa (`torch.manual_seed(42)`) no topo do ficheiro `train.py` para garantir que as apresentações têm resultados replicáveis em bancada.

## 5. Critérios de Aceitação (DoD)
- [ ] O modelo passa no `tests/test_model.py` (O tamanho e shape dos outputs do modelo combinam com o número de classes final definido).
- [ ] O loop de treino consegue iterar perfeitamente os tensores "Dummy Data" sem erros OOM (Out Of Memory) na gráfica (ou CPU).
- [ ] A arquitetura foi discutida de acordo com os requisitos e documentada nos ficheiros base do PyTorch.

---

> **Instrução para Agente de IA:**
> Leia a Constituição em `docs/`.
> Invoque `/speckit.clarify`: Confirme com o Helton o número exato de neurónios na *hidden layer* (camada escondida) e o *batch size* que ele considera ideal para o teste Dummy inicial. Seguidamente, faça o `/speckit.plan`.
