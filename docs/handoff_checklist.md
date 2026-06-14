# Checklist de Entrega à Equipa (Handoff)

Documento de apoio à auditoria ([team_handoff_readiness_audit.md](team_handoff_readiness_audit.md)). Marca cada item antes de anunciar o arranque aos 8 colegas.

## Bloqueante (fechar antes de entregar)

- [ ] **`src/dados/esquemas.py` criado e commitado** com as 3 dataclasses e todos os campos/tipos:
  - [ ] `DocumentoBruto(nome_ficheiro, caminho, texto, numero_paginas, origem)`
  - [ ] `Acordao(ecli, tribunal, ano, relator, numero_documento, data_acordao, meio_processual, decisao_bruta, descritores, sumario, texto_integral, origem)`
  - [ ] `RegistoClassificacao(id_documento, texto, categoria_normalizada, tribunal, ano)`
- [ ] **Entrada da inferência decidida** (descritores+sumário = treino) e refletida em `requisitos.md` RF11, `especificacao_07` e guia do Sandro.
- [ ] **Dicionário decisão→classe aprovado pelo Pedro** e partilhado com o Gustavo (P3).

## Acessos e ambiente

- [ ] Os 8 membros têm acesso de escrita ao GitHub `geek2geeks/jurimetria_app`.
- [ ] Os 8 membros têm acesso ao projeto Jira `SCRUM` e veem o seu ticket (`SCRUM-5`..`SCRUM-12`).
- [ ] Token Jira exposto anteriormente foi **revogado** e substituído.
- [ ] Chave DeepSeek partilhada tem limite de custo e plano de rotação/revogação.
- [ ] GitHub Actions a correr (sem bloqueio de faturação) — confirmar 1 PR verde.
- [ ] Cada membro corre o diagnóstico de `instalacao_software.md` §8 e obtém Python 3.11.

## Qualidade e segurança

- [ ] `python -m unittest discover -s tests -p "test_*.py" -v` passa localmente.
- [ ] `.gitignore` protege `.env`, segredos, dados e `artefactos/execucao_*`.
- [ ] `.env.example` só contém placeholders (sem chaves reais).
- [ ] Link do dataset (Drive) revisto quanto a privacidade/RGPD.
- [ ] Nenhum dado jurídico real ou PDF está versionado.

## Importante (logo a seguir)

- [ ] `docs/criterios_avaliacao.md` (mapa deliverable → peso da nota → pessoa).
- [ ] Requisito "comparar ≥2 configurações" acrescentado a `requisitos.md` e à spec do P5.
- [ ] `config.json` → `configuracao.json` uniformizado (guia P4).
- [ ] `requirements.txt` limpo (`PyPDF2` e `tqdm` justificados ou removidos).
- [ ] Relatórios antigos marcados como históricos.

## Primeiro dia da equipa (sugestão de ordem)

1. Pedro + Daniela publicam `esquemas.py` e anunciam-no como contrato congelado.
2. Cada pessoa: lê constituição → seu guia → sua spec → abre o ticket Jira.
3. Cada pessoa cria a sua branch `funcionalidade/SCRUM-XX-...` e começa com mocks.
4. Primeiro PR de cada um: esqueleto + 1 teste mínimo a passar.
