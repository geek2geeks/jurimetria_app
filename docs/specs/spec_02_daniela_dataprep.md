# Especificação: Parsing Posicional de Metadados

**Assignee:** Daniela (P2 - Data Prep)
**Fase do SDD:** Specify

## 1. Contexto (O Porquê)
Os nossos acórdãos portugueses sofrem de um problema estrutural severo: são PDFs ou JSONs gerados a partir de um layout de 2 colunas. Uma leitura linear ingénua cruza e funde a coluna do "Relator" com a coluna do "Meio Processual". Precisamos de algoritmos inteligentes (parsing posicional ou âncoras textuais) para garantir que o *Feature Engineer* recebe as colunas perfeitas.

## 2. Tarefa Técnica (O Quê)
1. Construir o módulo de parser `src/preprocessing/metadata_parser.py`.
2. A função principal deve receber o dicionário cru gerado pelo `data_loader.py` do Alessandro.
3. Isolar os campos críticos que a rede neural vai precisar: `ECLI`, `Tribunal`, `Descritores`, `Sumario_Texto`, `Decisao`.
4. O parser deve usar expressões regulares (`re`) rigorosas e delimitadores fixos para contornar o salto de linhas.
5. Se um documento não tiver a secção `Decisão` preenchida (campo vital), o parser deve retornar `None` para esse campo específico em vez de tentar adivinhar com o parágrafo seguinte.

## 3. Inputs e Outputs
- **Input:** `Dict[str, Any]` (O output exato gerado pelo P1).
- **Output:** Objeto Data Class ou dicionário padronizado:
  ```python
  @dataclass
  class Acordao:
      ecli: str
      tribunal: str
      descritores: List[str]
      sumario: str
      decisao: Optional[str]
  ```

## 4. Regras e Restrições SDD
- **Resiliência a Nulos:** O código Python deve antecipar falhas de regex (usar `.get()` ou blocos `try/except`).
- **Data Classes:** O uso de `@dataclass` (módulo nativo do Python) é obrigatório para representar a estrutura do Acórdão final.

## 5. Critérios de Aceitação (DoD)
- [ ] O módulo inclui testes unitários em `tests/test_parser.py` testando documentos reais com 2 colunas.
- [ ] Documentos em que a decisão esteja explicitamente omitida não quebram a pipeline, resultando num objeto cujo atributo `decisao` é `None`.

---

> **Instrução para Agente de IA:**
> Antes de gerar o Python, garante que tens acesso ao `constitution.md`. 
> Executa `/speckit.clarify`: Faz perguntas concretas à Daniela sobre quais são os "tokens" e marcadores âncora que a Regex deve usar. Após o esclarecimento, gera o Plano Arquitetural (`/speckit.plan`).
