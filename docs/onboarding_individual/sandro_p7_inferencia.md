# Onboarding — Sandro (P7: Inferência e LLM Opcional)

## O teu papel em linguagem simples

Tu transformas o projeto treinado numa ferramenta utilizável. Depois de todos criarem loaders, parser, limpeza, vetorização, modelo e métricas, o teu módulo permite pegar num texto novo e pedir uma previsão.

A tua tarefa principal é offline: não depende de internet nem de API externa. A parte LLM é opcional.

## O que vais construir

- `src/inference/predict.py`;
- `tests/test_inference.py`.

A tua classe principal será algo como:

```python
class InferenceEngine:
    def __init__(self, run_id: str):
        ...

    def predict_new_document(self, text: str) -> str:
        ...
```

## Por que isto é importante academicamente

A disciplina avalia a capacidade de transformar um experimento em uma aplicação. Treinar um modelo dentro de um script não basta. É preciso conseguir carregar o modelo depois, aplicar a mesma limpeza, usar o mesmo vocabulário e devolver uma previsão para um novo documento.

A tua etapa demonstra reprodutibilidade e integração. É aqui que se prova que os artefactos do MLOps fazem sentido.

## O contrato que deves respeitar

Entrada:

```bash
python src/inference/predict.py run_001 "texto do sumário novo"
```

O teu código deve ler:

```text
artifacts/run_001/manifest.json
```

E, através dele, carregar:

- `vocab.json`;
- `idf.npy`;
- `id_to_label.json`;
- `model_config.json`;
- `weights.pth`.

Saída:

```text
Predição: REVOGADA
Probabilidade softmax: 0.78
```

Não chames a este valor "confiança" sem um processo próprio de calibração.

## O que deves estudar primeiro

1. O que é inferência.
2. O que é um artefacto de treino.
3. O que é `manifest.json`.
4. O que é `load_state_dict`.
5. O que é limpeza consistente entre treino e teste.
6. O que é uma API key e por que não deve ir para GitHub.

## Como começar sem saber software

Não esperes pelos ficheiros reais. Cria um `manifest.json` falso dentro de uma pasta de teste. Cria também um modelo dummy e um vectorizer dummy. O primeiro objetivo é conseguir ler os caminhos do manifest.

Depois liga o vectorizer. Depois liga o modelo. Só no fim pensa em LLM.

## Teste mínimo esperado

O teu teste deve provar que:

- `InferenceEngine` lê um manifest falso;
- não usa caminhos hardcoded;
- aplica limpeza antes de vetorizar;
- devolve uma label textual, não apenas um número;
- funciona sem internet.

Comando:

```bash
python -m unittest tests/test_inference.py
```

## O que não deves fazer

Não carregues `weights.pth` diretamente com caminho fixo. Não faças inferência com texto cru sem limpeza. Não coloques API keys no código. Não tornes o DeepSeek obrigatório.

## Como explicar na apresentação

Podes dizer:

> A inferência é carregada por `run_id` e `manifest.json`, garantindo que modelo, vocabulário e labels pertencem à mesma execução. Isto evita misturar artefactos incompatíveis e permite usar o sistema de forma reprodutível.

## Como usar IA na tua tarefa

Pede primeiro um plano para a inferência offline. Não envies textos jurídicos reais à IA e não tornes o DeepSeek obrigatório. Uma explicação LLM é texto gerado, não parecer jurídico nem explicabilidade do modelo. Revê, testa sem internet e declara o apoio de IA no PR.
