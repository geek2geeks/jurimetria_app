"""
Parsing posicional de metadados de decisoes judiciais portuguesas (P2 / SCRUM-6).

Transforma um `DocumentoBruto` (output do P1 - Alessandro) num `Acordao`
estruturado, extraindo campos como relator, ECLI, sumario, descritores,
tribunal e data_acordao atraves de expressoes regulares posicionais.

Tolerante a campos em falta: devolve `None` (ou lista vazia) em vez de falhar.
Nao altera os contratos em `src/dados/esquemas.py` (copropriedade P2+P8) nem o
`carregador_acordaos_json.py`. Apenas consome `DocumentoBruto` e produz `Acordao`.

Validado contra `data/documento_bruto_ECLI_PT_TRL_2025_20.24.0T8LSB.L1.4.D7.json`
(output real do P1 com 21 paginas, 74163 chars de texto de PDF).
"""
from __future__ import annotations

import re
from typing import Final, Pattern

from src.dados.esquemas import Acordao, DocumentoBruto


# ---------------------------------------------------------------------------
# REGEX COMPILADAS (topo do modulo, compiladas uma unica vez)
# ---------------------------------------------------------------------------
# Compilar regex fora da funcao e' mais eficiente (nao recompila a cada
# chamada). typing.Final indica que a variavel e' constante.
# (?im) = case-insensitive + multiline (^ e $ casam inicio/fim de linha).
# (?P<nome>...) = grupo nomeado, mais legivel que grupo numerico.
# ---------------------------------------------------------------------------


# ECLI: PT:STJ:2024:123 ou TRL:2025:20.24.0T8LSB.L1.4.D7 (com pontos, letras)
# Ancorado a word boundary para nao apanhar substrings dentro de "DECLINA" etc.
_REGEX_ECLI: Final[Pattern[str]] = re.compile(
    r"\bECLI:PT:[A-Z0-9.:_-]+"
)


# Tribunal: extraido do ECLI, porque no texto bruto o tribunal nao vem
# rotulado. ECLI:PT:TRL:... -> grupo 1 = "TRL"
_REGEX_TRIBUNAL_DO_ECLI: Final[Pattern[str]] = re.compile(
    r"ECLI:PT:([A-Z]+):"
)


# Relator: no texto do PDF, a tabela tem "Relator" como rotulo e o nome
# esta' 1 linha abaixo, seguido de sufixo curto (ex: "rl" para relator,
# "cld" para conselheiro, "j" para juiz). Regex: "\nRelator[^\n]*\nNOME suf"
_REGEX_RELATOR: Final[Pattern[str]] = re.compile(
    r"\nRelator[^\n]*\n([A-ZÁÉÍÓÚÂÊÔÃÕÇ][^\n]+?)\s+[a-z]{1,3}\s"
)


# Descritores: pode estar "Descritores" sozinho (com newline depois) ou
# "Descritores: a; b; c" na mesma linha. Regex: apanha ambos os formatos.
# Depois da label, aceita qualquer char que nao seja nova linha ate encontrar
# a lista de descritores (string com pelo menos 1 ';').
# O (?=[;\n]|\Z) e' lookahead para parar antes de uma nova seccao.
_REGEX_DESCRITORES: Final[Pattern[str]] = re.compile(
    r"Descritores\s*[:\-]?\s*\n?\s*([^\n]+(?:;[^\n]+)+)"
)


# Sumario: de "Sumario:" ate "Decisao Integral:". Lookahead para a proxima
# seccao. re.DOTALL faz o . casar com \n (default e' so' ate' \n).
# Tolera "Sumario" e "Sumário" (OCR pode perder o acento).
_REGEX_SUMARIO: Final[Pattern[str]] = re.compile(
    r"Sum[áa]rio[:\s]*\n(.+?)(?=\nDecis[ãa]o Integral)",
    re.DOTALL,
)


# Data do acordao: regex generico para datas dd/mm/aaaa (best-effort).
# Pode apanhar outras datas no texto (ex: data de criacao PDF), mas a do
# acordao costuma ser a primeira que aparece no cabecalho.
_REGEX_DATA_ACORDAO: Final[Pattern[str]] = re.compile(
    r"\b(\d{2}/\d{2}/\d{4})\b"
)


# Meio processual: rotulo "Meio Processual" seguido do valor.
# No texto real, o rotulo esta' numa tabela com outros rotulos na mesma linha
# (ex: "Meio Processual Decisão\nApelação improcedente"). Saltamos qualquer
# texto ate' ao fim da linha, depois apanhamos o valor na linha seguinte.
# Valores possiveis: Apelacao, Recurso, Revista, Contra-ordenacao.
_REGEX_MEIO_PROCESSUAL: Final[Pattern[str]] = re.compile(
    r"Meio\s+Processual[^\n]*\n\s*(Apela[çc][ãa]o|Recurso|Revista|Contra[- ]ordenação)",
    re.IGNORECASE,
)


