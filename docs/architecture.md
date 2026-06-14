# Arquitetura e Pipeline MLOps

O projeto JurisTriage adota uma arquitetura em cascata focada no encapsulamento de funções. O dado flui sistematicamente através de Contratos de Dados (Dataclasses) para manter o pipeline estável.

## 1. Contratos de Dados (Data Flow)
```text
[ Documentos no Disco (PDF / JSON cru) ]
       ↓
[ P1 ] Data Loaders (pdf_loader / json_raw_loader)
       ↓
[ Contrato Inicial: RawDocument ]
       ↓
[ P2 ] Metadata Parser (Recebe e converte em campos)
       (Ou json_acordao_loader para JSON estruturado)
       ↓
[ Contrato Central: Acordao (Estruturado, mas ainda com texto semi-bruto) ]
       ↓
[ P3 ] Cleaner + Label Normalizer (Remoção do ruído e normalização da decisão)
       ↓
[ P8 ] Dataset Builder (Aglomerador da Pipeline Principal)
       ↓
[ Contrato ML: DatasetRow (Texto limpo e Label final) ]
       ↓
[ P4 ] NumPy Vectorizer (Fit no Train / Transform no resto)
       ↓
[ P5 ] PyTorch Dataset/DataLoader & Training
```

## 2. A Gestão de Artefactos (Run Manifests)
A avaliação e inferência operam de forma isolada do modelo principal. Isto impede misturas de versões de modelos e vocabulários.

Após a finalização de cada treino (`run`), os diferentes módulos exportam os seus artefactos para uma diretoria rastreável:
```text
artifacts/run_001/
  ├── vectorizer/  (Gleicy P4 deposita o vocab.json, idf.npy, config.json)
  ├── labels/      (Gleicy P4 ou Pedro P8 depositam o id_to_label)
  ├── model/       (Helton P5 deposita o weights.pth e o model_config.json)
  ├── metrics.json (Luciana P6 deposita a macro-f1)
  └── manifest.json (Pedro P8 agrega todos os links num único documento)
```

**O Uso de JSONs como Fonte Alternativa:**
Para acelerar o desenvolvimento de Gustavo, Gleicy e Helton, os JSONs estruturados já fornecidos funcionam como entrada direta no adaptador (JSON -> `Acordao`). Isto permite que o pipeline avance de forma assíncrona enquanto o parser de PDF cru é afinado.
