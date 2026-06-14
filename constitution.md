# JurisTriage PT — Constituição do Projeto

**Versão:** 2.4
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
| Alessandro | P1 — Ingestão de dados / Data Loader |
| Daniela | P2 — Parsing posicional de metadados |
| Gustavo | P3 — Limpeza textual e normalização de labels |
| Gleicy | P4 — Vetorização NumPy e split dos dados |
| Helton | P5 — Modelo PyTorch e treino |
| Luciana | P6 — Baseline, métricas e avaliação |
| Sandro | P7 — Inferência e explicação opcional |
| Pedro | P8 — Tech Lead, QA, requisitos, arquitetura, Jira e GitHub |

---

## 2. Escopo Obrigatório vs Opcional

| Escopo | Itens |
|---|---|
| **Must Have** | Carregamento de PDFs/JSON, parsing estrito, limpeza, vetorização NumPy, modelo PyTorch, baseline, avaliação, inferência isolada, testes e documentação. |
| **Could Have** | Explicação textual via LLM/DeepSeek. |

---

## 3. Contratos de Dados Internos (Schemas)

Para garantir a coesão da equipa, evitamos usar dicionários genéricos. O projeto assenta em 3 contratos principais (`src/data/schemas.py`), co-mantidos pelo Pedro e pela Daniela:

1. **`RawDocument`**: Representa um documento bruto acabado de ser carregado (PDF ou JSON cru). Usado antes do parsing.
2. **`Acordao`**: O contrato central. Representa o acórdão estruturado (com ecli, sumario, decisao_raw, etc). Independentemente de a fonte ser PDF ou JSON, a partir do P2, todo o projeto consome estritamente o `Acordao`. *Nota:* O texto aqui é estruturado, mas ainda pode conter formatação crua.
3. **`DatasetRow`**: A linha pronta para Machine Learning, contendo o texto final limpo (input) e a label normalizada.

---

## 4. Gestão de Artefactos MLOps e Manifest

Qualquer treino do modelo (`run`) gera resíduos (pesos e vocabulários) que têm de ser alinhados.
Cada treino deve gerar uma subpasta no diretório `artifacts/`.

**Estrutura Recomendada:**
```text
artifacts/
└── run_001/
    ├── vectorizer/
    │   ├── vocab.json
    │   ├── idf.npy
    │   └── config.json
    ├── labels/
    │   ├── label_to_id.json
    │   └── id_to_label.json
    ├── model/
    │   ├── model_config.json
    │   └── weights.pth
    ├── metrics.json
    └── manifest.json
```

**Regras de Arquitetura MLOps:**
1. A Inferência (P7) nunca deve carregar ficheiros soltos manualmente. Deve pedir o `run_id` e usar o respetivo `manifest.json` para carregar tudo em sincronia.
2. O Modelo PyTorch (P5) deve ser gravado estritamente com `state_dict()` em `weights.pth`. A arquitetura base fica em `model_config.json`.
3. O Vetorizador TF-IDF (P4) só pode efetuar o `fit` no conjunto de treino (`X_train`). Validação, teste e inferência usam apenas `transform()`.

---

## 5. Regras sobre PDFs, JSONs e Data Leakage

- O parser deve ser tolerante a campos ausentes (usando `None`).
- A `decisao_raw`, o texto dispositivo, ECLI, URL e qualquer trecho de `full_text` que revele a decisão NUNCA entram na matriz explicativa (X).
- As únicas fontes de texto autorizadas para X são `descritores` e `sumario`, depois da limpeza definida pelo P3.
- O papel do JSON é ser uma fonte alternativa e aceleradora. Regra:
  - JSON cru -> `RawDocument` -> `metadata_parser` -> `Acordao`
  - JSON estruturado -> `json_acordao_loader` (adapter) -> `Acordao`

---

## 6. Classes de decisão

As cinco classes iniciais, aprovadas pelo Pedro como responsável técnico, são:

1. `MANTIDA`
2. `REVOGADA`
3. `ANULADA`
4. `NAO_CONHECIDA`
5. `OUTRA`

O dicionário que converte expressões jurídicas para estas classes deve ser revisto pelo Pedro. Casos ambíguos não devem ser adivinhados: ficam sem label ou são encaminhados para revisão.

---

## 7. Desenvolvimento assistido por IA e revisão humana

O professor aprovou a equipa de oito pessoas, mas não concedeu uma autorização específica para código gerado por IA. Cada aluno deve respeitar as regras da disciplina e, em caso de dúvida, confirmar com o professor.

Se um membro usar IA para programar:

- deve seguir o fluxo SDD descrito em `docs/ai_development_workflow.md`;
- deve tratar toda a resposta da IA como rascunho;
- deve ler e compreender cada alteração;
- deve executar os testes;
- deve declarar o uso de IA no Pull Request;
- deve obter revisão humana antes do merge.

Pedro é o revisor obrigatório dos Pull Requests dos restantes membros. Um PR criado pelo próprio Pedro deve ter outro membro humano como revisor; autoaprovação não conta como revisão.

Ferramentas recomendadas, mas não obrigatórias:

- GitHub Spec Kit `v0.10.2`;
- OpenCode `>=1.14.24`;
- DeepSeek V4 Pro;
- Anaconda/conda com Python 3.11.

Nenhuma IA pode inventar contratos, alterar `RawDocument`, `Acordao` ou `DatasetRow` sem aprovação de Pedro e Daniela, contornar testes ou efetuar merge direto em `main`.

> A IA pode escrever código, mas uma pessoa é responsável pelo código.

---

## 8. Segurança, privacidade e serviços externos

- Segredos nunca entram no Git, documentação, screenshots, logs ou prompts.
- PDFs, JSONs reais, `full_text`, `decisao_raw`, vocabulários e artefactos que possam conter dados identificáveis não devem ser enviados para uma IA externa.
- Apenas exemplos sintéticos ou devidamente sanitizados podem ser usados em prompts.
- A explicação opcional produzida por LLM é texto gerado, não aconselhamento jurídico nem prova de explicabilidade do modelo PyTorch.
- A chave DeepSeek partilhada é gerida por Pedro, deve ter limites de utilização e deve ser revogada no final do projeto ou quando um membro sair.

---

## 9. Políticas de Comentários, Limpeza e Docstrings

O código deve ler-se facilmente. Os comentários justificam "Porquê" e nunca "O que é isto".

**Regras:**
- Adiciona *Docstrings* claras nas funções principais.
- Justifica decisões invulgares em comentários (e.g., heurísticas de parsing ou tratamento de excepções).
- TODOs devem incluir o ticket real: `# TODO[SCRUM-123]: Melhorar a extração do Tribunal`.
- Garante que os testes correm localmente (`python -m unittest discover -s tests -p "test_*.py" -v`) antes do PR.
