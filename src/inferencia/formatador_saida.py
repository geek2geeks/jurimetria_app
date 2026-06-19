"""Formatadores da saída da inferência (Sandro / SCRUM-11, vertente "Could Have")."""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.inferencia.motor_inferencia import ResultadoInferencia

_registo = logging.getLogger(__name__)

AVISO_NAO_JURIDICO = (
    "Explicação automática e aproximada; não constitui aconselhamento jurídico."
)


# ----------------------------------------------------------------------------
# 1) Leitura de .env (sem depender do pacote python-dotenv — fica auto-contido)
# ----------------------------------------------------------------------------
def carregar_dotenv(caminho: str | Path = ".env") -> None:
    """Carrega `.env` para `os.environ` (não sobrepõe variáveis já definidas)."""

    ficheiro = Path(caminho)
    if not ficheiro.exists():
        _registo.debug(
            "Ficheiro .env não encontrado em %s; a usar só o ambiente.", ficheiro
        )
        return
    for linha in ficheiro.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, _, valor = linha.partition("=")
        chave = chave.strip()
        valor = valor.strip().strip('"').strip("'")
        os.environ.setdefault(chave, valor)


# ----------------------------------------------------------------------------
# 2) Configuração (estrutura imutável, lida do ambiente)
# ----------------------------------------------------------------------------
@dataclass(frozen=True)
class ConfiguracaoSaida:
    """Decisões de saída (explicação e formato) lidas do ambiente."""

    usar_llm: bool
    formato: str  # "texto" | "markdown" | "json"
    url_base: str
    modelo: str
    chave_api: str | None
    tempo_limite_segundos: int

    @classmethod
    def a_partir_do_ambiente(cls) -> "ConfiguracaoSaida":
        formato = os.environ.get("FORMATO_SAIDA", "texto").lower()
        if formato not in {"texto", "markdown", "json"}:
            _registo.warning("FORMATO_SAIDA='%s' inválido; a usar 'texto'.", formato)
            formato = "texto"
        return cls(
            usar_llm=os.environ.get("EXPLICACAO_VIA_LLM", "false").lower() == "true",
            formato=formato,
            url_base=os.environ.get(
                "DEEPSEEK_URL_BASE", "https://openrouter.ai"
            ).rstrip("/"),
            modelo=os.environ.get("DEEPSEEK_MODELO", "deepseek/deepseek-v4-flash"),
            chave_api=os.environ.get("DEEPSEEK_CHAVE_API"),
            tempo_limite_segundos=int(
                os.environ.get("LLM_TEMPO_LIMITE_SEGUNDOS", "20")
            ),
        )


# ----------------------------------------------------------------------------
# 3) Explicação OFFLINE (sem rede, determinística) — fallback seguro
# ----------------------------------------------------------------------------
def explicar_offline(
    resultado: "ResultadoInferencia", termos_relevantes: list[str]
) -> str:
    """Versão local da explicação, sem rede; é também o fallback do LLM."""
    confianca = resultado.distribuicao[resultado.categoria_prevista]
    partes = [
        f"Classe prevista: {resultado.categoria_prevista} (confiança {confianca:.0%})."
    ]
    if termos_relevantes:
        partes.append(
            "Termos com maior peso na decisão: " + ", ".join(termos_relevantes) + "."
        )
    partes.append(AVISO_NAO_JURIDICO)
    return " ".join(partes)


