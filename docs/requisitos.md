# JurisTriage PT — Especificação de Requisitos de Software

**Projeto:** JurisTriage PT — Classificação Automatizada de Sentido Decisório de Acórdãos Judiciais  
**Disciplina:** Engenharia de Software para IA e Frameworks Profundos  
**Versão:** 3.0 (Consolidação da Entrega 5 — Requisitos)  
**Data:** 19 de Agosto de 2026  
**Responsável pela Consolidação:** Pedro Rodrigues (Tech Lead / P8)  
**Scrum Master:** Gustavo Menezes Gonçalves  
**Revisão de Contratos e Dados:** Daniela (P2)  
**Revisão de Mensurabilidade e Métricas:** Luciana (P6)  

---

## 1. Visão Geral e Contexto de Negócio

O **JurisTriage PT** é uma Prova de Conceito (PoC) académica que implementa um pipeline completo de Engenharia de Software para Inteligência Artificial (MLOps). O objetivo do sistema é classificar o **sentido decisório normativo** de acórdãos dos tribunais superiores portugueses (DGSI/CSM) a partir exclusivamente dos **descritores** e do **sumário** do acórdão.

### 1.1 Cadeia de Transformação Canónica
```text
DocumentoBruto (PDF/JSON) ──► Acordao ──► RegistoClassificacao ──► Matrizes NumPy (TF-IDF)
                                                                       │
                                      ┌────────────────────────────────┘
                                      ▼
                             MLP PyTorch (Treino) ──► Avaliação (Macro-F1 vs Baseline)
                                      │
                                      ▼
                         Artefactos + Manifesto MLOps ──► Motor de Inferência (Local/Isolado)
                                                                       │
                                                       (Opcional) Explicação LLM
```

---

## 2. Requisitos Funcionais (RF)

| ID | Nome | Descrição Formal | Responsável Primário |
|---|---|---|---|
| **RF01** | Ingestão Incremental e Gestão de Memória | O sistema **deve** carregar ficheiros PDF e JSON suplementares a partir do sistema de ficheiros local utilizando geradores/iteradores Python (`Iterator[DocumentoBruto]`), garantindo consumo constante de memória e tolerância a ficheiros corrompidos ou ilegíveis sem interromper a execução do lote. | Alessandro (P1) |
| **RF02** | Extração de Texto Bruto | O sistema **deve** extrair o conteúdo textual completo de acórdãos em formato PDF padrão CSM/DGSI, preservando a sequência textual e a segmentação de páginas para processamento subsequente. | Alessandro (P1) |
| **RF03** | Parsing Posicional e Segregação de Metadados | O sistema **deve** realizar análise estruturada do documento identificando os campos de cabeçalho (`ecli`, `tribunal`, `relator`, `data_acordao`, `processo`, `seccao`) e segregando-os no contrato `Acordao`. Estes campos **não podem** ser utilizados como variáveis preditivas ($X$). | Daniela (P2) |
| **RF04** | Extração Canónica de Variáveis de Entrada ($X$) | O sistema **deve** extrair os `descritores` (`list[str]`) e o `sumario` (`str`), disponibilizando a composição canónica da entrada de classificação exclusivamente através da interface `Acordao.texto_caracteristicas()` (descritores normalizados + sumário). | Daniela (P2) |
| **RF05** | Limpeza Textual e Remoção de Ruído | O sistema **deve** higienizar o texto das decisões, eliminando marcas de formatação e paginação (ex.: `Powered by TCPDF`), cabeçalhos recorrentes, múltiplos espaços em branco e normalizando a caixa de texto e caracteres especiais. | Gustavo (P3) |
| **RF06** | Normalização Canónica do Rótulo de Saída ($Y$) | O sistema **deve** mapear a decisão jurídica em bruto (`decisao_bruta`) para exatamente uma de 5 classes canónicas: `MANTIDA`, `REVOGADA`, `ANULADA`, `NAO_CONHECIDA` e `OUTRA`. Decisões vazias, não reconhecidas ou ambíguas não podem ser forçadas para `OUTRA`, devendo ser rejeitadas para treino ou encaminhadas para revisão. | Gustavo (P3) |
| **RF07** | Construção do Dataset de Classificação | O sistema **deve** transformar instâncias de `Acordao` no contrato `RegistoClassificacao` (contendo `texto_limpo` e `categoria_normalizada`), estruturando a coleção de dados para modelação sem criar acoplamento obrigatório a bibliotecas tabulares como Pandas. | Gleicy (P4) |
| **RF08** | Vetorização TF-IDF Matricial com NumPy | O sistema **deve** converter o texto pré-processado numa matriz numérica esparsa/densa de características TF-IDF utilizando exclusivamente álgebra linear da biblioteca `NumPy`. O ajuste de vocabulário e IDF (`fit`) deve ocorrer estritamente sobre o conjunto de treino; validação, teste e inferência devem executar apenas `transform`. | Gleicy (P4) |
| **RF09** | Treino e Comparação de Redes Neuronais PyTorch | O sistema **deve** implementar modelos de classificação MLP com `torch.nn.Module`, executando o ciclo de treino e validação com `CrossEntropyLoss` e otimizadores PyTorch. O sistema deve treinar e comparar **pelo menos duas configurações experimentais** distintas (ex.: taxa de aprendizagem, camadas ocultas, função de ativação ou regularização), registando as respetivas curvas de perda. | Helton (P5) |
| **RF10** | Avaliação Multiqualidade e Baseline Maioritária | O sistema **deve** avaliar o classificador treinado contra uma *baseline* ingénua de classe maioritária, reportando obrigatoriamente a métrica **Macro-F1** (além de métricas por classe e matriz de confusão), garantindo avaliação justa perante dados desbalanceados. | Luciana (P6) |
| **RF11** | Motor de Inferência Isolado e Autónomo | O sistema **deve** fornecer um módulo de inferência (`MotorInferencia`) capaz de receber um novo `Acordao` ou texto bruto, aplicar a mesma transformação do treino, consultar o modelo persistido e devolver a classe prevista com respetivas pontuações de confiança, funcionando de forma 100% local e desacoplada. | Sandro (P7) |
| **RF12** | Persistência Coerente de Artefactos MLOps | O sistema **deve** serializar e versionar todos os artefactos necessários para reproduzir e executar a inferência (`pesos.pth`, `vocabulario.json`, `idf.npy`, `configuracao_modelo.json`, `metricas.json`), catalogados num ficheiro central `manifesto.json`. *(Opcional)* O sistema pode suportar formatação de explicações via LLM externa sem interferir na decisão do modelo neural. | Pedro (P8) / Sandro (P7) |

