# JurisTriage PT — Constituição do Projeto

**Versão:** 2.5
**Projeto:** JurisTriage PT
**Disciplina:** Engenharia de Software para IA e Frameworks Profundos
**Metodologia:** Spec-Driven Development (SDD) + GitHub + Jira
**Lead:** Pedro

Esta Constituição define as regras de engenharia, colaboração, segurança e qualidade do projeto.
Todos os membros da equipa e qualquer agente de IA que trabalhe neste repositório devem seguir este documento.

---

## 1. Equipa e responsabilidades gerais

A equipa tem 8 pessoas:

| Pessoa | Papel principal |
|---|---|
| Alessandro | P1 — Ingestão e carregamento de dados |
| Daniela | P2 — Parsing posicional de metadados |
| Gustavo | P3 — Limpeza textual e normalização de categorias |
| Gleicy | P4 — Vetorização NumPy e divisão dos dados |
| Helton | P5 — Modelo PyTorch e treino |
| Luciana | P6 — Modelo de referência, métricas e avaliação |
| Sandro | P7 — Inferência e explicação opcional |
| Pedro | P8 — Responsável técnico, qualidade, requisitos, arquitetura, Jira e GitHub |

---

## 2. Escopo Obrigatório vs Opcional

| Escopo | Itens |
|---|---|
| **Must Have** | Carregamento de PDFs/JSON, análise de metadados, limpeza, vetorização NumPy, modelo PyTorch, modelo de referência, avaliação, inferência isolada, testes e documentação. |
| **Could Have** | Explicação textual via LLM/DeepSeek. |

---

## 3. Contratos de dados internos

Para garantir a coesão da equipa, evitamos usar dicionários genéricos. O projeto assenta em três contratos principais, definidos em `src/dados/esquemas.py` e co-mantidos por Pedro e Daniela:

1. **`DocumentoBruto`**: Representa um documento acabado de ser carregado (PDF ou JSON em bruto). Usado antes da análise de metadados.
2. **`Acordao`**: O contrato central. Representa o acórdão estruturado, incluindo `ecli`, `sumario` e `decisao_bruta`. Independentemente da fonte, a partir do P2 todo o projeto consome `Acordao`.
3. **`RegistoClassificacao`**: O registo pronto para aprendizagem automática, contendo o texto final limpo e a categoria normalizada.

---

## 4. Gestão de artefactos MLOps e manifesto

Cada treino gera pesos, vocabulários e métricas que têm de permanecer alinhados. Cada execução cria uma subpasta em `artefactos/`.

**Estrutura Recomendada:**
```text
artefactos/
└── execucao_001/
    ├── vetorizador/
    │   ├── vocabulario.json
    │   ├── idf.npy
    │   └── configuracao.json
    ├── categorias/
    │   ├── categoria_para_id.json
    │   └── id_para_categoria.json
    ├── modelo/
    │   ├── configuracao_modelo.json
    │   └── pesos.pth
    ├── metricas.json
    └── manifesto.json
```

**Regras de Arquitetura MLOps:**
1. A inferência (P7) nunca deve carregar ficheiros soltos manualmente. Deve pedir o `id_execucao` e usar o respetivo `manifesto.json` para carregar tudo em sincronia.
2. O modelo PyTorch (P5) deve ser gravado estritamente com `state_dict()` em `pesos.pth`. A arquitetura base fica em `configuracao_modelo.json`.
3. O vetorizador TF-IDF (P4) só pode efetuar `fit` em `caracteristicas_treino`. Validação, teste e inferência usam apenas `transform()`.

---

## 5. Regras sobre PDFs, JSONs e fuga de informação

