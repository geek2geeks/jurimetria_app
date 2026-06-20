# Guia — Helton (P5: PyTorch, modelo e treino)

## O teu papel em linguagem simples

Tu constróis e treinas o modelo neural. A Gleicy entrega matrizes numéricas; tu transformas essas matrizes em tensores PyTorch e ensinas uma rede simples a associar padrões de texto às classes de decisão.

## O que vais construir

- `src/modelos/rede_neuronal.py`;
- `src/treino/treinar_modelo.py`;
- `tests/test_rede_neuronal.py`.

O teu modelo principal será algo como:

```python
class RedeNeuronalClassificacao(nn.Module):
    ...
```

## Por que isto é importante academicamente

A disciplina exige PyTorch, treino de modelo e uso de bibliotecas de aprendizagem profunda. A tua etapa mostra que a equipa sabe passar da matriz NumPy para o ciclo de aprendizagem neuronal: passagem direta, cálculo da perda, retropropagação e otimização.

Academicamente, o teu trabalho demonstra a diferença entre preparar dados e treinar um modelo. Também mostra que modelos devem ser reprodutíveis e carregáveis por outras pessoas.

## O contrato que deves respeitar

Entrada:

```python
caracteristicas_treino: np.ndarray
caracteristicas_teste: np.ndarray
categorias_treino: np.ndarray
categorias_teste: np.ndarray
```

Saída:

```text
artefactos/execucao_XXX/modelo/pesos.pth
artefactos/execucao_XXX/modelo/configuracao_modelo.json
```

`pesos.pth` guarda os pesos. `configuracao_modelo.json` guarda a arquitetura necessária para reconstruir o modelo.

## O que deves estudar primeiro

1. O que é um tensor.
2. O que é uma rede neural.
3. O que é uma camada Linear.
4. O que é função de perda.
5. O que é `state_dict`.
6. Por que não se deve guardar o modelo inteiro com `torch.save(model)`.

## Como começar sem saber software

Começa com dados falsos. Não esperes pela Gleicy. Usa:

```python
caracteristicas_simuladas = torch.randn(20, 100)
categorias_simuladas = torch.randint(0, 5, (20,))
```

Primeiro prova que o modelo recebe uma matriz e devolve 5 valores por linha. Depois adiciona treino. Depois adiciona exportação dos pesos.

## Teste mínimo esperado

O teu teste deve provar que:

- o modelo recebe `numero_entradas` e devolve `numero_saidas=5`;
- uma etapa de treino executa sem erro;
- `pesos.pth` é guardado;
- `configuracao_modelo.json` contém `numero_entradas`, `numero_ocultas` e `numero_saidas`.

Comando:

```bash
python -m unittest tests/test_rede_neuronal.py
```

## O que não deves fazer

Não uses `torch.save(model, "model.pt")`. Não dependas de GPU. Não esperes pelos dados finais para começar. Não alteres o vocabulário ou categorias da Gleicy.

## Como explicar na apresentação

Podes dizer:

> O modelo PyTorch foi implementado como uma MLP simples para demonstrar o ciclo completo de treino neural. Guardámos apenas o `state_dict` e a configuração da arquitetura para garantir portabilidade e inferência reprodutível.

## Como usar IA na tua tarefa

Pede uma explicação da passagem direta, da função de perda e de `state_dict` antes de editar. Começa com tensores simulados e um plano curto. Não aceites dependência de GPU nem `torch.save(model)`. Lê o treino linha a linha, executa os testes e declara o apoio de IA no pedido de integração.

## Especificações Técnicas Originais

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