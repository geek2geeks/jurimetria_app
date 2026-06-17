# Entrega P7 — MotorInferencia

**Autor:** Sandro Tarabay
**Data:** 2026-06-15
**Versão:** 1.3
**Domínio:** D07 — Inferência e explicação (SCRUM-11)
**Fase:** 1 (entrega) — inclui a vertente *Could Have* (LLM) e exibição de métricas do treino (P6)

## Propósito

Dado um `id_execucao` e um `Acordao`, prever uma de cinco categorias
(`MANTIDA`, `REVOGADA`, `ANULADA`, `NAO_CONHECIDA`, `OUTRA`) reconstruindo o
vetorizador e o modelo pelo `manifesto.json`, usando a mesma composição de
entrada do treino (sem train/serve skew). Explicação opcional, offline ou via
LLM remoto, sempre marcada como "não constitui aconselhamento jurídico".

## Diagrama macro — posicionamento no projecto

```mermaid
flowchart LR
    subgraph TREINO["TREINO — corre uma vez, orquestrado por P8 (Pedro)"]
        direction TB
        P1["P1 · Alessandro<br/>ingestão PDF/JSON"]
        P2T["P2 · Daniela<br/>analisar_documento_bruto"]
        P3T["P3 · Gustavo<br/>limpar_texto<br/>normalizar_categoria"]
        P4T["P4 · Gleicy<br/>ajustar TF-IDF<br/>dividir treino/teste"]
        P5T["P5 · Helton<br/>treinar MLP"]
        P6T["P6 · Luciana<br/>avaliar_execucao"]
        P1 --> P2T --> P3T --> P4T --> P5T --> P6T
    end

    subgraph ART["artefactos/execucao_001/ — produto do treino"]
        direction TB
        MANIF["manifesto.json<br/>(índice de tudo)"]
        VOCAB["vetorizador/<br/>vocabulario.json + idf.npy"]
        CATS["categorias/<br/>id_para_categoria.json"]
        MODELO["modelo/<br/>pesos.pth + configuracao.json"]
        METR["metricas.json<br/>(Macro-F1, baseline)"]
    end

    P6T -->|escreve| ART

    subgraph P7["O MEU MÓDULO (P7) — Inferência"]
        direction TB
        CLI["executar_inferencia.py<br/>(CLI) ou API directa"]
        MOTOR["MotorInferencia.__init__"]
        PREVER["MotorInferencia.prever(acordao)"]
        FORMAT["formatador_saida.py<br/>texto / markdown / json<br/>(opcional: LLM remoto)"]
        SAIDA["stdout"]

        CLI --> MOTOR --> PREVER --> FORMAT --> SAIDA
    end

    P2N["Acordao novo<br/>(produzido pelo P2)"] --> CLI

    MANIF -.->|lê| MOTOR
    VOCAB -.->|carrega| MOTOR
    CATS -.->|lê| MOTOR
    MODELO -.->|load_state_dict| MOTOR
    METR -.->|exibe| FORMAT

    style P7 fill:#e8f4f8,stroke:#2c7da0,stroke-width:2px
    style TREINO fill:#fafafa,stroke:#888
    style ART fill:#fff4e6,stroke:#cc7700
```

## Diagrama micro — fluxo interno

```mermaid
flowchart TD
    A["Acordao recebido<br/>(do P2)"] --> B["texto_caracteristicas<br/>= descritores + sumário<br/>(sem campos de fuga)"]
    B --> C["limpar_texto<br/>P3 · Gustavo"]
    C --> D["VetorizadorTfidfNumPy.transformar<br/>P4 · Gleicy<br/>(tf × idf, normalização L2)"]
    D --> E["ClassificadorMLP.forward<br/>P5 · Helton<br/>(em modo eval, sem grad)"]
    E --> F["torch.softmax<br/>(probabilidades)"]
    F --> G["np.argmax<br/>(índice da classe)"]
    G --> H["id_para_categoria<br/>(P8, do manifesto)"]
    H --> I["ResultadoInferencia<br/>· categoria<br/>· distribuição<br/>· termos relevantes"]
    I --> J{"EXPLICACAO_VIA_LLM<br/>no .env?"}
    J -->|false| K["explicar_offline<br/>(top-5 termos TF-IDF)"]
    J -->|true| L["POST OpenRouter<br/>(DeepSeek)"]
    L -->|falha rede/chave| K
    L -->|sucesso| M["Formatador<br/>texto / markdown / json"]
    K --> M
    M --> N["stdout"]

    style A fill:#fff4e6,stroke:#cc7700
    style I fill:#e8f4f8,stroke:#2c7da0
    style N fill:#e8f4f8,stroke:#2c7da0
    style J fill:#fefcbf,stroke:#b7791f
```

## Contratos

**Construtor:** `MotorInferencia(id_execucao: str, pasta_artefactos: str | Path = "artefactos")`

**Método:** `.prever(acordao: Acordao, com_explicacao: bool = False) -> ResultadoInferencia`

**Resultado:**

```python
@dataclass
class ResultadoInferencia:
    categoria_prevista: str        # uma das 5 classes ADR-05
    indice_previsto: int           # 0–4
    distribuicao: dict[str, float] # softmax; soma ≈ 1
    termos_relevantes: list[str]   # top-5 por peso TF-IDF
    excerto_sumario: str           # ≤ 400 caracteres
    explicacao_gerada: str | None
```