- O analisador de metadados deve ser tolerante a campos ausentes, usando `None`.
- A `decisao_bruta`, o texto dispositivo, ECLI, URL e qualquer trecho de `texto_integral` que revele a decisão NUNCA entram na matriz explicativa (X).
- As únicas fontes de texto autorizadas para X são `descritores` e `sumario`, depois da limpeza definida pelo P3.
- Cada PDF do corpus vem com um JSON irmão (`extraction_success=true`), que é a **source of truth** da extração e o desbloqueador da equipa. O parser posicional de PDF (P2) deve ser **validado contra** esse JSON. Schema e mapeamento em `docs/esquema_json_corpus.md`. Regra:
  - JSON em bruto -> `DocumentoBruto` -> `analisador_metadados` -> `Acordao`
  - JSON estruturado -> `carregador_acordaos_json` -> `Acordao`

---

## 6. Classes de decisão

As cinco classes iniciais, aprovadas pelo Pedro como responsável técnico, são:

1. `MANTIDA`
2. `REVOGADA`
3. `ANULADA`
4. `NAO_CONHECIDA`
5. `OUTRA`

O dicionário que converte expressões jurídicas para estas classes foi decidido com base na distribuição real do corpus e está documentado em `docs/esquema_json_corpus.md` §5 e no ADR-05 (`docs/decisoes.md`). Casos ambíguos não devem ser adivinhados: ficam sem categoria ou são encaminhados para revisão.

---

## 7. Desenvolvimento assistido por IA e revisão humana

O professor aprovou a equipa de oito pessoas, mas não concedeu uma autorização específica para código gerado por IA. Cada aluno deve respeitar as regras da disciplina e, em caso de dúvida, confirmar com o professor.

Se um membro usar IA para programar:

- deve seguir o fluxo SDD descrito em `docs/fluxo_desenvolvimento_ia.md`;
- deve tratar toda a resposta da IA como rascunho;
- deve ler e compreender cada alteração;
- deve executar os testes;
- deve declarar o uso de IA no pedido de integração;
- deve obter revisão humana antes da integração.

Pedro é o revisor obrigatório dos pedidos de integração dos restantes membros. Como administrador e responsável técnico, Pedro pode validar e integrar os próprios pedidos, desde que os testes sejam executados e a decisão fique documentada.

Ferramentas recomendadas, mas não obrigatórias:

- GitHub Spec Kit `v0.10.2`;
- OpenCode `>=1.14.24`;
- DeepSeek V4 Pro;
- Anaconda/conda com Python 3.11.

Nenhuma IA pode inventar contratos, alterar `DocumentoBruto`, `Acordao` ou `RegistoClassificacao` sem aprovação de Pedro e Daniela, contornar testes ou integrar alterações diretamente em `main`.

> A IA pode escrever código, mas uma pessoa é responsável pelo código.

---

## 8. Segurança, privacidade e serviços externos

- Segredos nunca entram no Git, documentação, screenshots, logs ou prompts.
- PDFs, JSONs reais, `texto_integral`, `decisao_bruta`, vocabulários e artefactos que possam conter dados identificáveis não devem ser enviados para uma IA externa.
- Apenas exemplos sintéticos ou devidamente sanitizados podem ser usados em prompts.
- A explicação opcional produzida por LLM é texto gerado, não aconselhamento jurídico nem prova de explicabilidade do modelo PyTorch.
- A chave DeepSeek partilhada é gerida por Pedro, deve ter limites de utilização e deve ser revogada no final do projeto ou quando um membro sair.

---

## 9. Nomes descritivos em português

O código do JurisTriage deve usar nomes descritivos em português de Portugal. Esta regra aplica-se a classes, funções, métodos, variáveis, módulos, pastas, ficheiros de teste e chaves internas criadas pela equipa.

### 9.1 Formato dos identificadores

- Classes usam `PascalCase`: `DocumentoBruto`, `RegistoClassificacao`, `MotorInferencia`.
- Funções, métodos, variáveis, módulos e pastas usam `snake_case`: `carregar_pdfs`, `decisao_bruta`, `motor_inferencia.py`.
- Os identificadores não usam acentos, cedilhas, espaços ou hífenes.
- Funções começam por um verbo que descreve a ação: `limpar_texto`, `avaliar_execucao`, `guardar_manifesto`.
- Booleanos exprimem uma condição: `tem_sumario`, `modelo_carregado`, `categoria_reconhecida`.
- Coleções usam nomes no plural: `documentos_brutos`, `categorias_previstas`, `caminhos_artefactos`.

