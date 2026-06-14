# Fluxo GitHub e Jira

Este guia assume pouca experiência prévia.

## 1. O papel de cada ferramenta

- **Jira:** diz o que deve ser feito, por quem e em que estado.
- **Git:** guarda o histórico local do código.
- **GitHub:** aloja o repositório e os Pull Requests.
- **Pull Request:** permite revisão antes de juntar código à `main`.

O Jira não substitui o GitHub. Cada ticket Jira deve apontar para uma branch e um PR.

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
2. lê a descrição e a spec ligada;
3. muda o estado para `In Progress` quando começares;
4. regista dúvidas no ticket;
5. usa a chave real, por exemplo `SCRUM-123`.

## 4. Criar a branch

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/SCRUM-123-descricao-curta
```

Se `git pull --ff-only` falhar, não forces. Executa `git status` e pede ajuda.

## 5. Trabalhar e testar

Trabalha apenas nos ficheiros da tua spec.

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

## 6. Publicar a branch

```bash
git push -u origin feature/SCRUM-123-descricao-curta
```

Abre o GitHub e cria um Pull Request para `main`.

## 7. Conteúdo do Pull Request

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

Pede revisão ao Pedro. Se o autor for Pedro, pede revisão a outro membro.

## 8. Depois da revisão

Se houver comentários:

1. não feches o PR;
2. faz as correções na mesma branch;
3. executa novamente os testes;
4. faz novo commit e `git push`;
5. responde aos comentários.

Depois do merge:

```bash
git switch main
git pull --ff-only origin main
git branch -d feature/SCRUM-123-descricao-curta
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
- não aprovar o próprio PR;
- impedir merge com testes falhados;
- manter contratos e arquitetura;
- ligar tickets aos PRs;
- evitar tarefas duplicadas.

## 11. Automação Jira

O script `create_jira_tasks.py` prepara as oito tarefas. Por segurança:

- usa a API Jira v3;
- não contém tokens;
- faz simulação por defeito;
- evita criar a mesma tarefa duas vezes;
- exige os `accountId` dos responsáveis para atribuição;
- só cria tarefas reais com `--apply`.

Os emails são necessários para convidar colegas que ainda não estão no Jira. Para atribuição pela API, o identificador mais fiável é o `accountId` Atlassian.