---

## 3. Requisitos Não Funcionais (RNF)

| ID | Nome | Categoria | Descrição |
|---|---|---|---|
| **RNF01** | Modularidade e Arquitetura Limpa | Arquitetura | O código fonte deve estar rigorosamente organizado em módulos de responsabilidade única sob `src/` (`dados`, `pre_processamento`, `caracteristicas`, `modelos`, `treino`, `avaliacao`, `inferencia`), comunicando através dos contratos em `src/dados/esquemas.py`. |
| **RNF02** | Tipagem Estática e Análise Estática | Manutenibilidade | Todas as funções, métodos e atributos de classes públicas devem incluir anotações de tipo estritas (`typing`), garantindo validação em tempo de desenvolvimento. |
| **RNF03** | Cobertura de Testes Automatizados | Confiabilidade | O projeto deve disponibilizar uma suite abrangente de testes unitários e de integração utilizando a biblioteca nativa `unittest`, cobrindo todos os módulos do pipeline sem dependências de serviços externos. |
| **RNF04** | Ciência Reproduzível e Determinismo | Reprodutibilidade | O particionamento dos dados, a inicialização de pesos e o treino devem utilizar sementes pseudoaleatórias fixas (`semente = 42`), registando no manifesto os parâmetros de configuração, versões das dependências e sistema operativo. |
| **RNF05** | Eficiência e Baixa Pegada Computacional | Desempenho | O pipeline completo (ingestão de 10 acórdãos, vetorização, treino de 10 épocas e inferência) deve executar em menos de 60 segundos numa máquina convencional (CPU x86_64, 8 GB RAM) sem exigir aceleração por GPU. |
| **RNF06** | Robustez a Classes Desbalanceadas | Qualidade de ML | A validação do classificador não pode admitir a Exatidão (*Accuracy*) como prova única de adequação do modelo, exigindo convergência superior à baseline maioritária em termos de **Macro-F1**. |
| **RNF07** | Tratamento Gracioso de Falhas (*Fail-Safe Parsing*) | Robustez | Processos sem descritores, sem delimitador de "Decisão Integral" ou com campos ausentes devem preencher esses atributos com `None` ou `[]` sem interromper o fluxo de ingestão ou classificação. |
| **RNF08** | Transparência de IA Generativa | Governança | Toda e qualquer utilização de ferramentas de IA generativa (OpenCode, Spec Kit, assistentes) para auxílio ao desenvolvimento deve ser explicitamente declarada nos commits e Pull Requests. |
| **RNF09** | Nomenclatura e Documentação em Português | Padronização | Todos os identificadores de código (classes, funções, variáveis), mensagens de commit, documentação e relatórios devem adotar português de Portugal, salvaguardando termos técnicos universais (ex.: *token*, *fit*, *transform*, *loss*). |