### 9.2 Clareza obrigatória

- São proibidas abreviaturas vagas como `doc`, `obj`, `tmp`, `res`, `val` e `data` quando existe um nome mais preciso.
- Não usar nomes genéricos como `processar`, `dados` ou `resultado` sem contexto suficiente.
- Variáveis matemáticas curtas, como `x`, `y` ou `i`, só são aceitáveis em fórmulas ou ciclos locais muito pequenos, quando o significado for evidente.
- O mesmo conceito deve ter o mesmo nome em todos os módulos.

### 9.3 Vocabulário oficial

| Conceito | Nome obrigatório |
|---|---|
| Documento acabado de carregar | `DocumentoBruto` |
| Acórdão estruturado | `Acordao` |
| Registo pronto para classificação | `RegistoClassificacao` |
| Decisão original | `decisao_bruta` |
| Texto completo | `texto_integral` |
| Categoria final | `categoria_normalizada` |
| Identificador de execução | `id_execucao` |
| Semente aleatória | `semente` |
| Manifesto da execução | `manifesto.json` |

### 9.4 Exceções

Mantêm-se os nomes oficiais impostos por bibliotecas, formatos, métricas e APIs externas, incluindo JSON, PDF, TF-IDF, NumPy, PyTorch, Jira, `state_dict`, `fit`, `transform`, Macro-F1 e os nomes de campos exigidos por serviços externos.

O guia `docs/convencoes_nomes.md` apresenta exemplos práticos, mas esta Constituição é a fonte normativa.

---

## 10. Políticas de comentários, limpeza e docstrings

O código deve ler-se facilmente. Os comentários justificam "Porquê" e nunca "O que é isto".

**Regras:**
- Adiciona *Docstrings* claras nas funções principais.
- Justifica decisões invulgares em comentários (e.g., heurísticas de parsing ou tratamento de excepções).
- Confirma que os nomes públicos cumprem a secção 9 antes de abrir um pedido de integração.
- TODOs devem incluir o ticket real: `# TODO[SCRUM-123]: Melhorar a extração do Tribunal`.
- Garante que os testes correm localmente (`python -m unittest discover -s tests -p "test_*.py" -v`) antes do PR.

## 11. Boas Práticas e Regras Adicionais

# Boas práticas de desenvolvimento

## 1. Tarefas pequenas

Cada tarefa deve ser pequena o suficiente para compreender, testar e rever. Não mistures correções sem relação no mesmo pedido de integração.

## 2. Ramos

Nunca trabalhes diretamente em `main`.

Formato:

```text
funcionalidade/<JIRA-KEY>-descricao-curta
correcao/<JIRA-KEY>-descricao-curta
documentacao/<JIRA-KEY>-descricao-curta
```

Exemplo, se o ticket for `SCRUM-123`:

```text
funcionalidade/SCRUM-123-carregador-pdf
```

Não inventes números de ticket. Usa a chave real apresentada pelo Jira.

## 3. Commits

Formato:

```text
[<JIRA-KEY>] Descrição curta
```

Bom:

```text
[SCRUM-123] Adicionar transformação TF-IDF com NumPy
```

Mau:

```text
update stuff
```

Antes do commit:

```bash
git status
git diff
```

Adiciona ficheiros de forma explícita:

```bash
git add src/caracteristicas/vetorizador_tfidf.py tests/test_vetorizador_tfidf.py
```

Evita `git add .`, porque pode incluir `.env`, dados, logs ou alterações de outra tarefa.

## 4. Pedidos de integração

Todo o pedido de integração deve incluir:

- ticket Jira;
- objetivo;
- ficheiros principais;
- testes executados;
- riscos conhecidos;
- indicação de apoio de IA;
- screenshots apenas quando relevantes e sem segredos.

Pedro revê os pedidos dos colegas. Como administrador e responsável técnico, Pedro pode validar os próprios pedidos, desde que documente os testes, riscos e decisão.

## 5. Checklist de revisão