# Decisao bruta (Y - alvo do modelo): vem na tabela como "Apelação improcedente"
# ou similar. Apanha a palavra que vem depois do meio processual.
# Case-insensitive para tolerar OCR.
_REGEX_DECISAO_BRUTA: Final[Pattern[str]] = re.compile(
    r"(?:Apela[çc][ãa]o|Recurso|Revista)\s+"
    r"(improcedente|procedente|provimento|provido|negado provimento|"
    r"mantida|revogada|n[ãa]o conhecida|parcialmente procedente|"
    r"nulidade|anulada)",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# HELPERS PRIVADOS
# ---------------------------------------------------------------------------


def _primeiro_grupo(padrao: Pattern[str], texto: str) -> str | None:
    """Devolve o grupo 1 do primeiro match, ou None se nao casar.

    Helper generico: procura a regex, devolve o grupo 1 com strip.
    String vazia -> None (tolerancia, constituicao §5).
    """
    match = padrao.search(texto)
    if not match:
        return None
    valor = match.group(1).strip()
    return valor or None


def _primeiro_match_completo(padrao: Pattern[str], texto: str) -> str | None:
    """Devolve o match completo (grupo 0), ou None. Para regex sem grupos."""
    match = padrao.search(texto)
    if not match:
        return None
    return match.group(0).strip() or None


def _dividir_descritores(bloco: str | None) -> list[str]:
    """Divide o bloco de descritores por ponto-e-virgula.

    Faz strip a cada item e descarta vazios. Retorna [] se bloco for None
    ou string vazia.
    """
    if not bloco:
        return []
    return [parte.strip() for parte in bloco.split(";") if parte.strip()]


def _normalizar_espacos(valor: str | None) -> str | None:
    """Remove quebras de linha e espacos duplicados. Devolve None se vazio.

    Texto de PDF/OCR vem com quebras e espacos estranhos:
      "O tribunal\\ndecidiu que..."     -> "O tribunal decidiu que..."
      "A   lei   civil  portuguesa"   -> "A lei civil portuguesa"
    """
    if not valor:
        return None
    return re.sub(r"\s+", " ", valor).strip() or None


# ---------------------------------------------------------------------------
# FUNCAO PUBLICA
# ---------------------------------------------------------------------------


def analisar_documento_bruto(documento_bruto: DocumentoBruto) -> Acordao:
    """Extrai metadados posicionais do texto bruto e devolve um Acordao.

    Estrategia:
      1. Validar o input (None -> TypeError, texto nao-str -> TypeError).
      2. Aplicar cada regex ao campo `texto` do DocumentoBruto.
      3. Ausencias viram None (ou [] para descritores).
      4. Construir um Acordao com `origem="pdf"` e `extracao_bem_sucedida=True`.

    Args:
        documento_bruto: Caixa com texto bruto e metadados de origem (P1).

    Returns:
        Acordao preenchido com os campos extraidos. NUNCA dict.
        Os campos que nao sao extraidos por P2 ficam None (dataclass default).

    Raises:
        TypeError: se documento_bruto for None ou texto nao for str.
            Outros campos em falta NAO levantam excecao.
    """
    # --- Validacoes de input (erros de programacao, NAO de dados) ---
    if documento_bruto is None:
        raise TypeError(
            "documento_bruto nao pode ser None - "
            "passe um DocumentoBruto valido."
        )

    texto = documento_bruto.texto
    if not isinstance(texto, str):
        raise TypeError(
            f"documento_bruto.texto deve ser str, "
            f"recebeu {type(texto).__name__}"
        )

    # --- Extracao de campos (cada um via regex + helper) ---

    ecli = _primeiro_match_completo(_REGEX_ECLI, texto)

    tribunal = _primeiro_grupo(_REGEX_TRIBUNAL_DO_ECLI, texto)

    relator = _primeiro_grupo(_REGEX_RELATOR, texto)

    descritores_bloco = _primeiro_grupo(_REGEX_DESCRITORES, texto)
    descritores = _dividir_descritores(descritores_bloco)

    sumario_match = _REGEX_SUMARIO.search(texto)
    sumario_bruto = sumario_match.group(1) if sumario_match else None
    sumario = _normalizar_espacos(sumario_bruto)

    data_acordao = _primeiro_grupo(_REGEX_DATA_ACORDAO, texto)

    meio_processual = _primeiro_grupo(_REGEX_MEIO_PROCESSUAL, texto)

    decisao_bruta = _primeiro_grupo(_REGEX_DECISAO_BRUTA, texto)

    # --- Construir e devolver o Acordao ---
    return Acordao(
        ecli=ecli,
        url=None,  # PDF nao tem URL (vem do JSON)
        tribunal=tribunal,
        ano=None,  # P2 nao extrai (pode vir do ECLI no futuro)
        relator=relator,
        numero_documento=None,  # P2 nao extrai (esta' em "rl" ao lado do nome)
        data_acordao=data_acordao,
        meio_processual=meio_processual,
        votacao=None,  # P2 nao extrai
        area_tematica=None,  # P2 nao extrai
        descritores=descritores,
        sumario=sumario,
        decisao_bruta=decisao_bruta,
        texto_integral=None,  # LEAKAGE - nao se preenche no parser posicional
        origem="pdf",
        extracao_bem_sucedida=True,
    )