## Dependências de outros módulos

| Origem | Como é consumido |
|---|---|
| P2 · `Acordao` | Recebido como parâmetro — quem chama é responsável pela origem |
| P3 · `limpar_texto` | Import directo |
| P4 · `VetorizadorTfidfNumPy` | Import directo + `.carregar()` do disco |
| P5 · `ClassificadorMLP` | Import directo + `state_dict` |
| P8 · `manifesto.json` | `ler_manifesto(id_execucao, pasta_artefactos)` |
| P6 · `metricas.json` | Leitura passiva do JSON; sem chamada a funções |

## Ficheiros a integrar (PR para o repo da equipa)

```
src/inferencia/
├── motor_inferencia.py
├── executar_inferencia.py
├── formatador_saida.py
└── configuracao_gpu.py

tests/
├── test_motor_inferencia.py
├── test_executar_inferencia.py
└── test_formatador_saida.py

docs/
└── entrega_p7_inferencia.md
```

## Comandos

```bash
# Instalação
pip install -e .
cp .env.exemplo .env       # ajustar ID_EXECUCAO e chaves opcionais

# Testes
python -m unittest discover -s tests -p "test_*.py"

# Inferência (ficheiro único)
python -m src.inferencia.executar_inferencia \
    --ficheiro-json data/ECLI_PT_STA_1950_000578_FF.json

# Inferência (pasta inteira)
python -m src.inferencia.executar_inferencia --pasta-dados data/

# Layout / LLM por variável de ambiente
FORMATO_SAIDA=markdown python -m src.inferencia.executar_inferencia ...
EXPLICACAO_VIA_LLM=true python -m src.inferencia.executar_inferencia ...
```

## Variáveis `.env`

| Variável | Default | Função |
|---|---|---|
| `ID_EXECUCAO` | `execucao_teste` | Subpasta de `artefactos/` a carregar |
| `PASTA_ARTEFACTOS` | `artefactos` | Pasta-mãe das execuções |
| `PASTA_DADOS` | `data` | Pasta com os JSONs a inferir |
| `FORMATO_SAIDA` | `texto` | `texto` / `markdown` / `json` |
| `EXPLICACAO_VIA_LLM` | `false` | Activa LLM remoto (Could Have) |
| `DEEPSEEK_URL_BASE` | `https://openrouter.ai` | Endpoint OpenRouter |
| `DEEPSEEK_MODELO` | `deepseek/deepseek-v4-flash` | Modelo OpenRouter |
| `DEEPSEEK_CHAVE_API` | — | Chave; **nunca commitar** |
| `LLM_TEMPO_LIMITE_SEGUNDOS` | `20` | Timeout do LLM |
| `GPU_HABILITADA` | `false` | Activa GPU NVIDIA |
| `GPU_NUM_DISPOSITIVOS` | `1` | 1, 2 ou 3 |
| `GPU_DISPOSITIVOS` | `auto` | `auto` / `"0"` / `"0,1"` / `"0,1,2"` |

## Pedido ao integrador (P8 — Pedro)

**`requirements.txt`** — acrescentar:

```
requests>=2.31.0    # P7 — LLM opcional (Could Have)
```

**`.env.exemplo`** — acrescentar as 12 variáveis da tabela acima.

**`pyproject.toml`** — opcional, para entry-points:

```toml
[project.scripts]
jurimetria-inferir = "src.inferencia.executar_inferencia:principal"
```

## Garantias verificadas

- **Anti-leakage** (teste programático): dois `Acordao` com mesmos descritores+sumário mas `ecli`/`tribunal`/`decisao_bruta`/`texto_integral` distintos produzem a mesma previsão.
- **Determinismo**: mesmo input → mesmo output; `semente=42`.
- **LLM offline-first** (ADR-03): desligado por defeito; sem chave cai para offline; nunca envia campos de fuga.
- **TF-IDF em NumPy** (ADR-01): zero `sklearn` na vetorização.
- **Multi-GPU** opcional (1/2/3) via `.env`; defaults para CPU.
- **`pyproject.toml`** com `setuptools.build_meta` (compatível com setuptools ≥ 40).

## Limitações

- Modelo do scaffolding **não treinado** (pesos aleatórios) — valida canalização, não qualidade. Substituído pela execução real do P5/P8.
- `limpar_texto` da entrega é versão base; no repo da equipa o P7 usa a versão canónica do P3 (mesmo path, sem alteração de código).
- LLM sem chave → cai para offline silenciosamente.
- Para inferência, `DataParallel` em 3 GPUs traz overhead; recomendado 1 GPU. Para treino (Fase 2), considerar `DistributedDataParallel`.

## Checklist

- [x] Nomes em `snake_case`/`PascalCase` (pt-PT)
- [x] Type hints completos; `mypy --strict` limpo
- [x] `ruff` limpo
- [x] Ausência de data leakage testada
- [x] Carregamento exclusivamente pelo `manifesto.json`
- [x] `semente=42`; `logging` em vez de `print`
- [x] 56 testes; só dados sintéticos
- [x] LLM offline-first; fallback silencioso
- [x] Multi-GPU opcional
- [x] Exibição informativa das métricas (P6) — leitura passiva
- [x] `pyproject.toml` válido; entry-points registados
