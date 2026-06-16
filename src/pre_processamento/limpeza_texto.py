# -*- coding: utf-8 -*-
"""Modulo de limpeza de texto e normalizacao de categorias (P3)."""

import re
import string
import unicodedata


def remover_acentos(texto: str) -> str:
    """Remove diacriticos (acentos e cedilhas) de uma string.

    Args:
        texto: A string original.

    Returns:
        A string normalizada sem acentuacao.
    """
    texto_normalizado = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto_normalizado if not unicodedata.combining(c))


def limpar_texto(texto: str) -> str:
    """Limpa o ruido textual do sumario de um acordao.

    Remove marcas como "Powered by TCPDF", enderecos de e-mail, URLs,
    numeros de telefone, faxes, codigos postais e normaliza espacos.

    Args:
        texto: O texto em bruto a ser limpo.

    Returns:
        O texto limpo sem ruido e com espacamento normalizado.
    """
    if not texto:
        return ""

    # Remover caracteres de substituicao (mojibake)
    texto = texto.replace("\uFFFD", "")

    # 1. Remover Powered by TCPDF
    # Captura "Powered by TCPDF" e possivel link associado (ex: (www.tcpdf.org))
    tcpdf_padrao = re.compile(r'(?i)powered\s+by\s+tcpdf(?:\s*\(\s*www\.tcpdf\.org\s*\))?')
    texto = tcpdf_padrao.sub("", texto)

    # 2. Remover enderecos de e-mail
    email_padrao = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    texto = email_padrao.sub("", texto)

    # 3. Remover URLs e dominios .pt
    # Captura http/https, www, e dominios terminados em .pt
    url_padrao = re.compile(r'https?://[^\s()<>]+|www\.[^\s()<>]+|\b[a-zA-Z0-9.-]+\.pt\b')
    texto = url_padrao.sub("", texto)

    # 4. Remover telefones e faxes
    # Captura rotulos comuns como Tel, Telefone, Fax seguidos por numeros
    telefones_rotulos = re.compile(r'(?i)\b(?:tel(?:ef)?\.?|fax)\b:?\s*(?:\+351\s*)?(?:\d\s*[-.]?\s*){9,12}')
    texto = telefones_rotulos.sub("", texto)
    # Captura numeros soltos de 9 digitos que comecam por 2 ou 9 (padrao PT)
    telefones_soltos = re.compile(r'\b(?:\+351\s*)?(?:2\d|9[1236])(?:\s*[-.]?\s*\d){7}\b')
    texto = telefones_soltos.sub("", texto)

    # 5. Remover codigos postais (formatos XXXX-XXX)
    codigo_postal_padrao = re.compile(r'\b\d{4}-\d{3}\b')
    texto = codigo_postal_padrao.sub("", texto)

    # 6. Normalizar multiplos espacos, quebras de linha e tabulacoes
    texto = re.sub(r'\s+', " ", texto)

    return texto.strip()


def normalizar_categoria(decisao_bruta: str | None) -> str | None:
    """Normaliza a decisao em bruto para uma das 5 categorias regulamentadas.

    As categorias sao: MANTIDA, REVOGADA, ANULADA, NAO_CONHECIDA ou OUTRA.
    Caso nao seja reconhecida, devolve None.

    A ordem de correspondencia e estrita (NAO_CONHECIDA -> ANULADA -> MANTIDA ->
    REVOGADA -> OUTRA) conforme ADR-05.

    Args:
        decisao_bruta: O texto da decisao em bruto.

    Returns:
        A categoria normalizada ou None se nao reconhecida.
    """
    if not decisao_bruta:
        return None

    # 1. Higienizacao inicial
    decisao = decisao_bruta.lower()
    decisao = decisao.replace("\uFFFD", "")
    decisao = remover_acentos(decisao)

    # Substituir pontuacao por espacos
    tabela_pontuacao = str.maketrans(string.punctuation, " " * len(string.punctuation))
    decisao = decisao.translate(tabela_pontuacao)

    # Normalizar espacos
    decisao = " ".join(decisao.split())

    # 2. Definicao dos stems ordenados (conforme ADR-05)
    stems_nao_conhecida = [
        "tomar conhec", "conhec do recurso", "conhec do objecto", "rejei",
        "desert", "deserc", "extempor", "nao admit", "admiss", "negado seguimento"
    ]

    stems_anulada = [
        "anulad", "nulidad"
    ]

    stems_mantida = [
        "nega proviment", "negado proviment", "negou proviment", "negar proviment",
        "negad", "nao provido", "improced", "confirma", "mantid", "mantem", "manter",
        "indefer", "denegad", "desatend"
    ]

    stems_revogada = [
        "proviment", "provid", "proced", "concedid", "concede", "revoga",
        "alterad", "alterar", "reformad", "modificad", "deferid",
        "atendida a reclama", "autorizada a revis"
    ]

    stems_outra = [
        "extin", "prejudicad", "homolog", "sobrest", "apens", "habilita", "desist",
        "aclarad", "retific", "correc", "remet", "reenvio", "baixa",
        "prosseguimento", "dilig", "ordenad", "competn", "incompet", "declara",
        "jurisprud", "assento", "constituc", "suspens", "revis"
    ]

    # 3. Correspondencia ordenada (a primeira que casa ganha)
    for stem in stems_nao_conhecida:
        if stem in decisao:
            return "NAO_CONHECIDA"

    for stem in stems_anulada:
        if stem in decisao:
            return "ANULADA"

    for stem in stems_mantida:
        if stem in decisao:
            return "MANTIDA"

    for stem in stems_revogada:
        if stem in decisao:
            return "REVOGADA"

    for stem in stems_outra:
        if stem in decisao:
            return "OUTRA"

    return None
