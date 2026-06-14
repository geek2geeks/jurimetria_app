# Critérios de avaliação (mapa deliverable → peso → responsável)

Reposição do mapeamento de avaliação para a equipa saber onde está a nota.

> **A confirmar contra o enunciado oficial (`Projeto.pdf`).** Os pesos abaixo
> seguem a leitura do enunciado feita na fase de proposta; se o PDF divergir,
> manda o PDF.

| Critério | Peso aprox. | Onde no projeto | Principais responsáveis |
|---|---:|---|---|
| Definição/contextualização do problema | 10% | `docs/visao.md`, `docs/requisitos.md` | P8 (Pedro) |
| Modularização, funções, organização | 15% | `src/` por responsabilidade | Todos; coord. P8 |
| Tipagem e qualidade de código | 10% | type hints em todas as funções; constituição §9/§10 | Todos |
| Uso real de NumPy | 10% | `src/caracteristicas/vetorizador_tfidf.py` | P4 (Gleicy) |
| PyTorch (treino) | ~20% | `src/modelos/`, `src/treino/` | P5 (Helton) |
| Testes (unittest) | 10% | `tests/`, CI GitHub Actions | P7 (Sandro) testes de inferência; todos testam o seu módulo; coord. P8 |
| Requisitos | 15% | `docs/requisitos.md` | P8 (Pedro) |
| Design, arquitetura e Git | ~5% | `docs/arquitetura.md`, `docs/decisoes.md`, fluxo Git | P8 (Pedro) |
| Apresentação final | 5% | demo + slides | Todos; coord. P8 |

## Implicações práticas

- **Quase metade da nota (~45%) está na Entrega 1**: qualidade de código
  (módulos, funções, type hints) + NumPy + definição do problema. Não deixar
  para o fim.
- **Requisitos (15%) pesam mais do que os testes (10%)** — o documento de
  requisitos é um entregável de peso, não um anexo.
- A **accuracy do modelo não é o foco**: a nota premeia engenharia de software.
  Por isso a métrica é **Macro-F1 vs baseline**, não accuracy (ver
  `docs/requisitos.md` RNF08 e `especificacao_06`).
- Cada membro deve ter **pelo menos um commit de código**: "contribuições
  individuais" é avaliado (ver histórico Git e Jira).
