# Guia de Instalação e Uso: SpecKit com OpenCode

Este guia detalha a configuração e utilização do **GitHub Spec Kit** (`specify-cli`) em conjunto com a aplicação de inteligência artificial **OpenCode** para apoiar o desenvolvimento do projeto **JurisTriage PT**. 

O Spec Kit adota a metodologia de **Desenvolvimento Baseado em Especificações (SDD - Spec-Driven Development)**, permitindo que a IA trabalhe de forma estruturada e auditável através de etapas bem definidas (análise, planeamento, tarefas, verificação e implementação) em vez do tradicional prompt improvisado.

---

## 1. Instalação do OpenCode

O OpenCode (versão recomendada: `>=1.14.24`) é o assistente de IA nativo de terminal que utilizaremos. Para instalá-lo de forma limpa, utilize um dos seguintes métodos oficiais de acordo com o seu sistema operativo:

### No Windows
Escolha apenas **um** dos seguintes gerenciadores de pacotes (abra o terminal como Administrador):

*   **Via Chocolatey:**
    ```powershell
    choco install opencode
    ```
*   **Via Scoop:**
    ```powershell
    scoop install opencode
    ```
*   **Via Node.js (npm):**
    ```powershell
    npm install -g opencode-ai
    ```

### No macOS
*   **Via Homebrew:**
    ```bash
    brew install anomalyco/tap/opencode
    ```
*   **Via Script curl oficial:**
    ```bash
    curl -fsSL https://opencode.ai/install | bash
    ```

### Verificação
Para garantir que a instalação foi concluída corretamente, execute:
```bash
opencode --version
```
*Resultado esperado: `1.14.24` ou superior.*

---

## 2. Ligação do OpenCode ao DeepSeek (Melhores Práticas)

Para que o assistente OpenCode consiga raciocinar e gerar soluções, devemos ligá-lo a um modelo fundacional. O projeto recomenda o **DeepSeek-V4-Pro** para tarefas complexas de lógica e código.

### Configuração Segura (Passo a Passo)
> ⚠️ **Cuidado (Segurança de Chaves API):** Nunca guarde a sua chave da DeepSeek no ficheiro `.env` do projeto, em variáveis de ambiente globais do sistema (`setx` no Windows ou `.zshrc` no macOS) ou no histórico do terminal. O OpenCode possui uma forma segura de gerir chaves.

1.  Abra o OpenCode no seu terminal dentro da pasta do repositório:
    ```bash
    opencode
    ```
2.  Na barra de chat do OpenCode, digite o comando de ligação:
    ```text
    /connect
    ```
3.  Selecione o provedor **DeepSeek** no menu interativo.
4.  Cole a chave de API diretamente no campo seguro exibido (a chave é partilhada e gerida pelo Pedro, Scrum Master).
5.  Selecione o modelo **DeepSeek-V4-Pro** (ou use a versão *Flash* para tarefas de baixo custo).
6.  Confirme a alteração e feche o assistente. O OpenCode guardará a chave de forma encriptada no chaveiro seguro da máquina.

---

## 3. Instalação Isolada do GitHub Spec Kit (`specify-cli`)

Para evitar conflitos de dependências com a biblioteca padrão ou com o ambiente Conda do projeto (`juristriage`), instalamos o Spec Kit de forma isolada utilizando o gestor de ferramentas **uv**.

### Passo 1: Instalar o gestor `uv`
*   **No Windows:**
    ```powershell
    winget install --id=astral-sh.uv -e
    ```
*   **No macOS:**
    ```bash
    brew install uv
    ```

### Passo 2: Instalar a versão fixada do Spec Kit (`v0.10.2`)
O projeto exige que todos os membros da equipa utilizem a mesma versão para evitar conflitos de templates. Instale especificando a tag oficial:
```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v0.10.2
```

Se por acaso já tiver uma versão anterior instalada, force a atualização com:
```bash
uv tool install --force specify-cli --from git+https://github.com/github/spec-kit.git@v0.10.2
```

### Passo 3: Verificação
Confirme a instalação e as integrações disponíveis com os comandos:
```bash
specify version
specify integration list
```
*Resultados esperados: Versão `0.10.2` e integração `opencode` disponível.*

![Instalação do Spec Kit](fig_speckit_install.png)

---

## 4. Inicialização no Repositório

> 📢 **Importante (Papel do Scrum Master):** Apenas o **Pedro (Scrum Master)** deve inicializar o Spec Kit na raiz do repositório. Os restantes membros da equipa apenas obtêm as configurações através do `git pull`.

