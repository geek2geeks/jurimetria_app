"""Registro estruturado de processamento da ingestão P1.

A saída oficial da P1 continua sendo `DocumentoBruto` emitido por `yield`.
Este módulo é uma melhoria complementar para registrar, em arquivos de log,
quais ficheiros foram processados com sucesso e quais falharam.

Os registros podem ser gravados em três formatos:
- CSV: bom para abrir em planilha;
- JSON: bom para inspecionar uma lista completa de registros;
- JSONL: bom para pipelines, pois cada linha é um registro independente.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from uuid import uuid4


StatusProcessamento = Literal["sucesso", "falha"]
OrigemProcessamento = Literal["pdf", "json"]


def agora_utc_iso() -> str:
    """Retorna a data/hora atual em UTC no formato ISO-8601."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(slots=True)
class RegistroProcessamento:
    """Representa um registro de log para um ficheiro processado.

    Cada instância descreve o resultado de um único arquivo: sucesso ou falha,
    origem, caminho, tamanho, páginas e mensagem de erro quando existir.
    """

    id_execucao: str
    nome_ficheiro: str
    caminho: str
    origem: OrigemProcessamento
    status: StatusProcessamento
    numero_paginas: int | None
    tamanho_texto: int
    tamanho_bytes: int | None
    data_hora_inicio: str
    data_hora_fim: str
    duracao_segundos: float
    motivo_falha: str
    mensagem_erro: str


def calcular_tamanho_bytes(caminho: str | Path) -> int | None:
    """Calcula o tamanho do arquivo em bytes quando o caminho existe."""
    try:
        return Path(caminho).stat().st_size
    except OSError:
        return None


def criar_registro_sucesso(
    *,
    caminho: str | Path,
    origem: OrigemProcessamento,
    numero_paginas: int | None,
    tamanho_texto: int,
    inicio: datetime,
) -> RegistroProcessamento:
    """Cria um registro de sucesso para um arquivo carregado pela P1."""
    fim = datetime.now(timezone.utc)
    caminho_path = Path(caminho)
    return RegistroProcessamento(
        id_execucao=str(uuid4()),
        nome_ficheiro=caminho_path.name,
        caminho=str(caminho_path),
        origem=origem,
        status="sucesso",
        numero_paginas=numero_paginas,
        tamanho_texto=tamanho_texto,
        tamanho_bytes=calcular_tamanho_bytes(caminho_path),
        data_hora_inicio=inicio.isoformat().replace("+00:00", "Z"),
        data_hora_fim=fim.isoformat().replace("+00:00", "Z"),
        duracao_segundos=round((fim - inicio).total_seconds(), 6),
        motivo_falha="",
        mensagem_erro="",
    )


def criar_registro_falha(
    *,
    caminho: str | Path,
    origem: OrigemProcessamento,
    inicio: datetime,
    erro: Exception,
    motivo_falha: str,
) -> RegistroProcessamento:
    """Cria um registro de falha sem interromper o ciclo de ingestão."""
    fim = datetime.now(timezone.utc)
    caminho_path = Path(caminho)
    return RegistroProcessamento(
        id_execucao=str(uuid4()),
        nome_ficheiro=caminho_path.name,
        caminho=str(caminho_path),
        origem=origem,
        status="falha",
        numero_paginas=None,
        tamanho_texto=0,
        tamanho_bytes=calcular_tamanho_bytes(caminho_path),
        data_hora_inicio=inicio.isoformat().replace("+00:00", "Z"),
        data_hora_fim=fim.isoformat().replace("+00:00", "Z"),
        duracao_segundos=round((fim - inicio).total_seconds(), 6),
        motivo_falha=motivo_falha,
        mensagem_erro=f"{type(erro).__name__}: {erro}",
    )


def salvar_registros(registros: list[RegistroProcessamento], pasta_logs: str | Path) -> None:
    """Salva os registros de processamento em CSV, JSON e JSONL.

    A pasta raiz informada é organizada automaticamente em:
    - `csv/log_ingestao.csv`;
    - `json/log_ingestao.json`;
    - `jsonl/log_ingestao.jsonl`.
    """
    pasta_logs = Path(pasta_logs)
    pasta_csv = pasta_logs / "csv"
    pasta_json = pasta_logs / "json"
    pasta_jsonl = pasta_logs / "jsonl"

    pasta_csv.mkdir(parents=True, exist_ok=True)
    pasta_json.mkdir(parents=True, exist_ok=True)
    pasta_jsonl.mkdir(parents=True, exist_ok=True)

    registros_dict = [asdict(registro) for registro in registros]

    with (pasta_json / "log_ingestao.json").open("w", encoding="utf-8") as ficheiro:
        json.dump(registros_dict, ficheiro, ensure_ascii=False, indent=2)

    with (pasta_jsonl / "log_ingestao.jsonl").open("w", encoding="utf-8") as ficheiro:
        for registro in registros_dict:
            ficheiro.write(json.dumps(registro, ensure_ascii=False) + "\n")

    campos = list(RegistroProcessamento.__dataclass_fields__.keys())
    with (pasta_csv / "log_ingestao.csv").open("w", encoding="utf-8", newline="") as ficheiro:
        escritor = csv.DictWriter(ficheiro, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(registros_dict)
