"""Inspeciona uma amostra reprodutível de PDFs do corpus jurídico."""

from __future__ import annotations

import json
import os
import random
from pathlib import Path
from typing import Any

import pdfplumber


TRIBUNAIS = ("STJ", "STA", "TRL", "TRP", "TRC", "TRE", "TRG")
SEMENTE_AMOSTRA = 42
LIMITE_AMOSTRA = 15


def obter_diretoria_origem() -> Path:
    """Obtém a diretoria do corpus, mantendo compatibilidade com a configuração antiga."""
    caminho_configurado = os.getenv("PDF_DIRETORIA_ORIGEM") or os.getenv(
        "PDF_SOURCE_DIR",
        "data/raw",
    )
    return Path(caminho_configurado)


def selecionar_amostra_pdfs(diretoria_origem: Path) -> list[Path]:
    """Seleciona PDFs de vários tribunais e anos de forma reprodutível."""
    caminhos_pdf = list(diretoria_origem.rglob("*.pdf"))
    caminhos_por_tribunal: dict[str, list[Path]] = {
        tribunal: [] for tribunal in TRIBUNAIS
    }

    for caminho_pdf in caminhos_pdf:
        try:
            tribunal = caminho_pdf.relative_to(diretoria_origem).parts[0]
        except (ValueError, IndexError):
            continue

        amostra_tribunal = caminhos_por_tribunal.get(tribunal)
        if amostra_tribunal is not None and len(amostra_tribunal) < 50:
            amostra_tribunal.append(caminho_pdf)

    gerador_aleatorio = random.Random(SEMENTE_AMOSTRA)
    caminhos_selecionados: list[Path] = []
    for caminhos_tribunal in caminhos_por_tribunal.values():
        if caminhos_tribunal:
            quantidade = min(2, len(caminhos_tribunal))
            caminhos_selecionados.extend(
                gerador_aleatorio.sample(caminhos_tribunal, quantidade)
            )

    caminhos_antigos = [
        caminho
        for caminho in caminhos_pdf
        if "2008" in caminho.name or "2009" in caminho.name
    ]
    caminhos_recentes = [
        caminho
        for caminho in caminhos_pdf
        if "2024" in caminho.name or "2025" in caminho.name
    ]
    if caminhos_antigos:
        caminhos_selecionados.append(caminhos_antigos[0])
    if caminhos_recentes:
        caminhos_selecionados.append(caminhos_recentes[0])

    return list(dict.fromkeys(caminhos_selecionados))[:LIMITE_AMOSTRA]


def identificar_ano_no_nome(caminho_pdf: Path) -> str | None:
    """Extrai o primeiro ano com quatro algarismos do nome do ficheiro."""
    for parte_nome in caminho_pdf.name.split("_"):
        if parte_nome.isdigit() and len(parte_nome) == 4:
            return parte_nome
    return None


def criar_registo_inspecao(
    caminho_pdf: Path,
    diretoria_origem: Path,
) -> dict[str, Any]:
    """Cria o registo inicial de inspeção para um PDF."""
    return {
        "caminho": str(caminho_pdf),
        "tribunal": caminho_pdf.relative_to(diretoria_origem).parts[0],
        "ano_no_nome": identificar_ano_no_nome(caminho_pdf),
        "numero_paginas": 0,
        "tem_ecli": False,
        "tem_url": False,
        "tem_relator": False,
        "tem_numero_documento": False,
        "tem_data_acordao": False,
        "tem_meio_processual": False,
        "tem_decisao": False,
        "tem_descritores": False,
        "tem_sumario": False,
        "tem_decisao_integral": False,
        "tem_secao_decisao": False,
        "tem_marca_tcpdf": False,
        "tem_rodape_pagina": False,
        "tem_rodape_morada": False,
        "tem_rodape_email": False,
    }


