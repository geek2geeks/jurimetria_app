"""Carregador incremental de JSONs contendo apenas texto bruto.

Responsabilidade da P1:
- ler JSONs ainda não estruturados;
- aceitar apenas string JSON ou objeto simples com chave "texto";
- emitir DocumentoBruto sequencialmente com origem="json";
- rejeitar JSONs estruturados, pois esses pertencem ao adaptador da P2.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Callable, Iterator
from pathlib import Path

from src.dados.esquemas import DocumentoBruto

logger = logging.getLogger(__name__)


def _ler_texto_json_bruto(caminho_json: Path) -> str:
    """Lê um JSON bruto e devolve somente o texto.

    Formatos aceitos pela P1:
    1. "texto bruto em string";
    2. {"texto": "texto bruto dentro de uma chave simples"}.

    JSONs com campos jurídicos prontos, como ecli, relator, decisao ou sumario,
    não são tratados aqui para não invadir a responsabilidade da P2.
    """
    with caminho_json.open("r", encoding="utf-8") as ficheiro:
        conteudo = json.load(ficheiro)

    if isinstance(conteudo, str):
        return conteudo

    if isinstance(conteudo, dict) and isinstance(conteudo.get("texto"), str):
        return conteudo["texto"]

    raise ValueError(
        "JSON bruto deve ser uma string JSON ou um objeto simples com a chave 'texto'."
    )


def carregar_jsons_brutos(
    pasta: str | Path,
    *,
    registrar_falha: Callable[[Path, Exception], None] | None = None,
) -> Iterator[DocumentoBruto]:
    """Percorre JSONs brutos de uma pasta e emite um DocumentoBruto por vez.

    Assim como no carregador de PDF, o yield evita carregar todos os documentos
    em memória, permitindo processar grandes volumes de arquivos.

    Args:
        pasta: Diretório de entrada com JSONs brutos.
        registrar_falha: Callback opcional usado pelos scripts auxiliares para
            registrar falhas estruturadas em CSV/JSON/JSONL. Esse parâmetro não
            altera o contrato principal da P1, que continua sendo o yield de
            DocumentoBruto.
    """
    pasta_path = Path(pasta)

    for caminho_json in sorted(pasta_path.rglob("*.json")):
        try:
            texto = _ler_texto_json_bruto(caminho_json)

            documento = DocumentoBruto(
                nome_ficheiro=caminho_json.name,
                caminho=str(caminho_json),
                texto=texto,
                numero_paginas=None,
                origem="json",
            )

            # Esta é a saída exigida pela especificação P1.
            yield documento

        except Exception as erro:
            # JSON inválido ou estruturado é registrado, mas não interrompe
            # o processamento dos demais arquivos da pasta.
            logger.exception("Falha ao carregar JSON '%s': %s", caminho_json, erro)
            if registrar_falha is not None:
                registrar_falha(caminho_json, erro)
            continue


# Alias para compatibilidade com versões anteriores dos scripts.
iterar_jsons_brutos = carregar_jsons_brutos