---

## 4. Requisitos de Dados (RD) — Especificação GR4ML

Em conformidade com a metodologia de Engenharia de Requisitos para ML (GR4ML), os contratos de dados do JurisTriage PT são formais e imutáveis:

### RD01 — Contrato `DocumentoBruto`
* **Definição:** Entrada imediata após a leitura física do ficheiro.
* **Atributos:**
  * `caminho`: `Path` — Caminho absoluto ou relativo do ficheiro de origem.
  * `nome_ficheiro`: `str` — Nome base do ficheiro (ex.: `"acordao_001.pdf"`).
  * `texto`: `str` — Conteúdo textual bruto extraído.
  * `numero_paginas`: `int` — Contagem de páginas do documento.
  * `origem`: `str` — Origem do documento (`"pdf"` ou `"json"`).

### RD02 — Contrato Central `Acordao`
* **Definição:** Estrutura canónica que representa o processo judicial analisado.
* **Metadados (Proibidos em $X$):**
  * `ecli`: `str | None` — Identificador ECLI europeu.
  * `tribunal`: `str | None` — Tribunal de origem (ex.: `"Supremo Tribunal de Justiça"`).
  * `relator`: `str | None` — Juiz relator.
  * `data_acordao`: `str | None` — Data formal da decisão.
  * `processo`: `str | None` — Número do processo no tribunal.
  * `seccao`: `str | None` — Secção julgadora.
* **Variáveis Preditivas ($X$):**
  * `descritores`: `list[str]` — Lista de palavras-chave temáticas.
  * `sumario`: `str | None` — Texto resumido das conclusões jurídicas.
* **Variável Alvo ($Y$):**
  * `decisao_bruta`: `str | None` — Dispositivo ou decisão original.
* **Método de Interface:**
  * `texto_caracteristicas()`: Devolve `f"{' '.join(descritores)} {sumario}".strip()`.

### RD03 — Contrato `RegistoClassificacao`
* **Definição:** Registo individual pronto para alimentação ao pipeline numérico.
* **Atributos:**
  * `texto_limpo`: `str` — Texto resultante de `texto_caracteristicas()` após remoção de ruído (RF05).
  * `categoria_normalizada`: `str` — Uma das 5 classes canónicas (RF06).

### RD04 — Estruturas Numéricas e Tensores
* **Matriz de Características ($X$):** `numpy.ndarray` de tipo `float32`, dimensão $(N, V)$, onde $N$ é o número de amostras e $V$ é a dimensão do vocabulário TF-IDF ajustado no treino.
* **Vetor de Rótulos ($y$):** `numpy.ndarray` de tipo `int64`, dimensão $(N,)$, contendo valores inteiros indexados no intervalo $[0, 4]$.
* **Tensores PyTorch:** `torch.FloatTensor` para características e `torch.LongTensor` para rótulos, encapsulados em `TensorDataset` e manipulados via `DataLoader`.

### RD05 — Pacote de Artefactos de Execução MLOps
* **Diretório:** `artefactos/execucao_XXX/`
* **Conteúdo Obrigatório:**
  1. `manifesto.json`: Metadados da execução, semente, parâmetros, métricas e hashes dos artefactos.
  2. `pesos.pth`: Pesos do modelo serializados via `torch.save(rede.state_dict(), ...)`.
  3. `vocabulario.json`: Dicionário termo $\to$ índice gerado no `fit` do treino.
  4. `idf.npy`: Vetor de pesos IDF computado no treino.
  5. `configuracao_modelo.json`: Hiperparâmetros da arquitetura (camadas, neurónios, ativação).
  6. `metricas.json`: Métricas de avaliação alcançadas no conjunto de teste/validação.