def atualizar_indicadores_globais(
    registo_inspecao: dict[str, Any],
    texto_pagina: str,
) -> None:
    """Atualiza indicadores que podem aparecer em qualquer página."""
    texto_minusculas = texto_pagina.lower()
    registo_inspecao["tem_sumario"] |= "sumário:" in texto_minusculas
    registo_inspecao["tem_decisao_integral"] |= (
        "decisão integral:" in texto_minusculas
    )
    registo_inspecao["tem_marca_tcpdf"] |= "powered by tcpdf" in texto_minusculas
    registo_inspecao["tem_rodape_morada"] |= (
        "rua duque de palmela" in texto_minusculas
    )
    registo_inspecao["tem_rodape_email"] |= (
        "csm@csm.org.pt" in texto_minusculas
    )
    registo_inspecao["tem_rodape_pagina"] |= (
        "página" in texto_minusculas and "/" in texto_minusculas
    )


def inspecionar_pdf(
    caminho_pdf: Path,
    diretoria_origem: Path,
) -> dict[str, Any]:
    """Inspeciona os campos e marcadores textuais de um PDF."""
    registo_inspecao = criar_registo_inspecao(
        caminho_pdf,
        diretoria_origem,
    )

    try:
        with pdfplumber.open(caminho_pdf) as documento_pdf:
            registo_inspecao["numero_paginas"] = len(documento_pdf.pages)
            if not documento_pdf.pages:
                return registo_inspecao

            texto_primeira_pagina = documento_pdf.pages[0].extract_text() or ""
            primeira_pagina_minusculas = texto_primeira_pagina.lower()
            registo_inspecao["tem_ecli"] = "ecli:pt:" in primeira_pagina_minusculas
            registo_inspecao["tem_url"] = (
                "http" in primeira_pagina_minusculas
                and "csm.org.pt" in primeira_pagina_minusculas
            ) or "jurisprudencia.csm.org.pt" in primeira_pagina_minusculas
            registo_inspecao["tem_relator"] = (
                "relator" in primeira_pagina_minusculas
            )
            registo_inspecao["tem_numero_documento"] = (
                "nº do documento" in primeira_pagina_minusculas
                or "nº convencional" in primeira_pagina_minusculas
            )
            registo_inspecao["tem_data_acordao"] = (
                "data do acórdão" in primeira_pagina_minusculas
            )
            registo_inspecao["tem_meio_processual"] = (
                "meio processual" in primeira_pagina_minusculas
            )
            registo_inspecao["tem_decisao"] = (
                "decisão:" in primeira_pagina_minusculas
                or "\ndecisão" in primeira_pagina_minusculas
            )
            registo_inspecao["tem_descritores"] = (
                "descritores" in primeira_pagina_minusculas
            )

            for pagina in documento_pdf.pages:
                atualizar_indicadores_globais(
                    registo_inspecao,
                    pagina.extract_text() or "",
                )

            texto_ultima_pagina = documento_pdf.pages[-1].extract_text() or ""
            ultima_pagina_minusculas = texto_ultima_pagina.lower()
            registo_inspecao["tem_secao_decisao"] = any(
                marcador in ultima_pagina_minusculas
                for marcador in ("iii - decisão", "iii – decisão", "decisão")
            )
    except Exception as erro:
        registo_inspecao["erro"] = str(erro)

    return registo_inspecao


def obter_caminho_relatorio() -> Path:
    """Obtém o caminho do relatório sem quebrar a variável de ambiente antiga."""
    caminho_configurado = os.getenv("PDF_CAMINHO_RELATORIO") or os.getenv(
        "PDF_INSPECTION_OUTPUT",
        "relatorio_inspecao_pdfs.json",
    )
    return Path(caminho_configurado)


def guardar_relatorio(
    registos_inspecao: list[dict[str, Any]],
    caminho_relatorio: Path,
) -> None:
    """Guarda os resultados da inspeção num ficheiro JSON."""
    caminho_relatorio.write_text(
        json.dumps(registos_inspecao, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def executar() -> None:
    """Executa a seleção, inspeção e gravação do relatório."""
    diretoria_origem = obter_diretoria_origem()
    print("A procurar PDFs...")
    caminhos_selecionados = selecionar_amostra_pdfs(diretoria_origem)
    registos_inspecao = [
        inspecionar_pdf(caminho_pdf, diretoria_origem)
        for caminho_pdf in caminhos_selecionados
    ]
    caminho_relatorio = obter_caminho_relatorio()
    guardar_relatorio(registos_inspecao, caminho_relatorio)
    print(f"Inspeção concluída. Relatório guardado em {caminho_relatorio}")


if __name__ == "__main__":
    executar()
