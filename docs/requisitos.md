# Requisitos do Sistema

Este documento consolida os Requisitos Funcionais (RF) e os Requisitos Não Funcionais (RNF) definidos formalmente para o projeto da cadeira de Engenharia de Software para IA.

## Requisitos Funcionais (O que o sistema faz)
- **RF01:** Carregar PDFs (e JSONs suplementares) de uma pasta local com gestão graciosa de memória, usando Iteradores/Generators Python.
- **RF02:** Extrair texto bruto do interior dos PDFs do layout padrão do CSM.
- **RF03:** Efetuar parsing posicional inteligente (Metadata Extraction) da tabela de colunas do PDF (Isolando ECLI, Tribunal, Relator, etc).
- **RF04:** Extrair especificamente os "Descritores" e o "Sumário" (Variáveis X de Entrada).
- **RF05:** Limpar ruído de layout do documento (cabeçalhos redundantes, paginação, lixo de marca d'água TCPDF).
- **RF06:** Normalizar as diferentes sentenças jurídicas do Rótulo "Decisão" (Variável Y de Saída) numa lista condensada de 5 Classes (`MANTIDA`, `REVOGADA`, etc).
- **RF07:** Construir um conjunto de dados tabular limpo para aprendizagem automática.
- **RF08:** Vetorizar o texto usando exclusivamente computação matricial da biblioteca `NumPy` (implementando TF-IDF customizado).
- **RF09:** Treinar um modelo Classificador Multilayer Perceptron usando exclusivamente `PyTorch`, **comparando pelo menos duas configurações** (ex.: nº de camadas, ativação ou batch size) com a respetiva curva de perda.
- **RF10:** Avaliar o modelo contra uma referência de classe maioritária, priorizando a métrica **Macro-F1**.
- **RF11:** Executar inferência isolada. Receber a **mesma composição de entrada do treino** (descritores + sumário, via `Acordao.texto_caracteristicas()`) de um novo documento e devolver a classe final prevista, sem dependências externas massivas.
- **RF12:** (Opcional) Exportar métricas e binários do PyTorch (`state_dict` em `pesos.pth` e configuração em `configuracao_modelo.json`) e usar um modelo de linguagem externo apenas para formatar uma explicação textual identificada como gerada.

## Requisitos Não Funcionais (Como o sistema opera com qualidade)
- **RNF01 (Modularidade):** O código deve estar estritamente fragmentado em módulos dentro da diretoria `/src`, e com responsabilidade única.
- **RNF02 (Tipagem Estática):** Toda e qualquer função no ecossistema deve adotar os Type Hints embutidos da biblioteca `typing`.
- **RNF03 (Cobertura de Testes):** A infraestrutura deve suportar e requerer a execução de scripts `unittest`.
- **RNF04 (Ciência Reproduzível):** Fixar `semente = 42` nas divisões e inicializações, registar versões, configuração e plataforma, e usar opções determinísticas quando aplicável.
- **RNF05 (Sanidade Git e Custo):** O corpus massivo (gigabytes de PDFs) não pode ser adicionado ao repositório GitHub (`.gitignore` imposto).
- **RNF06 (Segurança):** Em caso de uso de LLM, nenhuma API Key (DeepSeek) poderá transitar pelo histórico de commits. Apenas gestão por `.env` ou variáveis do SO.
- **RNF07 (Portabilidade):** O fluxo deve funcionar de ponta a ponta numa amostra de 10 PDFs num computador modesto.
- **RNF08 (rigor métrico):** a avaliação de um classificador com dados muito desequilibrados não pode usar apenas a exatidão como prova de sucesso; deve incluir Macro-F1.
- **RNF09 (Robustez Posicional):** O analisador de metadados deve tolerar processos sem descritores ou secções de "Decisão Integral". Um erro pontual não pode interromper o fluxo e deve devolver `None`.
- **RNF10 (Fuga de Informação):** O fluxo e a documentação devem provar que a decisão verdadeira nunca entrou nas características fornecidas ao tensor de treino.
- **RNF11 (Serviços Externos):** PDFs, JSONs reais, `texto_integral`, `decisao_bruta`, dados pessoais, segredos e artefactos identificáveis não podem ser enviados para agentes de IA ou APIs externas.
