# Especificação 07 — Motor de inferência e modelo de linguagem opcional

## Responsável
Sandro — Motor de inferência e modelo de linguagem opcional (P7)

## Jira
`SCRUM-11`

## Objetivo em linguagem simples
A tua missão foca-se na reconstrução realística do projeto, contendo duas vertentes:
Vertente principal: vais construir um programa que recebe um identificador de execução (`id_execucao`). A partir de `manifesto.json`, reconstrói o vetorizador, o mapa de categorias e o modelo para classificar novos sumários. Antes da vetorização, deve usar a mesma rotina de limpeza do Gustavo, garantindo que a inferência avalia texto normalizado.
Vertente secundária: opcionalmente, podes adicionar uma ligação REST a um modelo de linguagem, como o DeepSeek, para apresentar o resultado em texto legível.

## Porque é importante
Se a nossa plataforma não puder ser invocada isoladamente em inferência, de nada nos serve ter criado modelos poderosos. Este passo assegura também consistência através do carregamento de parâmetros do `manifesto` - prevenindo misturas perigosas entre versões da rede e do dicionário NumPy!

## Entradas
- Um argumento de linha de comandos que indica a diretoria do modelo por meio do identificador da execução (`execucao_001`).
- Um fragmento de sumário em bruto.

## Saídas
- O terminal apresenta a previsão final para esse sumário.
- Opcionalmente, um texto gerado pelo modelo de linguagem descreve a previsão, sem valor de parecer jurídico nem de explicação validada.

## Ficheiros a criar ou alterar
- `src/inferencia/motor_inferencia.py`
- `tests/test_motor_inferencia.py`

## Lista de trabalho
- [ ] Confirma na `constitution.md` os limites aplicáveis a chaves de API.
- [ ] No ficheiro `motor_inferencia.py`, constrói a classe `MotorInferencia` que recebe `id_execucao` e lê o manifesto.
- [ ] Importa apenas as dependências necessárias dos módulos anteriores: limpeza de texto P3, vetorizador P4 e rede neuronal P5.
- [ ] Cria o fluxo de previsão: limpeza de texto -> `transform` do vetorizador NumPy -> passagem direta em PyTorch -> remapeamento com `id_para_categoria`.

## Exemplo
**Inferência com o programa:** `motor_inferencia.py execucao_001 "Acórdão criminal provido..."`
O teu código retorna de imediato:
`Previsão: REVOGADA (probabilidade softmax: 0,78)`

Não chamar a esta probabilidade "confiança" sem calibração e validação próprias.

## Testes
Cria testes unitários em `tests/test_motor_inferencia.py`. Podes usar manifestos e pastas temporárias para testar o carregamento de artefactos.

## Critérios de conclusão
- A inferência limpa, transforma e prevê consistentemente, lendo caminhos orientados apenas pelo seu manifesto estático, abstendo-se de codificar caminhos absolutos ("fixos no código") para dicionários de treino.
- Nenhuma submissão do módulo contém senhas, chaves ou segredos para serviços.

## O que não fazer
- Não esqueças a limpeza! Processar texto sujo diretamente na inferência gera incongruências nos resultados em comparação ao treino.
- Foca-te primeiro no motor de inferência local. A ligação remota ao modelo de linguagem é um acrescento secundário.

## Dependências
- O teu módulo consome implicitamente o trabalho dos restantes alunos, desde as funções lógicas do P3 e P4, ao manifesto e artefactos de P5 e P8.

## Fluxo Git
- Ramo: `funcionalidade/SCRUM-11-motor-inferencia`
- Commit: `[SCRUM-11] Adicionar motor de inferência orientado pelo manifesto`

## Comentários esperados
- Avisos explícitos contra chaves de API fixas no código.
- Comentários orientativos sobre como simular ou instanciar os caminhos da infraestrutura de teste.
