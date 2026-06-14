# Guia — Sandro (P7: inferência e modelo de linguagem opcional)

## O teu papel em linguagem simples

Tu transformas o projeto treinado numa ferramenta utilizável. Depois de todos criarem carregadores, analisador, limpeza, vetorização, modelo e métricas, o teu módulo permite pegar num texto novo e pedir uma previsão.

A tua tarefa principal é local: não depende da Internet nem de uma API externa. A parte de modelo de linguagem é opcional.

## O que vais construir

- `src/inferencia/motor_inferencia.py`;
- `tests/test_motor_inferencia.py`.

A tua classe principal será algo como:

```python
class MotorInferencia:
    def __init__(self, id_execucao: str):
        ...

    def prever_documento(self, texto: str) -> str:
        ...
```

## Por que isto é importante academicamente

A disciplina avalia a capacidade de transformar um experimento numa aplicação. Treinar um modelo dentro de um script não basta. É preciso conseguir carregar o modelo depois, aplicar a mesma limpeza, usar o mesmo vocabulário e devolver uma previsão para um novo documento.

A tua etapa demonstra reprodutibilidade e integração. É aqui que se prova que os artefactos do MLOps fazem sentido.

## O contrato que deves respeitar

Entrada:

```bash
python src/inferencia/motor_inferencia.py execucao_001 "texto do sumário novo"
```

O teu código deve ler:

```text
artefactos/execucao_001/manifesto.json
```

E, através dele, carregar:

- `vocabulario.json`;
- `idf.npy`;
- `id_para_categoria.json`;
- `configuracao_modelo.json`;
- `pesos.pth`.

Saída:

```text
Previsão: REVOGADA
Probabilidade softmax: 0,78
```

Não chames a este valor "confiança" sem um processo próprio de calibração.

## O que deves estudar primeiro

1. O que é inferência.
2. O que é um artefacto de treino.
3. O que é `manifesto.json`.
4. O que é `load_state_dict`.
5. O que é limpeza consistente entre treino e teste.
6. O que é uma chave de API e por que não deve ser publicada no GitHub.

## Como começar sem saber software

Não esperes pelos ficheiros reais. Cria um `manifesto.json` falso dentro de uma pasta de teste. Cria também um modelo simulado e um vetorizador simulado. O primeiro objetivo é conseguir ler os caminhos do manifesto.

Depois liga o vetorizador. Depois liga o modelo. Só no fim pensa em LLM.

## Teste mínimo esperado

O teu teste deve provar que:

- `MotorInferencia` lê um manifesto simulado;
- não usa caminhos fixos no código;
- aplica limpeza antes de vetorizar;
- devolve uma categoria textual, não apenas um número;
- funciona sem internet.

Comando:

```bash
python -m unittest tests/test_motor_inferencia.py
```

## O que não deves fazer

Não carregues `pesos.pth` diretamente com um caminho fixo. Não faças inferência com texto em bruto sem limpeza. Não coloques chaves de API no código. Não tornes o DeepSeek obrigatório.

## Como explicar na apresentação

Podes dizer:

> A inferência é carregada por `id_execucao` e `manifesto.json`, garantindo que modelo, vocabulário e categorias pertencem à mesma execução. Isto evita misturar artefactos incompatíveis e permite usar o sistema de forma reprodutível.

## Como usar IA na tua tarefa

Pede primeiro um plano para a inferência local. Não envies textos jurídicos reais à IA e não tornes o DeepSeek obrigatório. Uma explicação LLM é texto gerado, não parecer jurídico nem explicabilidade do modelo. Revê, testa sem internet e declara o apoio de IA no PR.