Antes de inicializar, o Pedro deve garantir que a branch de trabalho está limpa. Execute o comando na raiz da pasta `jurimetria_app`:
```bash
specify init . --force --integration opencode
```

Este comando cria a estrutura de configuração do Spec Kit na pasta `.specify/`:
*   `.specify/config.json`: Define que o assistente ativo será o OpenCode.
*   `.specify/memory/constitution.md`: Uma referência às regras estruturais do projeto. *(Nota: O ficheiro `constitution.md` na raiz continua a ser a única fonte de verdade. Qualquer cópia na pasta `.specify` deve referenciar a raiz e não pode conter regras contraditórias).*

![Inicialização no Repositório](fig_speckit_init.png)

---

## 5. Fluxo de Trabalho Diário com Spec Kit (SDD)

Ao trabalhar numa tarefa, em vez de pedir à IA para "escrever o código diretamente", siga rigorosamente o ciclo de desenvolvimento SDD. No chat do OpenCode, use os comandos específicos do Spec Kit abaixo:

```text
  [Tarefa Jira: In Progress]
             │
             ▼
  [/speckit.clarify] ──► (Alinhamento / Revisão Humana de Ambiguidades)
             │
             ▼
  [/speckit.plan] ──► (Gera o plano em implementation_plan.md)
             │
             ▼
  [/speckit.tasks] ──► (Gera a checklist em task.md)
             │
             ▼
  [/speckit.analyze] ──► (Audita a consistência dos ficheiros)
             │
             ▼
  [/speckit.implement] ──► (Gera o código rascunho de trabalho)
             │
             ▼
  [Testes locais & Pull Request] ──► (Validação final e aprovação por Pedro)
```

### Comandos do Spec Kit e Melhores Práticas

1.  **`/speckit.clarify`**
    *   **O que faz:** Lê a especificação do seu ficheiro individual em `docs/guias_individuais/` e a Constituição do projeto, identificando potenciais ambiguidades nos contratos de dados, dependências e tipos.
    *   **Melhor Prática:** Não avance sem ler as ambiguidades detetadas. Discuta as respostas com a equipa (Pedro ou Daniela) se envolver alterações nos esquemas de dados.

2.  **`/speckit.plan`**
    *   **O que faz:** Cria um plano detalhado de implementação em `implementation_plan.md` na raiz do seu espaço de trabalho.
    *   **Melhor Prática:** O plano deve ser pequeno e focado. Garanta que o plano prevê testes automatizados e não altera ficheiros fora do seu escopo de tarefa.

3.  **`/speckit.tasks`**
    *   **O que faz:** Gera um ficheiro `task.md` com uma checklist de tarefas (TODO list) baseada no plano aprovado.
    *   **Melhor Prática:** Atualize o estado das tarefas (`[ ]` por fazer, `[/]` em progresso, `[x]` concluído) à medida que desenvolve. Isto mantém a transparência no Git.

4.  **`/speckit.analyze`** (ou `/speckit.checklist`)
    *   **O que faz:** Analisa de forma crítica se o código existente e a checklist estão alinhados com a especificação original e a Constituição do projeto.

5.  **`/speckit.implement`**
    *   **O que faz:** Produz o código rascunho com base nas tarefas.
    *   **Melhor Prática:** **NUNCA** integre o código gerado sem rever linha a linha. A IA é uma ferramenta de apoio, mas você é o único responsável técnico pelas suas alterações.

![Uso Diário do OpenCode com SpecKit](fig_speckit_use.png)

---

## 6. Validação e Entrega de Código

Após finalizar a implementação através do fluxo do Spec Kit:

1.  **Execute a suíte de testes locais:**
    ```bash
    python -m unittest discover -s tests -p "test_*.py" -v
    ```
    *Garante que nenhuma funcionalidade antiga foi quebrada e que a sua nova classe está coberta por testes.*
2.  **Verifique a segurança de segredos:**
    *   Certifique-se de que não adicionou acidentalmente ficheiros `.env` locais, logs com dados pessoais de acórdãos judiciais ou chaves de API nos seus commits.
3.  **Abra o Pull Request declarando a utilização da IA:**
    No preenchimento da descrição do PR, declare o uso de IA usando o seguinte formato estrito:
    ```text
    Apoio de IA: Sim.
    Ferramenta: OpenCode com DeepSeek V4 Pro.
    Utilização: Esclarecimento da especificação (/speckit.clarify) e rascunho de testes.
    Validação humana: Li o diff linha a linha, executei a suíte de testes e compreendo todas as alterações.
    ```

