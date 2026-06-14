"""Adaptador JSON -> Acordao (P2).

Cada PDF do corpus vem acompanhado de um JSON com `extraction_success=True`.
Esse JSON é a *source of truth* da extração e o principal desbloqueador da
equipa: permite obter `Acordao` limpos imediatamente, sem depender do parser
posicional de PDF (que é desenvolvido em paralelo e validado contra estes
JSON — ver docs/esquema_json_corpus.md).

Os nomes de campos do JSON são externos e mistos (PT/EN); são aqui mapeados
para os nomes portugueses do contrato `Acordao` (constituição §9.4).
"""
from __future__ import annotations

import json
from pathlib import Path

from src.dados.esquemas import Acordao


def _texto_ou_none(valor: object) -> str | None:
    """Normaliza strings vazias ou só com espaços para `None` (tolerância)."""
    if not isinstance(valor, str):
        return None
    limpo = valor.strip()
    return limpo or None


def _separar_descritores(valor: object) -> list[str]:
    """Os descritores vêm como string separada por ';' (100% do corpus)."""
    if not isinstance(valor, str):
        return []
    return [parte.strip() for parte in valor.split(";") if parte.strip()]


def _ler_json(caminho_ficheiro: str | Path) -> object:
    """Lê o JSON tolerando o encoding do corpus.

    O corpus tem caracteres de substituição (U+FFFD) gravados nos bytes; a
    leitura usa utf-8 e, em caso de falha, tenta cp1252/latin-1 antes de
    recorrer a substituição, para nunca interromper o lote.
    """
    bruto = Path(caminho_ficheiro).read_bytes()
    for codificacao in ("utf-8", "cp1252", "latin-1"):
        try:
            return json.loads(bruto.decode(codificacao))
        except UnicodeDecodeError:
            continue
    return json.loads(bruto.decode("utf-8", errors="replace"))


def acordao_de_dicionario(dados: dict) -> Acordao:
    """Converte um dicionário do JSON do corpus num `Acordao`.

    Campos ausentes ou vazios tornam-se `None` (ou lista vazia nos
    descritores), respeitando a regra de tolerância da constituição §5.
    """
    ano = dados.get("year")
    return Acordao(
        ecli=_texto_ou_none(dados.get("ecli")),
        url=_texto_ou_none(dados.get("jurisprudencia_url")),
        tribunal=_texto_ou_none(dados.get("court_code")),
        ano=ano if isinstance(ano, int) else None,
        relator=_texto_ou_none(dados.get("relator")),
        numero_documento=_texto_ou_none(dados.get("numero_documento")),
        data_acordao=_texto_ou_none(dados.get("data_acordao")),
        meio_processual=_texto_ou_none(dados.get("meio_processual")),
        votacao=_texto_ou_none(dados.get("votacao")),
        area_tematica=_texto_ou_none(dados.get("area_tematica")),
        descritores=_separar_descritores(dados.get("descritores")),
        sumario=_texto_ou_none(dados.get("sumario_texto")),
        decisao_bruta=_texto_ou_none(dados.get("decisao")),
        texto_integral=_texto_ou_none(dados.get("decisao_integral_texto")),
        origem="json",
        extracao_bem_sucedida=bool(dados.get("extraction_success", True)),
    )


def carregar_acordaos_json(caminho_ficheiro: str | Path) -> list[Acordao]:
    """Lê um ficheiro JSON do corpus e devolve uma lista de `Acordao`.

    Aceita um único acórdão (objeto JSON) ou uma lista de acórdãos.
    """
    dados = _ler_json(caminho_ficheiro)
    if isinstance(dados, list):
        return [acordao_de_dicionario(item) for item in dados if isinstance(item, dict)]
    if isinstance(dados, dict):
        return [acordao_de_dicionario(dados)]
    return []