---

## 5. Restrições de Projeto, Engenharia e Ética (RST)

| ID | Título | Descrição |
|---|---|---|
| **RST01** | Proibição de Bibliotecas de Alto Nível de ML | É **estritamente proibida** a utilização de `scikit-learn`, `keras`, `fastai`, `spacy` ou bibliotecas similares no pipeline principal. A vetorização TF-IDF deve ser implementada de raiz em `NumPy` e a rede neural implementada exclusivamente em `PyTorch`. |
| **RST02** | Prevenção Estrita de Fuga de Informação (*Anti-Leakage*) | 1. Nenhum campo identificador (`ecli`, `tribunal`, `relator`, `data_acordao`, `processo`, `seccao`, `decisao_bruta`, `texto_integral`, `url`) pode compor as variáveis $X$.<br>2. O cálculo de vocabulário e IDF (`fit`) ocorre **exclusivamente** sobre o conjunto de treino; qualquer projeção de teste, validação ou inferência deve utilizar estritamente `transform`. |
| **RST03** | Proteção do Corpus e Sanidade do Repositório Git | O corpus massivo (gigabytes de PDFs e JSONs reais) **não pode ser incluído no repositório GitHub**, estando estritamente bloqueado via `.gitignore`. O repositório deve conter apenas dados sintéticos, mockados ou pequenas amostras sanitizadas. |
| **RST04** | Privacidade e Segurança de Dados Jurídicos | Nomes de pessoas singulares, segredos de justiça, PDFs brutos ou chaves privadas de API **nunca** devem ser transmitidos a APIs de IA externas (OpenAI, DeepSeek, etc.). |
| **RST05** | Operação Autónoma e Isolamento Offline | A inferência e a classificação principal de acórdãos devem funcionar **100% offline**, sem qualquer dependência obrigatória de conectividade de rede ou de LLMs externas. |
| **RST06** | Governança e Imutabilidade de Contratos | Os esquemas estruturais em `src/dados/esquemas.py` são de co-responsabilidade de Daniela (P2) e Pedro (P8) e não podem ser alterados unilateralmente sem validação de impacto em todos os módulos. |

---

## 6. Critérios de Aceitação (CA)

Os critérios de aceitação foram definidos de forma observável e mensurável no padrão BDD (*Given-When-Then*):

* **CA01 (Ingestão com Memória Controlada — RF01):**  
  *Dado* um diretório contendo múltiplos PDFs, *quando* a função geradora de leitura é executada, *então* deve devolver instâncias de `DocumentoBruto` incrementalmente, mantendo o consumo de memória estável e ignorando ficheiros corrompidos com registo de log de aviso.
* **CA02 (Paridade entre Parser PDF e JSON Irmão — RF02, RF03):**  
  *Dado* um acórdão disponível em PDF e o respetivo JSON irmão com `extraction_success = true`, *quando* ambos são lidos pelos respetivos módulos, *então* os campos `descritores` e `sumario` extraídos pelo parser PDF devem coincidir com os metadados do JSON de referência.
* **CA03 (Tolerância a Metadados Ausentes — RF03, RNF07):**  
  *Dado* um documento sem secção de "Decisão Integral" ou sem "Descritores", *quando* o analisador de metadados processa o texto, *então* deve atribuir `descritores = []` ou `sumario = None` sem lançar exceções.
* **CA04 (Segregação de Variáveis Preditivas — RF04, RST02):**  
  *Dado* um `Acordao` preenchido com todos os metadados e decisão bruta, *quando* o método `Acordao.texto_caracteristicas()` é invocado, *então* nenhuma palavra do ECLI, Tribunal, Relator ou Decisão Bruta deve estar presente no texto resultante.
* **CA05 (Remoção de Ruído de Layout — RF05):**  
  *Dado* um texto contendo a marca `"Powered by TCPDF (www.tcpdf.org)"` e paginações repetitivas, *quando* a função de limpeza é aplicada, *então* todos esses padrões devem ser completamente eliminados do texto resultante.
* **CA06 (Mapeamento Estrito das 5 Classes — RF06):**  
  *Dado* uma coleção de decisões contendo variantes como `"Negado provimento"`, `"Concedido provimento"` e `"Revogada a sentença"`, *quando* a normalização é executada, *então* os rótulos gerados pertencem estritamente ao conjunto `{MANTIDA, REVOGADA, ANULADA, NAO_CONHECIDA, OUTRA}`.
