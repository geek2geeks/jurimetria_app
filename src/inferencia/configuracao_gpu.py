"""Configuração de GPU(s) NVIDIA para o projeto JurisTriage PT."""

from __future__ import annotations

import logging
import os

import torch
import torch.nn as nn

_registo = logging.getLogger(__name__)


def _ids_dispositivos(valor: str, num: int) -> list[int]:
    """Converte a variável GPU_DISPOSITIVOS numa lista de IDs inteiros."""

    if valor.lower() == "auto":
        return list(range(num))
    partes: list[str] = [p.strip() for p in valor.split(",") if p.strip()]
    return [int(p) for p in partes[:num]]


def configurar_dispositivo() -> tuple[torch.device, list[int]]:
    """Devolve (dispositivo_principal, lista_de_ids_gpu)."""

    habilitada: bool = os.environ.get("GPU_HABILITADA", "false").lower() == "true"

    if not habilitada:
        _registo.info("GPU_HABILITADA=false → a usar CPU.")
        return torch.device("cpu"), []

    if not torch.cuda.is_available():
        _registo.warning("GPU_HABILITADA=true mas CUDA não está disponível → CPU.")
        return torch.device("cpu"), []

    gpus_disponiveis: int = torch.cuda.device_count()
    num_pedido: int = int(os.environ.get("GPU_NUM_DISPOSITIVOS", "1"))
    num_usar: int = min(num_pedido, gpus_disponiveis)

    if num_usar < num_pedido:
        _registo.warning(
            "Pediu %d GPU(s) mas só há %d disponível(eis); a usar %d.",
            num_pedido,
            gpus_disponiveis,
            num_usar,
        )

    valor_ids: str = os.environ.get("GPU_DISPOSITIVOS", "auto")
    ids: list[int] = _ids_dispositivos(valor_ids, num_usar)

    dispositivo_principal: torch.device = torch.device(f"cuda:{ids[0]}")
    nomes: list[str] = [torch.cuda.get_device_name(i) for i in ids]
    _registo.info(
        "GPU(s) em uso: %s → %s",
        ids,
        " | ".join(nomes),
    )
    return dispositivo_principal, ids


def preparar_modelo(
    modelo: nn.Module,
    dispositivo: torch.device,
    ids_gpu: list[int],
) -> nn.Module:
    """Move o modelo para o dispositivo e aplica DataParallel se >1 GPU."""

    modelo = modelo.to(dispositivo)
    if len(ids_gpu) > 1:
        modelo = nn.DataParallel(modelo, device_ids=ids_gpu)
        _registo.info("DataParallel activo em %d GPU(s): %s", len(ids_gpu), ids_gpu)
    return modelo