- Segue a especificação?
- Preserva os contratos?
- Mantém a tarefa dentro do escopo?
- Usa type hints nas funções públicas?
- Inclui testes úteis?
- Todos os testes passam?
- Executou realmente testes, em vez de descobrir zero?
- Introduz segredos ou dados privados?
- Introduz fuga de informação?
- Adiciona dependências desnecessárias?
- O autor compreende o código?
- Os nomes são descritivos e seguem `docs/convencoes_nomes.md`?

## 6. Testes

Usa `unittest`.

Comando completo:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Cada módulo deve ter testes. Exemplos:

- `tests/test_carregador_pdf.py`
- `tests/test_analisador_metadados.py`
- `tests/test_limpeza_texto.py`
- `tests/test_construtor_registos.py`
- `tests/test_vetorizador_tfidf.py`
- `tests/test_rede_neuronal.py`
- `tests/test_treinar_modelo.py`
- `tests/test_metricas.py`
- `tests/test_manifesto.py`
- `tests/test_motor_inferencia.py`

Um teste deve provar comportamento, não apenas executar código sem erro.

## 7. Tipagem, docstrings e comentários

- Usa type hints em funções públicas.
- Usa docstrings nas classes e funções principais.
- Comentários explicam a razão de uma decisão.
- Usa nomes descritivos em português, conforme `docs/convencoes_nomes.md`.
- Evita abreviaturas vagas como `doc`, `obj`, `tmp`, `res`, `val` e `data`.

Bom:

```python
def analisar_documento_bruto(documento_bruto: DocumentoBruto) -> Acordao:
    ...
```

Mau:

```python
def parse(doc):
    ...
```

Bom:

```python
# Excluímos decisao_bruta para impedir que a resposta entre nas características.
```

Mau:

```python
# Incrementa i
i += 1
```

## 8. Segredos

Nunca commits:

- `.env`;
- chaves API;
- `auth.json`;
- tokens Jira;
- ficheiros `*.key`;
- emails privados desnecessários;
- caminhos pessoais;
- cópias integrais do conjunto de dados.

Se um segredo aparecer numa conversa, screenshot, log ou commit, considera-o exposto e revoga-o.

## 9. Dados e privacidade

Não commits nem envies a uma IA externa:

- PDFs reais;
- corpus JSON completo;
- `texto_integral`;
- `decisao_bruta`;
- dados pessoais;
- vocabulários ou artefactos identificáveis.

Usa dados sintéticos ou amostras sanitizadas.

## 10. Dependências

Ao adicionar uma dependência:

- justifica-a no PR;
- adiciona-a a `requirements.txt`;
- confirma compatibilidade com Python 3.11;
- evita dependências pesadas sem necessidade.

Scikit-learn só pode ser usado para métricas autorizadas, nunca para TF-IDF ou divisão dos dados.

## 11. Reprodutibilidade

Usa `semente = 42` nas divisões e inicializações. A semente ajuda, mas não garante resultados idênticos entre sistemas. Regista também versões, configuração, plataforma e opções determinísticas relevantes.

## 12. Artefactos MLOps

Não mistures artefactos de runs diferentes:

```text
artefactos/execucao_XXX/manifesto.json
```

A inferência recebe `id_execucao` e carrega todos os caminhos pelo manifesto. Não usa caminhos absolutos.

## 13. Fuga de informação

Características autorizadas:

- `descritores`;
- `sumario`.

Proibidos como input:

- `decisao_bruta`;
- texto dispositivo;
- ECLI;
- URL;
- `texto_integral`;
- qualquer campo derivado da resposta final.

O TF-IDF faz `fit` apenas no treino. Validação, teste e inferência usam `transform`.

## 14. Recuperação de erros Git

Não uses `git reset --hard`, `git checkout --` ou comandos encontrados ao acaso. Para conflitos ou alterações perdidas:

1. para;
2. executa `git status`;
3. copia a mensagem de erro sem incluir segredos;
4. pede ajuda ao Pedro;
5. regista o bloqueio no Jira.
