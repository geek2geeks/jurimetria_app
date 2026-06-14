# JurisTriage PT — Guia Rápido de Arranque (Quickstart)

**Para toda a equipa — inclusive quem não é da área de software.**
Este guia diz-te, em poucas páginas: o que instalar, onde começar, e como pedir ajuda.

> **Não percas tempo a decorar tudo.** Precisas só de perceber a TUA parte. Se ficares preso em qualquer ponto, **contacta o Pedro** (líder técnico) no grupo de WhatsApp / canal da equipa. Não há perguntas parvas — perguntar cedo poupa horas a todos.

---

## 1. O que é o projeto, em duas linhas

Lemos decisões judiciais portuguesas (acórdãos), limpamos o texto e treinamos um modelo simples que tenta prever o **sentido da decisão** a partir dos **descritores + sumário**. O que conta para a nota é a **engenharia de software** (código organizado, testes, documentação, Git), não a "inteligência" do modelo.

**Boa notícia (desbloqueador):** cada PDF vem com um **JSON** já extraído (fiável). Podes começar a trabalhar com esses JSON desde já, sem esperar por ninguém. Ver `docs/esquema_json_corpus.md`.

---

## 2. Onde cada pessoa começa

Encontra a tua linha. Lê a tua **especificação** (`docs/especificacoes/`) e o teu **guia** (`docs/guias_individuais/`). Começa pequeno e com dados de exemplo — **não esperes pelos colegas**.

| Tu és | Papel | Ticket Jira | Começa por | 1º passo concreto |
|---|---|---|---|---|
| **Alessandro** | P1 — Carregar dados | `SCRUM-5` | `src/dados/carregador_pdf.py` | Ler 2 PDFs (1 bom, 1 estragado) e imprimir nome + nº de páginas. |
| **Daniela** | P2 — Metadados / contratos | `SCRUM-6` | `src/dados/esquemas.py` (já há base) + `analisador_metadados.py` | Rever os contratos com o Pedro; validar o parser contra o JSON irmão. |
| **Gustavo** | P3 — Limpeza + categorias | `SCRUM-7` | `src/pre_processamento/limpeza_texto.py` | Remover `Powered by TCPDF`; mapear "improcedente" → `MANTIDA`. |
| **Gleicy** | P4 — NumPy / TF-IDF | `SCRUM-8` | `src/caracteristicas/vetorizador_tfidf.py` | Vocabulário de 3 frases e transformar em matriz NumPy. |
| **Helton** | P5 — Modelo PyTorch | `SCRUM-9` | `src/modelos/rede_neuronal.py` | Rede que recebe matriz e devolve 5 valores (com tensores falsos). |
| **Luciana** | P6 — Métricas / baseline | `SCRUM-10` | `src/avaliacao/metricas.py` | Função que recebe `y_real`/`y_previsto` e calcula Macro-F1. |
| **Sandro** | P7 — Inferência | `SCRUM-11` | `src/inferencia/motor_inferencia.py` | Ler um `manifesto.json` falso e seguir os caminhos. |
| **Pedro** | P8 — Integração / líder | `SCRUM-12` | `src/dados/esquemas.py` + `construtor_registos.py` | Congelar contratos; ligar as peças; CI. |

> **Toda a gente faz pelo menos um commit de código** — é critério de avaliação ("contribuições individuais"). Mesmo as tarefas mais de documentação têm uma parte de código.

---

## 3. Links, downloads e instalação

### Links rápidos (guarda esta lista)

- **📂 Dados do projeto** (PDFs + JSONs) — descarrega aqui: <https://drive.google.com/file/d/1n3XGcyk1ZoSf5vbaQYhZ5BGivebt98WG/view?usp=drive_link>
- **💻 Repositório** (GitHub): <https://github.com/geek2geeks/jurimetria_app>
- **📋 Quadro Jira** (projeto SCRUM): <https://fixola198.atlassian.net/jira/software/projects/SCRUM/boards/1>
- **Git**: <https://git-scm.com/download/win> (Windows) · macOS: `xcode-select --install` ou Homebrew
- **Anaconda** (Python 3.11): <https://www.anaconda.com/download>
- **VS Code** (editor recomendado para todos): <https://code.visualstudio.com/download>
- **Google Antigravity** — IA grátis (Gemini): <https://antigravity.google/>
- **OpenCode** — IA (alternativa): <https://opencode.ai/>
- **GitHub Spec Kit** `v0.10.2`: <https://github.com/github/spec-kit>
- **uv** (instala o Spec Kit): <https://docs.astral.sh/uv/>

> **Dados:** descarrega o corpus do link acima, coloca-o localmente e define `DATA_DIR` no teu `.env` (ver `data/README.md`). **Não republiques** o corpus nem o envies a uma IA externa (RGPD).

### Instalar (ordem certa)

Guia completo e detalhado, Windows **e** macOS: `docs/instalacao_software.md`. Resumo:

### Obrigatório para todos
1. **Git** — guarda o histórico do código. (Windows: <https://git-scm.com/download/win>)
2. **Anaconda** — cria o ambiente Python isolado. (<https://www.anaconda.com/download>)
3. Abrir o **Anaconda Prompt** (Windows) ou **Terminal** (macOS) e criar o ambiente:

   ```bash
   conda create -n juristriage python=3.11 -y
   conda activate juristriage
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   python -m unittest discover -s tests -p "test_*.py" -v
   ```

   Se o último comando disser **OK**, o teu ambiente está pronto. ✅
4. Configurar o Git com o teu nome e email reais (os mesmos do GitHub):

   ```bash
   git config --global user.name "Nome Apelido"
   git config --global user.email "email-do-github"
   ```

### Só se fores usar IA para programar (opcional)
5. Escolhe **uma** opção de IA:
   - **Opção simples e grátis:** **Google Antigravity** (<https://antigravity.google/>) — IDE com IA (Gemini), grátis em preview.
   - **Opção avançada (SDD):** **OpenCode** (`>=1.14.24`) + **uv** + **GitHub Spec Kit `v0.10.2`** + ligação ao **DeepSeek V4 Pro** com `/connect`. Passos exatos em `docs/instalacao_software.md` (secções 3 a 6).

   Em qualquer caso: declara o uso de IA no PR, lê todo o código gerado e **nunca** envies PDFs/JSON reais, dados pessoais ou chaves para a IA.

> **Importante:** o professor aprovou a equipa, mas **não** deu autorização específica para código gerado por IA. Confirma as regras da disciplina. Se usares IA: tu continuas responsável pelo código, lês tudo, corres os testes e **declaras no Pull Request** que usaste IA. **Nunca** envies PDFs/JSON reais, dados pessoais ou chaves para a IA.

**Encravaste na instalação? Fala com o Pedro.** É normal — cada máquina é diferente.

---

## 4. O ciclo de trabalho do dia a dia (GitHub + Jira)

Guia completo: `docs/fluxo_github_jira.md`. Em 6 passos:

1. **Jira:** abre o teu ticket (`SCRUM-…`) e arrasta-o para **In Progress**.
2. **Branch:** nunca trabalhes na `main`.

   ```bash
   git switch main
   git pull --ff-only origin main
   git switch -c funcionalidade/SCRUM-XX-descricao-curta
   ```
3. **Programar:** trabalha só nos ficheiros da tua spec; faz commits pequenos:

   ```bash
   git add caminho/do/ficheiro.py tests/test_ficheiro.py
   git commit -m "[SCRUM-XX] Descrição curta"
   ```
   (Não uses `git add .` — pode apanhar segredos ou dados.)
4. **Testar antes de enviar:** `python -m unittest discover -s tests -p "test_*.py" -v`
5. **Pull Request:** `git push -u origin a-tua-branch`, abre PR para `main`, liga o ticket, diz se usaste IA, e **pede revisão ao Pedro**.
6. **Done:** depois do Pedro aprovar e fazer merge, move o ticket para **Done**.

---

## 5. Como resolver problemas (sem entrar em pânico)

| Situação | O que fazer |
|---|---|
| **Estou bloqueado / não percebo a tarefa** | Move o ticket Jira para **Blocked**, escreve o que tentaste, e **contacta o Pedro**. Um bloqueio bem explicado é melhor do que esconder. |
| **A minha parte depende de outra pessoa** | Usa **dados falsos (mock)** para avançar (os guias explicam como). Não fiques parado à espera. |
| **Conflito de merge no Git** | **NUNCA** uses `git push --force` nem `git reset --hard`. Faz `git status`, copia o erro (sem segredos) e pede ajuda ao Pedro. |
| **O computador ficou sem memória (muitos PDFs)** | Não corras tudo. Usa uma amostra pequena (ex.: 10 ficheiros). Fala com o P1 (Alessandro). |
| **Erro de código que não percebo** | Isola a função num script pequeno, lê a mensagem de erro, pesquisa, e se persistir **pergunta ao Pedro** ou ao responsável da dependência. |
| **Dúvida sobre conceitos/jargão** | Consulta a secção 6 abaixo e os glossários em `docs/guia_iniciantes.md`. Continua sem perceber? **Pedro.** |

> **Regra de ouro:** em caso de dúvida, **pergunta ao Pedro** antes de fazer algo que não tens a certeza. Vale sempre a pena.

---

## 6. Mini-glossário (o essencial)

- **Repositório / GitHub:** a pasta partilhada do projeto e o sítio onde vive online.
- **Jira:** o quadro onde estão as tarefas, quem as faz e o seu estado (To Do → In Progress → In Review → Done; ou **Blocked**).
- **Branch:** a tua linha de trabalho separada, para não estragares a dos outros.
- **Commit:** guardar um conjunto pequeno de alterações com uma mensagem.
- **Pull Request (PR):** pedir que o teu trabalho seja revisto e juntado à `main`.
- **Contrato de dados (`Acordao`, etc.):** a "forma" combinada dos dados que passam de uma pessoa para a outra, para tudo encaixar.
- **Source of truth (o JSON):** a versão fiável da extração de cada PDF; o teu ponto de partida.
- **Data leakage (fuga de informação):** dar ao modelo, sem querer, a própria resposta. Por isso o `ecli`, o tribunal e a decisão **não** entram no texto de entrada.
- **TF-IDF / NumPy / PyTorch:** transformar texto em números (NumPy) e treinar o modelo (PyTorch).
- **Macro-F1:** a métrica que usamos (mais justa que a "accuracy" quando há classes desequilibradas).
- **Mock (dados falsos):** dados inventados para testares a tua parte sem esperar pelos colegas.

Glossário mais completo: `docs/guia_iniciantes.md` (secção 2) e `constitution.md`.

---

## 7. Ordem de leitura recomendada

1. Este Quickstart.
2. `constitution.md` (as regras do jogo).
3. `docs/instalacao_software.md` (instalar tudo).
4. O teu **guia** em `docs/guias_individuais/` e a tua **especificação** em `docs/especificacoes/`.
5. `docs/fluxo_github_jira.md` (o dia a dia).

**Qualquer dúvida em qualquer ponto: contacta o Pedro.** Bom trabalho, equipa! 🚀
