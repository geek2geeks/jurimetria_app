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
