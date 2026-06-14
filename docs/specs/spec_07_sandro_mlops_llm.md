# Especificação: Inferência e Explicador Jurídico via LLM

**Assignee:** Sandro (P6 - Especialista MLOps - Parte 2)
**Fase do SDD:** Specify

## 1. Contexto (O Porquê)
Um juiz ou um advogado recusa-se a confiar num "Black Box" do PyTorch que atira a previsão "75% de chance de Improvimento". Para a cereja final do projeto, e completando as operações de AI Produto, o Sandro consumirá a previsão numérica calculada pelo Helton e usará a API do **DeepSeek 4 Pro** para converter o raciocínio matemático num parágrafo de Português Jurídico polido e fundamentado (Explainable AI).

## 2. Tarefa Técnica (O Quê)
1. Desenvolver o módulo `src/inference/llm_integration.py`.
2. A classe deve ler as Variáveis de Ambiente do Sistema (via pacote `os` ou `dotenv`) à procura da `DEEPSEEK_API_KEY` fornecida pelo Pedro.
3. Criar a função interativa: A aplicação final onde se passa a *string* do Sumário ("Caso sobre assédio moral e rescisão"), invoca-se o classificador do Helton ("Resultado: MANTIDA"), e preenche-se o Prompter: *"O classificador prevê MANTIDA. Baseando no Sumário {sumario}, justifique juridicamente como se falasse a um advogado."*
4. Executar chamada remota REST para a infraestrutura do DeepSeek usando a biblioteca `requests` ou o SDK adequado e apanhar a string limpa resultante.

## 3. Inputs e Outputs
- **Input Módulo:** Uma string pura de caso legal simulado (Sumário) e um Integer ou String do PyTorch.
- **Output Módulo:** Uma string devolvida com o raciocínio do modelo fundacional de IA.
- **Falha de Rede:** Em caso da API falhar por *timeout* ou *Auth Error*, a inferência deve apenas devolver a decisão dura do PyTorch, garantindo tolerância à falha (Fallback Mode).

## 4. Regras e Restrições SDD
- **Segurança OBRIGATÓRIA:** As chaves de API nunca podem ser "hardcoded" (coladas diretamente) no script Python. Se o Sandro o fizer e realizar *commit* no GitHub, a IA bloqueia-o.
- **Isolamento de Erros (Try/Except):** Toda chamada Web deve suportar os picos de latência (Timeouts de segurança).

## 5. Critérios de Aceitação (DoD)
- [ ] Chamada Web não quebra o ecossistema local.
- [ ] Interface visual amigável pela consola para que o professor faça a bateria de testes.
- [ ] O ficheiro `unittests` pode usar o pacote `unittest.mock` para simular as respostas do DeepSeek sem gastar créditos na integração remota (`tests/test_inference.py`).

---

> **Instrução para Agente de IA:**
> Leia a Constituição em `docs/`.
> Invoque `/speckit.clarify`: Questione ao Sandro quais devem ser os exatos limites de tokens de *system prompt* a passar ao LLM de forma a manter o orçamento de tokens da conta da universidade protegido. Avançar para o `/speckit.plan`.
