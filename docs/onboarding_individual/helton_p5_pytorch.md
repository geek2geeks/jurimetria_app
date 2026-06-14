# Onboarding — Helton (P5: PyTorch, Modelo e Treino)

## O teu papel em linguagem simples

Tu constróis e treinas o modelo neural. A Gleicy entrega matrizes numéricas; tu transformas essas matrizes em tensores PyTorch e ensinas uma rede simples a associar padrões de texto às classes de decisão.

## O que vais construir

- `src/models/classifier.py`;
- `src/training/train.py`;
- `tests/test_pytorch.py`.

O teu modelo principal será algo como:

```python
class JurimetriaMLP(nn.Module):
    ...
```

## Por que isto é importante academicamente

A disciplina exige PyTorch, treino de modelo e uso de frameworks profundos. A tua etapa mostra que a equipa sabe sair da matriz NumPy e entrar no ciclo de aprendizagem neural: forward pass, loss, backward pass e otimização.

Academicamente, o teu trabalho demonstra a diferença entre preparar dados e treinar um modelo. Também mostra que modelos devem ser reprodutíveis e carregáveis por outras pessoas.

## O contrato que deves respeitar

Entrada:

```python
X_train: np.ndarray
X_test: np.ndarray
y_train: np.ndarray
y_test: np.ndarray
```

Saída:

```text
artifacts/run_XXX/model/weights.pth
artifacts/run_XXX/model/model_config.json
```

`weights.pth` guarda os pesos. `model_config.json` guarda a arquitetura necessária para reconstruir o modelo.

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
X_dummy = torch.randn(20, 100)
y_dummy = torch.randint(0, 5, (20,))
```

Primeiro prova que o modelo recebe uma matriz e devolve 5 valores por linha. Depois adiciona treino. Depois adiciona exportação dos pesos.

## Teste mínimo esperado

O teu teste deve provar que:

- o modelo recebe `input_dim` e devolve `output_dim=5`;
- uma etapa de treino executa sem erro;
- `weights.pth` é guardado;
- `model_config.json` contém `input_dim`, `hidden_dim` e `output_dim`.

Comando:

```bash
python -m unittest tests/test_pytorch.py
```

## O que não deves fazer

Não uses `torch.save(model, "model.pt")`. Não dependas de GPU. Não esperes pelos dados finais para começar. Não alteres o vocabulário ou labels da Gleicy.

## Como explicar na apresentação

Podes dizer:

> O modelo PyTorch foi implementado como uma MLP simples para demonstrar o ciclo completo de treino neural. Guardámos apenas o `state_dict` e a configuração da arquitetura para garantir portabilidade e inferência reprodutível.

## Como usar IA na tua tarefa

Pede explicação do forward pass, loss e `state_dict` antes de editar. Começa com tensores dummy e um plano curto. Não aceites dependência de GPU nem `torch.save(model)`. Lê o treino linha a linha, executa os testes e declara o apoio de IA no PR.
