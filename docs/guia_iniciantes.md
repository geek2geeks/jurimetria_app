# Guia para iniciantes

Não precisas de conhecer todo o projeto. Precisas de compreender a tua tarefa, respeitar as entradas e saídas e pedir revisão quando tiveres dúvidas.

## 1. Ordem de leitura

1. `constitution.md`
2. `docs/instalacao_software.md`
3. `docs/fluxo_github_jira.md`
4. `docs/boas_praticas_desenvolvimento.md`
5. `docs/guias_individuais/README.md`
6. o teu guia individual;
7. a tua especificação em `docs/especificacoes/`;
8. o teu ticket Jira.

## 2. Glossário

- **Repositório:** pasta do projeto guardada pelo Git.
- **GitHub:** serviço onde está a cópia partilhada do repositório.
- **Jira:** quadro de tarefas, responsáveis e estados.
- **Ramo (*branch*):** linha de trabalho isolada para uma tarefa.
- **Commit:** registo de um conjunto pequeno de alterações.
- **Push:** envio dos commits para o GitHub.
- **Pedido de integração (*pull request*):** pedido para rever e integrar um ramo na `main`.
- **Review:** leitura crítica feita por outra pessoa.
- **Integração contínua (CI):** testes automáticos executados pelo GitHub.
- **Spec:** contrato escrito da tarefa.

## 3. Preparar o computador

Segue `docs/instalacao_software.md`. A configuração padrão é:

```bash
conda create -n juristriage python=3.11 -y
conda activate juristriage
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m unittest discover -s tests -p "test_*.py" -v
```

Confirma que o Git tem o teu nome e email reais:

```bash
git config --global user.name "Nome Apelido"
git config --global user.email "email-usado-no-github"
```

## 4. Começar uma tarefa

1. Abre o ticket Jira.
2. Lê a especificação ligada.
3. Confirma as dependências.
4. Muda o ticket para `In Progress`.
5. Atualiza a `main`.
6. Cria um ramo com a chave real do Jira.

```bash
git switch main
git pull --ff-only origin main
git switch -c funcionalidade/SCRUM-123-descricao-curta
```

`SCRUM-123` é apenas um exemplo. Usa a chave do teu ticket.

## 5. Trabalhar sem perder alterações

Consulta frequentemente:

```bash
git status
git diff
```

Antes do commit:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
git add caminho/do/ficheiro.py tests/test_ficheiro.py
git commit -m "[SCRUM-123] Descrição curta"
```

Não uses `git add .` sem rever cada ficheiro. Não uses `git reset --hard` nem apagues alterações para resolver um conflito.

## 6. Abrir um pedido de integração

```bash
git push -u origin funcionalidade/SCRUM-123-descricao-curta
```

No GitHub:

1. abre um pedido de integração para `main`;
2. liga o ticket Jira;
3. descreve as alterações;
4. indica os testes;
5. declara se usaste IA;
6. pede revisão ao Pedro.

Se Pedro for o autor, pode validar o próprio PR como administrador, deixando os testes e a decisão registados.

## 7. Usar IA

O professor aprovou a equipa, mas não deu uma autorização específica para código gerado por IA. Confirma as regras académicas aplicáveis.

Se usares IA:

- tu continuas responsável pelo código;
- não envies documentos jurídicos reais, dados pessoais ou chaves;
- pede primeiro explicação e plano;
- usa o fluxo do Spec Kit;
- lê todo o diff;
- executa os testes;
- declara o uso no PR.

Fluxo:

```text
/speckit.clarify
-> revisão humana
-> /speckit.plan
-> /speckit.tasks
-> /speckit.analyze
-> aprovação
-> /speckit.implement
-> testes
-> pedido de integração
-> revisão humana
```

Consulta `docs/fluxo_desenvolvimento_ia.md`.

## 8. Pedir ajuda

Quando algo falhar:

1. para antes de executar comandos destrutivos;
2. copia a mensagem de erro sem segredos;
3. executa `git status`;
4. coloca o ticket em `Blocked`;
5. explica o que tentaste;
6. pede ajuda ao Pedro ou ao responsável da dependência.

Um bloqueio bem descrito é melhor do que esconder um problema.

## 9. Definição de pronto

A tarefa está pronta quando:

- cumpre a especificação;
- tem testes;
- os testes passam;
- não contém segredos ou dados reais;
- o PR declara o uso de IA;
- Pedro ou outro revisor aplicável aprovou;
- o PR foi ligado ao Jira;
- o ticket foi movido para `Done` depois da integração.
