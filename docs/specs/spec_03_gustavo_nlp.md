# Especificação: Limpeza NLP e Normalização de Labels

**Assignee:** Gustavo (P3 - Especialista NLP)
**Fase do SDD:** Specify

## 1. Contexto (O Porquê)
No Direito Português há dezenas de formas de dizer a mesma coisa (ex: "Negado provimento", "Improcedente", "Mantida"). A nossa Rede Neural não vai aprender nada se o nosso vetor de saída (`y`) tiver 300 classes diferentes. Precisamos de limpar o ruído do texto e normalizar as sentenças em categorias padrão.

## 2. Tarefa Técnica (O Quê)
1. Criar o módulo `src/preprocessing/cleaner.py`.
2. Desenvolver a função `clean_text(text: str) -> str`: deve remover cabeçalhos de tribunal, artefactos ("Powered by TCPDF"), numeração de página e stop-words de baixo valor, convertendo tudo para *lowercase*.
3. Desenvolver a função `normalize_decision(decision_raw: str) -> str`: usar um dicionário de mapeamento ou regex para condensar as variações verbais em 4 classes restritas:
   - `MANTIDA`
   - `REVOGADA`
   - `ANULADA`
   - `NAO_CONHECIDA`

## 3. Inputs e Outputs
- **Input Limpeza:** String bruta com quebras de linha sujas.
- **Output Limpeza:** String monolítica pronta para TF-IDF.
- **Input Normalização:** String com a decisão jurídica exata extraída pela Daniela (ex: "Concedida a revista").
- **Output Normalização:** Enum ou String padronizada (ex: `REVOGADA`). Se o texto não mapear, retornar `OUTRA`.

## 4. Regras e Restrições SDD
- **Velocidade:** Evitar compilar Regex repetidamente dentro do *loop*. Compilar (`re.compile`) a nível de módulo.
- **Isolamento:** Este código não deve depender de redes neurais ou pacotes pesados como `spacy` se expressões regulares cumprirem os requisitos funcionais rápidos da amostra.

## 5. Critérios de Aceitação (DoD)
- [ ] O `test_cleaner.py` tem que possuir pelo menos 10 Casos de Uso (Edge Cases) testando lixo de PDF jurídico.
- [ ] A função de normalização mapeia 90% das expressões de "ganho/perda" comuns do STJ para uma das 4 classes.

---

> **Instrução para Agente de IA:**
> Leia a Constituição em `docs/`. 
> Executa `/speckit.clarify` e pede ao Gustavo o dicionário exato de mapeamento de termos (o glossário de sinónimos jurídicos). Seguidamente executa o `/speckit.plan`.
