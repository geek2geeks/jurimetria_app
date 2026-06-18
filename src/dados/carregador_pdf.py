"""Carregador incremental de PDFs em bruto.

Responsabilidade da P1:
- abrir arquivos PDF com pdfplumber;
- extrair o texto total;
- emitir DocumentoBruto sequencialmente com yield;
- registrar falhas sem interromper o processamento dos demais arquivos.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Iterator
from pathlib import Path

import pdfplumber

from src.dados.esquemas import DocumentoBruto

logger = logging.getLogger(__name__)


def _extrair_texto_pdf(caminho_pdf: Path) -> tuple[str, int]:
    """Extrai o texto de todas as páginas de um PDF.

    O separador "\f" é usado entre páginas para preservar uma referência
    simples de quebra de página, sem transformar o conteúdo em campos jurídicos.
    """
    textos_paginas: list[str] = []

    with pdfplumber.open(caminho_pdf) as pdf:
        numero_paginas = len(pdf.pages)

        for pagina in pdf.pages:
            # pdfplumber pode devolver None em páginas sem camada textual.
            # O "or ''" evita erro ao juntar textos depois.
            textos_paginas.append(pagina.extract_text() or "")

    texto_total = "".join(textos_paginas)
    return texto_total, numero_paginas


def carregar_pdfs(
    pasta: str | Path,
    *,
    registrar_falha: Callable[[Path, Exception], None] | None = None,
) -> Iterator[DocumentoBruto]:
    """Percorre PDFs de uma pasta e emite um DocumentoBruto por vez.

    O uso de yield é essencial para controlo de memória: em vez de carregar
    todos os documentos numa lista gigante, cada PDF é processado e entregue
    sequencialmente para a etapa seguinte.

    Args:
        pasta: Diretório de entrada com PDFs.
        registrar_falha: Callback opcional usado pelos scripts auxiliares para
            registrar falhas estruturadas em CSV/JSON/JSONL. Esse parâmetro não
            altera o contrato principal da P1, que continua sendo o yield de
            DocumentoBruto.
    """
    pasta_path = Path(pasta)

    for caminho_pdf in sorted(pasta_path.rglob("*.pdf")):
        try:
            texto, numero_paginas = _extrair_texto_pdf(caminho_pdf)

            documento = DocumentoBruto(
                nome_ficheiro=caminho_pdf.name,
                caminho=str(caminho_pdf),
                texto=texto,
                numero_paginas=numero_paginas,
                origem="pdf",
            )

            # Esta é a saída exigida pela especificação P1.
            yield documento

        except Exception as erro:
            # PDFs corrompidos ou ilegíveis não devem parar o ciclo.
            # O erro é registrado e o carregador segue para o próximo arquivo.
            logger.exception("Falha ao carregar PDF '%s': %s", caminho_pdf, erro)
            if registrar_falha is not None:
                registrar_falha(caminho_pdf, erro)
            continue


# Alias para compatibilidade com versões anteriores dos scripts.
iterar_pdfs = carregar_pdfs
