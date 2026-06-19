"""Funções auxiliares para materializar DocumentoBruto em JSON/CSV.

A saída oficial da P1 é o objeto DocumentoBruto emitido por yield. Estas funções
existem apenas para inspeção, teste em Colab e evidência da ingestão.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.dados.esquemas import DocumentoBruto


def documento_bruto_para_dict(
    documento: DocumentoBruto,
    *,
    incluir_texto_completo: bool = True,
) -> dict[str, Any]:
    """Converte DocumentoBruto para dicionário serializável em JSON/CSV."""
    texto = documento.texto if incluir_texto_completo else ""

    return {
        "contrato": "DocumentoBruto",
        "nome_ficheiro": documento.nome_ficheiro,
        "caminho": documento.caminho,
        "texto": texto,
        "numero_paginas": documento.numero_paginas,
        "origem": documento.origem,
        "tamanho_texto": len(documento.texto),
        "texto_preview": documento.texto[:500],
        "processado_em": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def nome_saida_documento_bruto(documento: DocumentoBruto) -> str:
    """Gera nome de arquivo para materialização auxiliar do DocumentoBruto.

    O sufixo .documento_bruto.json deixa claro que este arquivo é uma evidência
    da P1, não o JSON estruturado final da P2.
    """
    nome_base = Path(documento.nome_ficheiro).stem
    return f"{nome_base}.documento_bruto.json"
