# Dados (data/)

O corpus completo (centenas de milhares de PDFs + JSONs, vários GB) **não é
versionado** (constituição §8, `RNF05`, `.gitignore`). Esta pasta contém apenas
a estrutura e, no máximo, uma amostra pequena e sanitizada.

## Estrutura esperada do corpus (local)

```text
<DATA_DIR>/
└── TRIBUNAL/            # STA, STJ, TRL, TRP, TRC, TRE, TRG, TCONS, ...
    └── ANO/
        ├── ECLI_PT_STJ_2024_xxxx.pdf
        └── ECLI_PT_STJ_2024_xxxx.json   # mesmo nome do PDF; source of truth
```

Cada PDF tem um JSON irmão com o **mesmo nome**, na mesma pasta. O JSON é a
*source of truth* da extração (ver [docs/esquema_json_corpus.md](../docs/esquema_json_corpus.md)).

## Configuração

1. Coloca o corpus localmente (fora do repositório).
2. Define o caminho no teu `.env` (não versionado):

   ```text
   DATA_DIR=D:/pdfs        # exemplo Windows; ajusta ao teu caminho
   ```

3. Para desenvolvimento, usa uma amostra pequena (`RNF07`: o fluxo deve correr
   numa amostra de ~10 documentos num computador modesto).

## O que pode e não pode ser versionado

- ✅ `data/sample/**/*.json` **sanitizado/sintético** (permitido pelo `.gitignore`).
- ❌ PDFs reais, JSONs reais com dados pessoais, `texto_integral`, `decisao_bruta`.
- ❌ Qualquer ficheiro com nomes de pessoas ou dados identificáveis.

Em exemplos para slides/README, anonimizar (ex.: "José Silvério" → "[Autor 1]").
