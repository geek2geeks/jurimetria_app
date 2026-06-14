# Especificação: Ingestão de Dados (Data Loader)

**Assignee:** Alessandro (P1 - Especialista em Ingestão)
**Fase do SDD:** Specify

## 1. Contexto (O Porquê)
O nosso sistema precisa consumir a jurisprudência portuguesa. Como o dataset completo excede os limites de memória da máquina, precisamos de um *loader* tolerante a falhas que leia os documentos de forma iterativa sem rebentar a RAM (OOM), começando pela nossa amostra diversificada compactada.

## 2. Tarefa Técnica (O Quê)
1. Construir a classe/função iteradora `JurisTriageLoader` no arquivo `src/data/data_loader.py`.
2. A classe deve receber o caminho para a pasta de dados (`data/`) extraída do ZIP.
3. Deve iterar sobre os arquivos `.json` e `.pdf`.
4. Em vez de carregar tudo para uma lista, a função deve usar a diretiva `yield` (Generator em Python) para devolver um dicionário cru com os metadados brutos do JSON e o conteúdo em texto do PDF (se extraível).
5. O código deve capturar exceções (ex: JSON corrompido, PDF ilegível) e registá-las via módulo nativo `logging`, sem interromper o *loop*.

## 3. Inputs e Outputs
- **Input:** Caminho absoluto do diretório (tipo `str` ou `pathlib.Path`).
- **Output:** Generator de dicionários: `Generator[Dict[str, Any], None, None]`.
  - Exemplo de Yield: `{"filename": "...", "text": "...", "metadata": {...}}`

## 4. Regras e Restrições SDD
- **Tipagem Forte Obrigatória:** Todas as variáveis e retornos devem usar Type Hints do pacote `typing`.
- Nenhuma dependência pesada de ML (sem torch, sem sklearn) neste módulo. Apenas `json`, `pathlib`, `logging` e uma biblioteca leve para extração (como `pdfplumber` ou `PyPDF2` caso necessário para os PDFs).

## 5. Critérios de Aceitação (DoD)
- [ ] O módulo possui o arquivo de testes unitários `tests/test_loader.py`.
- [ ] O código consegue ler os 10.000 ficheiros JSONs da amostra sem exceder 1GB de RAM.
- [ ] Se eu colocar um ficheiro `txt` inválido no meio, o script regista o erro num `ingestion.log` e continua a iteração.

---

> **Instrução para Agente de IA:**
> Quando receberes este documento, NÃO inicies a programação imediatamente. Lê a Constituição do Projeto e executa o comando interativo:
> `/speckit.clarify`: Aponta as dúvidas sobre a estrutura exata do JSON e como tratar PDFs protegidos. Após as respostas, prossegue para a fase `/speckit.plan`.