* **CA07 (Tratamento de Decisões Ambíguas — RF06):**  
  *Dado* um acórdão com `decisao_bruta = ""` (vazio) ou com termos contraditórios não mapeados, *quando* a normalização é executada, *então* o sistema não deve forçar a classe para `OUTRA`, assinalando a impossibilidade de rotulação para treino.
* **CA08 (Vetorização Matricial sem Fuga de Dados — RF08, RST02):**  
  *Dado* um conjunto de treino $D_{treino}$ e um conjunto de teste $D_{teste}$, *quando* o `VetorizadorTfidfNumPy` é ajustado com `fit(D_{treino})` e aplicado com `transform(D_{teste})`, *então* a matriz resultante em $D_{teste}$ tem exatamente o mesmo número de colunas que $D_{treino}$, sem que palavras exclusivas de $D_{teste}$ entrem no vocabulário.
* **CA09 (Operação Pura NumPy — RF08, RST01):**  
  *Dado* o código fonte de `src/caracteristicas/vetorizador_tfidf.py`, *quando* analisado estaticamente, *então* não deve existir qualquer importação de `sklearn` ou de módulos de ML externos.
* **CA10 (Comparação Obrigatória de Configurações — RF09):**  
  *Dado* o script de treino principal, *quando* a execução é concluída, *então* devem ser apresentadas as curvas de perda de pelo menos duas configurações de rede (ex.: Config A vs Config B) comprovando a convergência em treino e validação.
* **CA11 (Persistência e Reconstrução do Modelo — RF09, RF12):**  
  *Dado* um treino concluído com sucesso, *quando* os ficheiros `pesos.pth` e `configuracao_modelo.json` são guardados em `artefactos/execucao_XXX/`, *então* o módulo de inferência deve ser capaz de recriar a arquitetura e carregar o `state_dict` com exatidão matemática idêntica.
* **CA12 (Superação da Baseline Maioritária — RF10, RNF06):**  
  *Dado* o relatório de avaliação no conjunto de teste, *quando* o classificador neural é comparado com o classificador ingénuo de classe maioritária, *então* o modelo neural deve reportar o seu valor de **Macro-F1** superando a baseline maioritária.
* **CA13 (Inferência Autónoma sem Rede — RF11, RST05):**  
  *Dado* um ambiente sem ligação à Internet e sem chaves de API configuradas, *quando* o comando de inferência é executado sobre um novo acórdão, *então* o sistema deve devolver a previsão e as probabilidades de classe com sucesso.
* **CA14 (Integridade do Manifesto MLOps — RF12):**  
  *Dado* o ficheiro `manifesto.json` gerado no treino, *quando* inspecionado, *então* deve conter os caminhos válidos para `pesos.pth`, `vocabulario.json`, `idf.npy`, `configuracao_modelo.json` e `metricas.json`, acompanhados da semente pseudoaleatória utilizada (`42`).
* **CA15 (Isolamento de Segredos e API Keys — RNF06, RST04):**  
  *Dado* o histórico completo do Git e os ficheiros de código versionados, *quando* submetidos a varrimento de credenciais, *então* nenhuma chave de API ou segredo deve constar nos commits.
* **CA16 (Sucesso da Suite de Testes — RNF03):**  
  *Dado* o repositório clonado, *quando* o comando `python -m unittest discover -s tests` é executado, *então* 100% dos testes unitários devem passar sem erros.

---

## 7. Matriz de Rastreabilidade (Traceability Matrix)

A matriz abaixo estabelece o mapeamento bidirecional entre as necessidades de negócio da disciplina, os requisitos de software, os critérios de aceitação e os módulos de implementação e verificação:

| Necessidade / Objetivo | Requisito Principal | Requisitos Relacionados | Critério de Aceitação (CA) | Módulo / Ficheiro de Implementação | Evidência de Verificação |
|---|---|---|---|---|---|
| Ingestão eficiente de jurisprudência sem saturação de RAM | **RF01** | RNF01, RNF05, RNF07, RD01 | CA01, CA03 | `src/dados/carregador_pdf.py`<br>`src/dados/carregador_json_bruto.py` | `tests/test_carregador_pdf.py` |
| Extração fiável do texto integral dos acórdãos | **RF02** | RNF05, RD01 | CA02 | `src/dados/carregador_pdf.py` | `tests/test_carregador_pdf.py` |
| Isolamento estrito de metadados e blindagem anti-leakage | **RF03** | RF04, RNF07, RD02, RST02 | CA02, CA03, CA04 | `src/pre_processamento/analisador_metadados.py`<br>`src/dados/esquemas.py` | `tests/test_analisador_metadados.py`<br>`tests/test_esquemas.py` |
| Padronização das variáveis de entrada $X$ (descritores + sumário) | **RF04** | RF05, RD02, RD03, RST02 | CA04 | `src/dados/esquemas.py` (`Acordao`) | `tests/test_esquemas.py` |
| Higienização e remoção de ruído textual de PDFs | **RF05** | RNF01, RD03 | CA05 | `src/pre_processamento/limpeza_texto.py` | `tests/test_limpeza_texto.py` |
| Categorização unificada do sentido decisório ($Y$ em 5 classes) | **RF06** | RNF06, RD03, RST02 | CA06, CA07 | `src/pre_processamento/limpeza_texto.py`<br>`docs/decisoes.md` (ADR-05) | `tests/test_limpeza_texto.py` |
| Construção de dataset de modelação sem acoplamento a Pandas | **RF07** | RNF01, RNF02, RD03, RD04 | CA08 | `src/caracteristicas/vetorizador_tfidf.py`<br>`src/dados/esquemas.py` | `tests/test_vetorizador_tfidf.py` |
| Vetorização TF-IDF matricial pura e sem fuga de dados | **RF08** | RNF04, RD04, RST01, RST02 | CA08, CA09 | `src/caracteristicas/vetorizador_tfidf.py` | `tests/test_vetorizador_tfidf.py` |
| Treino de rede neural com PyTorch e estudo de configurações | **RF09** | RNF03, RNF04, RD04, RST01 | CA10, CA11 | `src/modelos/rede_neuronal.py`<br>`src/treino/treinar_modelo.py` | `tests/test_rede_neuronal.py`<br>`tests/test_treino.py` |
| Avaliação robusta com Macro-F1 contra baseline ingénua | **RF10** | RNF04, RNF06, RD04 | CA12 | `src/avaliacao/metricas.py` | `tests/test_metricas.py` |
| Inferência local, rápida e independente de conectividade | **RF11** | RNF05, RNF07, RST04, RST05 | CA13 | `src/inferencia/motor_inferencia.py`<br>`src/inferencia/executar_inferencia.py` | `tests/test_motor_inferencia.py`<br>`tests/test_executar_inferencia.py` |
| Persistência estruturada de artefactos e rastreabilidade MLOps | **RF12** | RNF04, RD05, RST03, RST04 | CA11, CA14, CA15 | `src/treino/persistencia_execucao.py`<br>`src/dados/manifesto.py` | `tests/test_persistencia_execucao.py`<br>`tests/test_manifesto.py` |
| Conformidade de Engenharia de Software e Qualidade de Código | **RNF01-09** | RST01-06 | CA15, CA16 | Todo o repositório (`src/`, `tests/`, `docs/`) | CI GitHub Actions / `unittest discover` |

---

## 8. Glossário de Termos

* **Acórdão:** Decisão proferida por um tribunal coletivo superior (STJ, Relação).
* **Descritores:** Termos e palavras-chave jurídicas indexadas ao acórdão.
* **Sumário:** Síntese conclusiva elaborada pelo relator sobre as matérias de direito apreciadas.
* **Decisão Bruta:** Texto do dispositivo final do julgamento (ex.: *"Acordam em negar a revista..."*).
* **Data Leakage (Fuga de Informação):** Entrada indevida de dados da resposta ($Y$) ou de metadados não preditivos no conjunto de características ($X$), comprometendo a validade estatística do modelo.
* **Fit / Transform:** `Fit` é o cálculo estatístico de parâmetros (vocabulário, IDF) exclusivo do treino; `Transform` é a aplicação desses parâmetros em dados novos.
* **Macro-F1:** Média não ponderada das pontuações F1 de todas as classes, tratando classes minoritárias com a mesma relevância que classes maioritárias.
* **Manifesto MLOps:** Ficheiro JSON estruturado que indexa, autentica e correlaciona todos os artefactos de treino com os metadados de execução.
