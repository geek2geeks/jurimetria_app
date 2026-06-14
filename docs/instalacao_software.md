# Instalação de software

Este guia usa Python 3.11 em todas as máquinas. Não mistures ambientes: se escolheres Windows nativo, executa Python, Git e OpenCode no Windows; se escolheres WSL, instala e executa tudo dentro do WSL.

## 1. Instalar Git

Antes de clonar o projeto, instala Git:

- Windows: <https://git-scm.com/download/win>
- macOS: executa `xcode-select --install` ou instala Git por Homebrew.

Verifica:

```bash
git --version
```

## 2. Instalar Anaconda

Anaconda cria ambientes Python isolados. O projeto usa o ambiente `juristriage`.

### Windows

1. Abre <https://www.anaconda.com/download>.
2. Descarrega o instalador gráfico Windows 64-bit.
3. Executa a instalação para `Just Me`.
4. Não é necessário adicionar Anaconda ao `PATH`.
5. Abre **Anaconda Prompt** pelo menu Iniciar.
6. Verifica:

```bash
conda --version
python --version
```

### macOS

1. Abre <https://www.anaconda.com/download>.
2. Escolhe o instalador compatível com Apple Silicon. Para Mac Intel, consulta o arquivo de versões indicado pela Anaconda.
3. Executa o instalador `.pkg`.
4. Fecha e reabre o Terminal.
5. Verifica:

```bash
conda --version
python --version
```

### Criar o ambiente do projeto

Windows, no Anaconda Prompt:

```powershell
cd C:\caminho\para\jurimetria_app
conda create -n juristriage python=3.11 -y
conda activate juristriage
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m unittest discover -s tests -p "test_*.py" -v
```

macOS:

```bash
cd /caminho/para/jurimetria_app
conda create -n juristriage python=3.11 -y
conda activate juristriage
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m unittest discover -s tests -p "test_*.py" -v
```

No início de cada sessão:

```bash
conda activate juristriage
```

## 3. Instalar OpenCode

O projeto recomenda OpenCode `>=1.14.24`.

### Windows nativo

Escolhe apenas um método.

Com Chocolatey:

```powershell
choco install opencode
```

Com Scoop:

```powershell
scoop install opencode
```

Com Node.js:

```powershell
npm install -g opencode-ai
```

O OpenCode recomenda WSL para melhor compatibilidade. Esta alternativa é adequada apenas se instalares também Git, Anaconda/Miniconda e o ambiente do projeto dentro do WSL. No WSL, o caminho Windows `C:\posgrad\jurimetria_app` corresponde normalmente a `/mnt/c/posgrad/jurimetria_app`.

### macOS

Com Homebrew:

```bash
brew install anomalyco/tap/opencode
```

Ou com o instalador:

```bash
curl -fsSL https://opencode.ai/install | bash
```

### Verificar

```bash
opencode --version
```

O resultado deve ser `1.14.24` ou superior.

## 4. Ligar OpenCode ao DeepSeek

1. Ativa o ambiente e entra no repositório.
2. Executa:

```bash
opencode
```

3. Dentro do OpenCode, escreve:

```text
/connect
```

4. Procura e seleciona `DeepSeek`.
5. Cola a chave diretamente no campo seguro.
6. Seleciona `DeepSeek-V4-Pro`.
7. Confirma o modelo através do seletor de modelos do OpenCode.

Não uses `setx`, não escrevas a chave em `.zshrc` e não a coloques na linha de comandos. Esses métodos podem deixar a chave em histórico ou texto simples. Não tires screenshots durante a configuração.

A chave é partilhada e gerida por Pedro. Deve ter controlo de custos, ser rodada quando alguém sai e revogada no fim do projeto.

## 5. Instalar uv

O `uv` instala o Specify CLI num ambiente separado do projeto.

Windows:

```powershell
winget install --id=astral-sh.uv -e
```

macOS:

```bash
brew install uv
```

Verifica:

```bash
uv --version
```

## 6. Instalar GitHub Spec Kit

O projeto fixa a versão `v0.10.2`:

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v0.10.2
specify version
specify integration list
```

Se já existir outra versão:

```bash
uv tool install --force specify-cli --from git+https://github.com/github/spec-kit.git@v0.10.2
specify version
```

O comando deve indicar `0.10.2`.

No Windows, se continuar a aparecer uma versão antiga:

```powershell
where.exe specify
uv tool list
```

Mais de um caminho indica instalações duplicadas. Remove a cópia antiga pelo mesmo gestor que a instalou e mantém a versão isolada do `uv`. Não apagues executáveis sem confirmar primeiro o caminho.

### Inicialização no repositório

Só Pedro deve inicializar o Spec Kit. Os restantes membros recebem os ficheiros através de Git.

Antes de executar, Pedro deve:

1. garantir que o ramo está limpo;
2. criar um ramo próprio;
3. guardar uma cópia do diff;
4. confirmar a integração:

```bash
specify integration list
```

5. inicializar:

```bash
specify init . --force --integration opencode
```

6. rever todos os ficheiros criados ou alterados antes do commit.

O Spec Kit pode criar `.specify/memory/constitution.md`. A Constituição normativa deste projeto continua a ser `constitution.md` na raiz; qualquer cópia gerada deve apontar para ela e não pode introduzir regras divergentes.

### Uso diário

Dentro do OpenCode:

```text
/speckit.clarify
/speckit.plan
/speckit.tasks
/speckit.analyze
/speckit.implement
```

Não avances automaticamente entre etapas. Revê o resultado antes de continuar.

Vídeo introdutório ligado pelo repositório do Spec Kit:

<https://www.youtube.com/watch?v=a9eR1xsfvHg>

O vídeo é material complementar. Os comandos deste documento e a documentação oficial têm prioridade.

## 7. Variáveis locais

Cria `.env` a partir do exemplo:

Windows:

```powershell
Copy-Item .env.example .env
```

macOS:

```bash
cp .env.example .env
```

Preenche apenas no `.env` local. Para usar apenas OpenCode com `/connect`, não é necessário colocar a chave DeepSeek no `.env`.

## 8. Diagnóstico rápido

Executa:

```bash
git --version
conda --version
python --version
opencode --version
uv --version
specify version
```

Resultados esperados:

- Python `3.11.x`;
- OpenCode `1.14.24` ou superior;
- Specify CLI `0.10.2`.

Não continues se estiveres no ambiente `base` ou se `python --version` não mostrar 3.11.
