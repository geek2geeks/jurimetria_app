# Spec 05 — PyTorch Model and Training (O Cérebro da Operação)

## Assignee
Helton — Modelo PyTorch e Treino Neural (P5)

## Plain-language goal
A tua fase envolve arquitetar a Rede Neuronal Artificial da vossa IA usando PyTorch. Vais receber as matrizes da Gleicy, passá-las pelos `Dataloaders`, e treinar a rede para prever as probabilidades das 5 decisões (MANTIDA, REVOGADA, etc.). No final, a regra mais importante é exportar corretamente os teus "pesos" para a pasta do MLOps (Artifacts).

## Why this matters
O módulo central de "Deep Learning" ocorre no teu código. Sem exportares de forma isolada os teus parâmetros exatos de construção e pesos, a Inferência de vida real não terá as instruções para carregar a máquina offline.

## Inputs
Matrizes NumPy de Treino (`X_train`, `X_test`, `y_train`) criadas pelo módulo P4.

## Outputs
- O dicionário seguro de pesos da rede: `weights.pth`.
- O manifesto de configuração visual: `model_config.json`. Ambos a ser exportados para a respetiva diretoria do `run` em MLOps.

## Files to create or edit
- `src/models/classifier.py`
- `src/training/train.py`
- `tests/test_pytorch.py`

## Step-by-step checklist
- [ ] Confirma as regras de serialização do Modelo PyTorch na Constituição.
- [ ] Na `JurimetriaMLP(nn.Module)`, define a estrutura com `torch.manual_seed(42)`.
- [ ] No `train.py`, constrói o `Dataloader` e a clássica rotina: forward pass, `loss.backward()`, `optimizer.step()`.
- [ ] SALVAMENTO CORRETO: `torch.save(model.state_dict(), "artifacts/run_XXX/model/weights.pth")`.
- [ ] GUARDA A CONFIGURAÇÃO: Usa a biblioteca json para gravar `model_config.json` detalhando as dimensões para o reconstruir futuramente (ex. input_dim, hidden_dim).

## Example
Output do teu `model_config.json`:
```json
{
  "input_dim": 5000,
  "hidden_dim": 128,
  "output_dim": 5,
  "dropout": 0.2,
  "model_class": "JurimetriaMLP"
}
```

## Tests
Cria `tests/test_pytorch.py`. Podes usar tensores dummy aleatórios (`torch.randn`) para não bloqueares os testes. Prova que a *CrossEntropyLoss* diminui em 2 ou 3 iterações! Comando: `python -m unittest tests/test_pytorch.py`.

## Definition of Done
- A exportação dos artefactos de estado (weights e config) é validada.
- O loss decremental foi comprovado no treino dummy.

## What not to do
- **Não** graves o modelo através de `torch.save(model, 'model.pt')`. Essa técnica grava caminhos diretos no código e quebra incompatibilidades de máquina na hora da importação noutro portátil. Exporta apenas o `state_dict`.

## Dependencies
- Baseias-te no processamento das matrizes P4 e entregas o estado do modelo P5 à Pipeline central que coordena a gravação do `manifest.json`.

## Git workflow
- Branch: `feature/<JIRA-KEY>-pytorch-mlp`
- Commit: `[<JIRA-KEY>] Add PyTorch MLP neural network and state_dict serialization`

## Commenting expectations
- Docstrings a explicar as dimensões de entrada e de saída (logits).
- Breves comentários de apoio às hiper-parametrizações escolhidas.
