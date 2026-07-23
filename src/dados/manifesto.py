"""Módulo de manifesto — leitura e escrita de metadados de execução."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def escrever_manifesto(
    id_execucao: str,
    metadados: dict[str, Any],
    pasta_artefactos: str | Path
) -> Path:
    """Escreve os metadados de uma execução num ficheiro JSON.
    
    Adiciona um timestamp aos metadados antes de guardar.
    Cria a pasta se não existir.
    
    Args:
        id_execucao: Identificador da execução.
        metadados: Dicionário com a configuração e caminhos da execução.
        pasta_artefactos: Caminho base para os artefactos.
        
    Returns:
        Caminho para o ficheiro manifesto.json guardado.
    """
    pasta = Path(pasta_artefactos) / id_execucao
    pasta.mkdir(parents=True, exist_ok=True)
    
    # Criar uma cópia para não mutar o argumento
    dados_guardar = dict(metadados)
    if "timestamp" not in dados_guardar:
        dados_guardar["timestamp"] = datetime.now().isoformat()
        
    caminho_ficheiro = pasta / "manifesto.json"
    with open(caminho_ficheiro, "w", encoding="utf-8") as f:
        json.dump(dados_guardar, f, indent=4, ensure_ascii=False)
        
    return caminho_ficheiro


def ler_manifesto(
    id_execucao: str,
    pasta_artefactos: str | Path
) -> dict[str, Any]:
    """Lê os metadados de uma execução a partir do ficheiro JSON.
    
    Args:
        id_execucao: Identificador da execução.
        pasta_artefactos: Caminho base para os artefactos.
        
    Returns:
        Dicionário com os metadados lidos do ficheiro.
    """
    caminho_ficheiro = Path(pasta_artefactos) / id_execucao / "manifesto.json"
    
    with open(caminho_ficheiro, "r", encoding="utf-8") as f:
        return json.load(f)
