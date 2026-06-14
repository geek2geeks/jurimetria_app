# Requisitos do Sistema

Este documento consolida os Requisitos Funcionais (RF) e os Requisitos Não Funcionais (RNF) definidos formalmente para o projeto da cadeira de Engenharia de Software para IA.

## Requisitos Funcionais (O que o sistema faz)
- **RF01:** Carregar PDFs (e JSONs suplementares) de uma pasta local com gestão graciosa de memória, usando Iteradores/Generators Python.
- **RF02:** Extrair texto bruto do interior dos PDFs do layout padrão do CSM.
- **RF03:** Efetuar parsing posicional inteligente (Metadata Extraction) da tabela de colunas do PDF (Isolando ECLI, Tribunal, Relator, etc).
- **RF04:** Extrair especificamente os "Descritores" e o "Sumário" (Variáveis X de Entrada).
- **RF05:** Limpar ruído de layout do documento (cabeçalhos redundantes, paginação, lixo de marca d'água TCPDF).
- **RF06:** Normalizar as diferentes sentenças jurídicas do Rótulo "Decisão" (Variável Y de Saída) numa lista condensada de 5 Classes (`MANTIDA`, `REVOGADA`, etc).
- **RF07:** Construir um dataset tabular limpo para transição a Machine Learning.
- **RF08:** Vetorizar o texto usando exclusivamente computação matricial da biblioteca `NumPy` (implementando TF-IDF customizado).
- **RF09:** Treinar um modelo Classificador Multilayer Perceptron usando exclusivamente `PyTorch`.
- **RF10:** Avaliar a real eficácia do modelo treinado medindo-o contra uma *Baseline Cega* de maioria, priorizando o output da métrica **Macro-F1**.
- **RF11:** Executar inferência isolada. Receber o Sumário de um único novo PDF e devolver a classe final prevista sem dependências externas massivas.
- **RF12:** (Opcional) Exportar as métricas e binários do PyTorch (`state_dict` em `weights.pth` + configuração em `model_config.json`) e usar um LLM externo apenas para formatar uma explicação textual claramente identificada como gerada. Esta explicação não é parecer jurídico nem prova de explicabilidade do classificador.

## Requisitos Não Funcionais (Como o sistema opera com qualidade)
- **RNF01 (Modularidade):** O código deve estar estritamente fragmentado em módulos dentro da diretoria `/src`, e com responsabilidade única.
- **RNF02 (Tipagem Estática):** Toda e qualquer função no ecossistema deve adotar os Type Hints embutidos da biblioteca `typing`.
- **RNF03 (Cobertura de Testes):** A infraestrutura deve suportar e requerer a execução de scripts `unittest`.
- **RNF04 (Ciência Reproduzível):** Fixar uma `SEED = 42` nos splits e inicializações, registar versões, configuração e plataforma, e usar opções determinísticas quando aplicável. A seed reduz variação, mas não garante resultados idênticos entre sistemas.
- **RNF05 (Sanidade Git e Custo):** O corpus massivo (gigabytes de PDFs) não pode ser adicionado ao repositório GitHub (`.gitignore` imposto).
- **RNF06 (Segurança):** Em caso de uso de LLM, nenhuma API Key (DeepSeek) poderá transitar pelo histórico de commits. Apenas gestão por `.env` ou variáveis do SO.
- **RNF07 (Portabilidade):** O pipeline deve rodar end-to-end numa amostra de apenas 10 PDFs (Tiny Sample) num Laptop modesto, garantindo a acessibilidade no momento do desenvolvimento e demonstração.
- **RNF08 (Rigor Métrico):** A medição da performance no classificador de dados muito desequilibrados deve rejeitar a Accuracy como sucesso e provar o Macro-F1.
- **RNF09 (Robustez Posicional):** O parser do Metadata deve tolerar e assumir nativamente que certos processos antigos não têm descritores ou secções de "Decisão Integral". Um erro pontual não pode quebrar a pipeline e deve retornar tipo `None`.
- **RNF10 (Data Leakage):** A pipeline e a documentação devem provar estruturalmente que a resposta verdadeira da Decisão de um juiz nunca viajou dentro das variáveis explicativas fornecidas ao tensor de treino do PyTorch.
- **RNF11 (Serviços Externos):** PDFs, JSONs reais, `full_text`, `decisao_raw`, dados pessoais, segredos e artefactos identificáveis não podem ser enviados para agentes de IA ou APIs externas.
