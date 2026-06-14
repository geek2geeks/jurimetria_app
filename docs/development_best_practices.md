# Boas práticas de desenvolvimento

## 1. Tarefas pequenas

Cada tarefa deve ser pequena o suficiente para compreender, testar e rever. Não mistures correções sem relação no mesmo Pull Request.

## 2. Branches

Nunca trabalhes diretamente em `main`.

Formato:

```text
feature/<JIRA-KEY>-descricao-curta
fix/<JIRA-KEY>-descricao-curta
docs/<JIRA-KEY>-descricao-curta
```

Exemplo, se o ticket for `SCRUM-123`:

```text
feature/SCRUM-123-loader-pdf
```

Não inventes números de ticket. Usa a chave real apresentada pelo Jira.

## 3. Commits

Formato:

```text
[<JIRA-KEY>] Descrição curta
```

Bom:

```text
[SCRUM-123] Add NumPy TF-IDF transform method
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
git add src/features/vectorizer.py tests/test_numpy.py
```

Evita `git add .`, porque pode incluir `.env`, dados, logs ou alterações de outra tarefa.

## 4. Pull Requests

Todo PR deve incluir:

- ticket Jira;
- objetivo;
- ficheiros principais;
- testes executados;
- riscos conhecidos;
- indicação de apoio de IA;
- screenshots apenas quando relevantes e sem segredos.

Pedro revê os PRs dos colegas. Como administrador e responsável técnico, Pedro pode validar os próprios PRs, desde que documente os testes, riscos e decisão.

## 5. Checklist de revisão

- Segue a spec?
- Preserva os contratos?
- Mantém a tarefa dentro do escopo?
- Usa type hints nas funções públicas?
- Inclui testes úteis?
- Todos os testes passam?
- Executou realmente testes, em vez de descobrir zero?
- Introduz segredos ou dados privados?
- Introduz data leakage?
- Adiciona dependências desnecessárias?
- O autor compreende o código?

## 6. Testes

Usa `unittest`.

Comando completo:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Cada módulo deve ter testes. Exemplos:

- `tests/test_loader.py`
- `tests/test_parser.py`
- `tests/test_cleaner.py`
- `tests/test_dataset_builder.py`
- `tests/test_numpy.py`
- `tests/test_pytorch.py`
- `tests/test_training.py`
- `tests/test_evaluation.py`
- `tests/test_manifest.py`
- `tests/test_inference.py`

Um teste deve provar comportamento, não apenas executar código sem erro.

## 7. Tipagem, docstrings e comentários

- Usa type hints em funções públicas.
- Usa docstrings nas classes e funções principais.
- Comentários explicam a razão de uma decisão.

Bom:

```python
# Excluímos decisao_raw para impedir que a resposta entre nas features.
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
- dumps do dataset.

Se um segredo aparecer numa conversa, screenshot, log ou commit, considera-o exposto e revoga-o.

## 9. Dados e privacidade

Não commits nem envies a uma IA externa:

- PDFs reais;
- corpus JSON completo;
- `full_text`;
- `decisao_raw`;
- dados pessoais;
- vocabulários ou artefactos identificáveis.

Usa dados sintéticos ou amostras sanitizadas.

## 10. Dependências

Ao adicionar uma dependência:

- justifica-a no PR;
- adiciona-a a `requirements.txt`;
- confirma compatibilidade com Python 3.11;
- evita dependências pesadas sem necessidade.

Scikit-learn só pode ser usado para métricas autorizadas, nunca para TF-IDF ou split.

## 11. Reprodutibilidade

Usa seed 42 nos splits e inicializações. A seed ajuda, mas não garante resultados idênticos entre sistemas. Regista também versões, configuração, plataforma e opções determinísticas relevantes.

## 12. Artefactos MLOps

Não mistures artefactos de runs diferentes:

```text
artifacts/run_XXX/manifest.json
```

A inferência recebe `run_id` e carrega todos os caminhos pelo manifesto. Não usa caminhos absolutos.

## 13. Data leakage

Features autorizadas:

- `descritores`;
- `sumario`.

Proibidos como input:

- `decisao_raw`;
- texto dispositivo;
- ECLI;
- URL;
- `full_text`;
- qualquer campo derivado da resposta final.

O TF-IDF faz `fit` apenas no treino. Validação, teste e inferência usam `transform`.

## 14. Recuperação de erros Git

Não uses `git reset --hard`, `git checkout --` ou comandos encontrados ao acaso. Para conflitos ou alterações perdidas:

1. para;
2. executa `git status`;
3. copia a mensagem de erro sem incluir segredos;
4. pede ajuda ao Pedro;
5. regista o bloqueio no Jira.
