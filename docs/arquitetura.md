# Arquitetura e fluxo MLOps

O JurisTriage adota uma arquitetura em cascata com contratos tipados. Os nomes do código seguem `docs/convencoes_nomes.md`.

## 1. Fluxo de dados

```text
[ Documentos no disco (PDF / JSON em bruto) ]
       ↓
[ P1 ] Carregadores (carregador_pdf / carregador_json_bruto)
       ↓
[ Contrato inicial: DocumentoBruto ]
       ↓
[ P2 ] Analisador de metadados
       (ou carregador_acordaos_json para JSON estruturado)
       ↓
[ Contrato central: Acordao ]
       ↓
[ P3 ] Limpeza do texto e normalização da categoria
       ↓
[ P8 ] Construtor dos registos de classificação
       ↓
[ Contrato de aprendizagem: RegistoClassificacao ]
       ↓
[ P4 ] Vetorizador TF-IDF com NumPy
       ↓
[ P5 ] Rede neuronal e treino com PyTorch
```

## 2. Gestão de artefactos

A avaliação e a inferência usam os artefactos de uma execução específica, evitando misturas entre modelos e vocabulários.

```text
artefactos/execucao_001/
  ├── vetorizador/
  │   ├── vocabulario.json
  │   ├── idf.npy
  │   └── configuracao.json
  ├── categorias/
  │   ├── categoria_para_id.json
  │   └── id_para_categoria.json
  ├── modelo/
  │   ├── pesos.pth
  │   └── configuracao_modelo.json
  ├── metricas.json
  └── manifesto.json
```

Os JSONs estruturados podem entrar diretamente pelo adaptador `carregador_acordaos_json`, permitindo que a equipa avance enquanto o analisador dos PDFs em bruto é afinado.
