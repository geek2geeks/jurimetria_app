# Especificação 05 — Modelo e treino determinístico em PyTorch

## Responsável
Helton — Modelo PyTorch e treino neuronal (P5)

## Jira
`SCRUM-9`

## Objetivo em linguagem simples
A tua fase envolve construir a rede neuronal em PyTorch. Vais receber as matrizes da Gleicy, passá-las por objetos `DataLoader` e treinar a rede para prever as probabilidades das cinco decisões. No final, deves exportar corretamente os pesos para a pasta de artefactos.

## Porque é importante
O módulo de aprendizagem profunda ocorre no teu código. Sem exportares separadamente a configuração e os pesos, o motor de inferência não terá informação suficiente para reconstruir o modelo.

## Entradas
Matrizes NumPy de Treino (`caracteristicas_treino`, `caracteristicas_teste`, `categorias_treino`) criadas pelo módulo P4.

## Saídas
- O dicionário seguro de pesos da rede: `pesos.pth`.
- A configuração do modelo: `configuracao_modelo.json`. Ambos devem ser exportados para a diretoria da respetiva execução.

## Ficheiros a criar ou alterar
- `src/modelos/rede_neuronal.py`
- `src/treino/treinar_modelo.py`
- `tests/test_rede_neuronal.py`

## Lista de trabalho
- [ ] Confirma as regras de serialização do Modelo PyTorch na Constituição.
- [ ] Na `RedeNeuronalClassificacao(nn.Module)`, define a estrutura e usa `torch.manual_seed(semente)`.
- [ ] No `treinar_modelo.py`, constrói o `DataLoader` e a rotina de treino: passagem direta, `perda.backward()` e `otimizador.step()`.
- [ ] SALVAMENTO CORRETO: `torch.save(model.state_dict(), "artefactos/execucao_XXX/modelo/pesos.pth")`.
- [ ] Guarda a configuração com a biblioteca `json` em `configuracao_modelo.json`, detalhando as dimensões necessárias para reconstruir o modelo.
- [ ] **Comparar pelo menos duas configurações** (ex.: nº de camadas, ativação ou batch size) e registar a curva de perda de cada uma (requisito do enunciado, RF09).

## Exemplo
Conteúdo de `configuracao_modelo.json`:
```json
{
  "numero_entradas": 5000,
  "numero_ocultas": 128,
  "numero_saidas": 5,
  "dropout": 0.2,
  "classe_modelo": "RedeNeuronalClassificacao"
}
```

## Testes
Cria `tests/test_rede_neuronal.py`. Podes usar tensores aleatórios simulados (`torch.randn`) com uma semente explícita. Demonstra que a `CrossEntropyLoss` diminui em duas ou três iterações. Comando: `python -m unittest tests/test_rede_neuronal.py`.

## Critérios de conclusão
- A exportação dos artefactos de estado (pesos e configuração) é validada.
- A redução da perda foi comprovada no treino simulado.

## O que não fazer
- **Não** graves o modelo através de `torch.save(model, 'model.pt')`. Essa técnica grava caminhos diretos no código e quebra incompatibilidades de máquina na hora da importação noutro portátil. Exporta apenas o `state_dict`.

## Dependências
- Baseias-te no processamento das matrizes P4 e entregas o estado do modelo ao fluxo central, que coordena a gravação de `manifesto.json`.

## Fluxo Git
- Ramo: `funcionalidade/SCRUM-9-rede-neuronal`
- Commit: `[SCRUM-9] Adicionar rede neuronal e serialização dos pesos`

## Comentários esperados
- Docstrings que expliquem as dimensões de entrada e de saída (`logits`).
- Comentários breves que justifiquem os hiperparâmetros escolhidos.
