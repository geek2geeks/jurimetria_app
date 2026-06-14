# Registo de decisões arquiteturais (ADR)

Este repositório visa justificar o "Porquê" técnico das balizas fechadas aos 8 programadores envolvidos (Por vezes justificar e rastrear o PORQUÊ de algo não poder ser feito, tem mais valor de software que fazer de qualquer forma e esquecer meses depois).

## ADR-01: Restrição de bibliotecas na engenharia de features
- **Data:** Junho de 2026.
- **Contexto:** Podíamos ter usado o `scikit-learn` nativamente via objeto instanciado do TfidfVectorizer. Isto fecharia a feature e divisão de vetores do TF-IDF num dia.
- **Decisão:** Optou-se pela exclusão total e restrição imperativa de `Scikit-Learn` e `Pandas` (excetuando a pequena dependência para captar a `f1_score` de performance de modelo), com exclusividade fechada da Framework Matricial C-backend nativa NumPy.
- **Consequência Académica:** A implementação torna explícitos os cálculos matriciais e exige testes cuidadosos das fórmulas e dimensões. Também aumenta a responsabilidade da equipa pela correção numérica e pelo consumo de memória.

## ADR-02: Isolamento da rota analítica "Decisão" para evitar fuga de informação
- **Data:** Junho de 2026.
- **Contexto:** Se o texto da decisão entrar nas features, o modelo pode aprender diretamente a resposta e produzir métricas artificialmente elevadas.
- **Decisão:** `decisao_bruta`, texto dispositivo, ECLI, URL e trechos de `texto_integral` que revelem a decisão ficam fora de X. Apenas `descritores` e `sumario` limpos podem alimentar o TF-IDF. A categoria normalizada segue separadamente como Y.

## ADR-03: Texto opcional por LLM apenas como bónus
- **Data:** Junho de 2026.
- **Contexto:** Os projetos baseados puramente em API de terceiros podem ruir em horas de demonstração académica perante a banca num ambiente sem acesso Wi-fi nas faculdades (Rate Limits, Firewall restritivo acadêmico, Contas caídas ou falha nos servidores base das IA externas).
- **Decisão:** O modelo PyTorch será autocontido, serializado com `state_dict` e executável offline. O DeepSeek pode formatar texto opcional depois da previsão, com timeout e fallback local. O texto deve ser identificado como gerado e não é aconselhamento jurídico nem explicabilidade científica. Uma probabilidade softmax também não deve ser chamada de confiança calibrada sem calibração e validação próprias.

## ADR-04: Ambiente e ferramentas de apoio

- **Data:** Junho de 2026.
- **Decisão:** O ambiente do projeto usa Anaconda/conda com Python 3.11. O GitHub Spec Kit fica fixado em `v0.10.2`. OpenCode `>=1.14.24` com DeepSeek V4 Pro é recomendado, mas não obrigatório.
- **Justificação:** Python 3.11 é compatível com o projeto e evita o conflito entre o ambiente Python 3.10 inicialmente proposto e os requisitos atuais do Spec Kit.