# ----------------------------------------------------------------------------
# 4) Explicação via LLM (OpenRouter / DeepSeek) — opt-in
# ----------------------------------------------------------------------------
def explicar_via_llm(
    resultado: "ResultadoInferencia",
    termos_relevantes: list[str],
    sumario_excerto: str,
    configuracao: ConfiguracaoSaida,
) -> str:
    """Pede ao LLM uma frase em português; em caso de falha cai para offline."""

    try:
        import requests  # noqa: WPS433 — import local, só quando o LLM é usado
    except ImportError:
        _registo.warning("`requests` não está instalado; a usar explicação offline.")
        return explicar_offline(resultado, termos_relevantes)

    if not configuracao.chave_api:
        _registo.warning("DEEPSEEK_CHAVE_API ausente; a usar explicação offline.")
        return explicar_offline(resultado, termos_relevantes)

    instrucao_sistema = (
        "És um redator jurídico-técnico. Escreve em português de Portugal, "
        "em 2 a 3 frases curtas, explicando a classe prevista para um sumário "
        "de acórdão e os termos com mais peso. Não invoques jurisprudência. "
        "Termina sempre com: '" + AVISO_NAO_JURIDICO + "'"
    )
    contexto = {
        "categoria_prevista": resultado.categoria_prevista,
        "distribuicao": {k: round(v, 3) for k, v in resultado.distribuicao.items()},
        "termos_relevantes": termos_relevantes,
        "excerto_sumario": sumario_excerto[:400],  # limita o que sai
    }
    corpo = {
        "model": configuracao.modelo,
        "messages": [
            {"role": "system", "content": instrucao_sistema},
            {"role": "user", "content": json.dumps(contexto, ensure_ascii=False)},
        ],
        "temperature": 0.2,
    }
    cabecalhos = {
        "Authorization": f"Bearer {configuracao.chave_api}",
        "Content-Type": "application/json",
    }
    url = f"{configuracao.url_base}/api/v1/chat/completions"

    try:
        resposta = requests.post(
            url,
            headers=cabecalhos,
            json=corpo,
            timeout=configuracao.tempo_limite_segundos,
        )
        resposta.raise_for_status()
        dados = resposta.json()
        texto = str(dados["choices"][0]["message"]["content"]).strip()
        if AVISO_NAO_JURIDICO not in texto:
            texto = f"{texto} {AVISO_NAO_JURIDICO}"
        return texto
    except Exception as erro:  # noqa: BLE001 — qualquer falha cai para offline
        _registo.warning("Chamada ao LLM falhou (%s); a usar explicação offline.", erro)
        return explicar_offline(resultado, termos_relevantes)


# ----------------------------------------------------------------------------
# 5) Formatação (layout) — terminal, markdown ou JSON
# ----------------------------------------------------------------------------
def formatar(resultado: "ResultadoInferencia", explicacao: str, formato: str) -> str:
    """Embrulha o resultado no formato pedido."""
    if formato == "json":
        return json.dumps(
            {
                "categoria_prevista": resultado.categoria_prevista,
                "indice_previsto": resultado.indice_previsto,
                "distribuicao": {
                    k: round(v, 4) for k, v in resultado.distribuicao.items()
                },
                "explicacao": explicacao,
            },
            ensure_ascii=False,
            indent=2,
        )
    if formato == "markdown":
        linhas_distribuicao = "\n".join(
            f"| {classe} | {prob:.2%} |"
            for classe, prob in resultado.distribuicao.items()
        )
        return (
            f"### Resultado da inferência\n\n"
            f"**Classe prevista:** `{resultado.categoria_prevista}`  \n"
            f"**Índice:** {resultado.indice_previsto}\n\n"
            f"**Distribuição:**\n\n"
            f"| Classe | Probabilidade |\n|---|---|\n{linhas_distribuicao}\n\n"
            f"**Explicação:** {explicacao}\n"
        )
    # texto (padrão)
    linhas = [
        "================ Resultado da inferência ================",
        f"Classe prevista : {resultado.categoria_prevista} (índice {resultado.indice_previsto})",
        "Distribuição    :",
    ]
    for classe, prob in resultado.distribuicao.items():
        linhas.append(f"  - {classe:<15} {prob:.2%}")
    linhas.append("")
    linhas.append(f"Explicação      : {explicacao}")
    linhas.append("=========================================================")
    return "\n".join(linhas)
