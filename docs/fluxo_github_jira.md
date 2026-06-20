# Fluxo GitHub e Jira

Este guia assume pouca experiência prévia.

## 1. O papel de cada ferramenta

- **Jira:** diz o que deve ser feito, por quem e em que estado.
- **Git:** guarda o histórico local do código.
- **GitHub:** aloja o repositório e os pedidos de integração (*pull requests*).
- **Pedido de integração (*pull request*):** permite revisão antes de integrar código na `main`.

O Jira não substitui o GitHub. Cada ticket Jira deve apontar para um ramo e um pedido de integração.

## 2. Preparação da conta

Cada membro precisa de:

- conta GitHub;
- acesso de escrita ao repositório;
- conta Atlassian/Jira;
- acesso ao projeto Jira;
- nome e email corretos configurados no Git.

Configuração Git:

```bash
git config --global user.name "Nome Apelido"
git config --global user.email "email-usado-no-github"
```

Nunca uses `user@example.com`.

## 3. Receber uma tarefa

No Jira:

1. abre o ticket atribuído;
2. lê a descrição e a especificação ligada;
3. muda o estado para `In Progress` quando começares;
4. regista dúvidas no ticket;
5. usa a chave real, por exemplo `SCRUM-123`.

## 4. Criar o ramo

```bash
git switch main
git pull --ff-only origin main
git switch -c funcionalidade/SCRUM-123-descricao-curta
```

Se `git pull --ff-only` falhar, não forces. Executa `git status` e pede ajuda.

## 5. Trabalhar e testar

Trabalha apenas nos ficheiros da tua especificação.

Antes de cada commit:

```bash
git status
git diff
python -m unittest discover -s tests -p "test_*.py" -v
```

Adiciona os ficheiros explicitamente:

```bash
git add caminho/do/ficheiro.py tests/test_ficheiro.py
git commit -m "[SCRUM-123] Descrição curta"
```

## 6. Publicar o ramo

```bash
git push -u origin funcionalidade/SCRUM-123-descricao-curta
```

Abre o GitHub e cria um pedido de integração para `main`.

## 7. Conteúdo do pedido de integração

```text
## Ticket Jira
SCRUM-123

## Objetivo
Descrição curta.

## Alterações
- ...

## Testes
python -m unittest discover -s tests -p "test_*.py" -v

## Apoio de IA
Sim/Não.
Ferramenta e utilização, se aplicável.

## Riscos ou dúvidas
- ...
```

Pede revisão ao Pedro. Se o autor for Pedro, ele pode validar o próprio PR como administrador, documentando os testes e a decisão.

## 8. Depois da revisão

Se houver comentários:

1. não feches o PR;
2. faz as correções no mesmo ramo;
3. executa novamente os testes;
4. faz novo commit e `git push`;
5. responde aos comentários.

Depois da integração:

```bash
git switch main
git pull --ff-only origin main
git branch -d funcionalidade/SCRUM-123-descricao-curta
```

Move o ticket Jira para `Done` e adiciona o link do PR.

## 9. Estados Jira recomendados

```text
To Do -> In Progress -> In Review -> Done
                     -> Blocked
```

Usa `Blocked` quando precisares de uma decisão, acesso ou entrega de outro membro. Explica o bloqueio no ticket.

## 10. Regras para Pedro

- confirmar responsáveis e dependências no Jira;
- rever todos os PRs dos colegas;
- documentar explicitamente testes, riscos e decisão quando validar o próprio PR;
- impedir a integração quando os testes falham;
- manter contratos e arquitetura;
- ligar tickets aos PRs;
- evitar tarefas duplicadas.

## 11. Automação Jira

O script `criar_tarefas_jira.py` prepara as oito tarefas. Por segurança:

- usa a API Jira v3;
- não contém tokens;
- faz simulação por defeito;
- evita criar a mesma tarefa duas vezes;
- exige os `accountId` dos responsáveis para atribuição;
- só cria tarefas reais com `--apply`.

Os emails são necessários para convidar colegas que ainda não estão no Jira. Para atribuição pela API, o identificador mais fiável é o `accountId` Atlassian.

Fluxo recomendado:

1. Revoga o token exposto e cria um token novo.
2. Copia `.env.example` para `.env` e preenche apenas localmente.
3. Copia `membros_jira.exemplo.json` para `membros_jira.json`.
4. Substitui os exemplos pelos emails usados nas contas Atlassian.
5. Resolve os IDs:

```bash
python criar_tarefas_jira.py --resolver-responsaveis
```

6. Confirma a simulação:

```bash
python criar_tarefas_jira.py
```

7. Cria e atribui:

```bash
python criar_tarefas_jira.py --aplicar
```

`membros_jira.json` e `responsaveis_jira.json` são locais e estão ignorados pelo Git.

## Guia para Iniciantes (Resumo)

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
