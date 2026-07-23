"""[ENTREGA-3] Persistência da execução completa — Sandro Tarabay.

Propósito
---------
Costurar o treino (P5/P8) à inferência (P7). O `main.py` grava hoje apenas
`modelo/pesos.pth` e `modelo/configuracao.json`, sem manifesto — o que impede
o `MotorInferencia` de reconstruir a execução. Este módulo grava tudo na
estrutura da constituição §4 e emite o `manifesto.json`.

Quatro incompatibilidades resolvidas
------------------------------------
1. Prefixo do `state_dict`: o `main.py` grava a `RedeNeuronalClassificacao`
   nua (`camada1.weight`), mas o motor carrega para dentro do
   `ClassificadorMLP`, que a aninha em `self.rede` (`rede.camada1.weight`).
   Aqui gravamos já a partir do invólucro.
2. Nome do ficheiro: `configuracao.json` -> `configuracao_modelo.json`.
3. Chaves da configuração: escritas nas duas famílias (ver nota abaixo).
4. Ausência de `manifesto.json`.

Nota sobre as chaves duplicadas
-------------------------------
`especificacao_05` fixa `numero_entradas`/`numero_ocultas`/`numero_saidas`;
`ClassificadorMLP.de_configuracao` lê `dim_entrada`/`dim_oculta`/`num_classes`.
Escrevemos ambas como medida transitória, para desbloquear a integração sem
alterar ficheiros de outros responsáveis. Fica registada a necessidade de uma
decisão do responsável técnico (constituição §7) para convergir numa só
família e remover a redundância.

Contratos
---------
Entrada : rede treinada, vetorizador ajustado, dimensões, métricas opcionais.
Saída   : artefactos/<id_execucao>/ com modelo/, vetorizador/, categorias/,
          metricas.json e manifesto.json.

Erros
-----
`ValueError` — dimensões em falta ou vetorizador não ajustado.

Comandos
--------
    python -m unittest tests/test_persistencia_execucao.py -v
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import torch

from src.caracteristicas.vetorizador_tfidf import VetorizadorTfidfNumPy
from src.dados.manifesto import escrever_manifesto
from src.modelos.rede_neuronal import RedeNeuronalClassificacao
from src.treino.classificador_mlp import ClassificadorMLP

_registo = logging.getLogger(__name__)

_DIMENSOES_OBRIGATORIAS = ("numero_entradas", "numero_ocultas", "numero_saidas")


def _configuracao_do_modelo(
    dimensoes: dict[str, int],
    hiperparametros: dict[str, Any] | None,
) -> dict[str, Any]:
    """Constrói a configuração nas duas famílias de chaves (ver nota do módulo)."""
    em_falta = [chave for chave in _DIMENSOES_OBRIGATORIAS if chave not in dimensoes]
    if em_falta:
        raise ValueError(f"Dimensões em falta: {em_falta}")

    configuracao: dict[str, Any] = {
        # Família canónica da especificacao_05.
        "numero_entradas": int(dimensoes["numero_entradas"]),
        "numero_ocultas": int(dimensoes["numero_ocultas"]),
        "numero_saidas": int(dimensoes["numero_saidas"]),
        # Família lida por ClassificadorMLP.de_configuracao.
        "dim_entrada": int(dimensoes["numero_entradas"]),
        "dim_oculta": int(dimensoes["numero_ocultas"]),
        "num_classes": int(dimensoes["numero_saidas"]),
        "classe_modelo": "RedeNeuronalClassificacao",
        "invólucro": "ClassificadorMLP",
    }
    if hiperparametros:
        configuracao.update(hiperparametros)
    return configuracao


def guardar_execucao(
    id_execucao: str,
    rede: RedeNeuronalClassificacao,
    vetorizador: VetorizadorTfidfNumPy,
    dimensoes: dict[str, int],
    metricas: dict[str, Any] | None = None,
    hiperparametros: dict[str, Any] | None = None,
    semente: int = 42,
    pasta_artefactos: str | Path = "artefactos",
) -> Path:
    """Grava a execução completa e devolve a pasta criada.

    O `state_dict` é gravado a partir de `ClassificadorMLP(rede)` — e não da
    rede nua — para que as chaves tenham o prefixo `rede.` que o
    `MotorInferencia` espera ao reconstruir.
    """
    if not getattr(vetorizador, "esta_ajustado", False):
        raise ValueError("Vetorizador não ajustado; execute o fit antes de guardar.")

    pasta_execucao = Path(pasta_artefactos) / id_execucao
    (pasta_execucao / "modelo").mkdir(parents=True, exist_ok=True)
    (pasta_execucao / "vetorizador").mkdir(parents=True, exist_ok=True)
    (pasta_execucao / "categorias").mkdir(parents=True, exist_ok=True)

    # 1. Pesos, a partir do invólucro (resolve o prefixo `rede.`).
    envolvido = ClassificadorMLP(rede)
    envolvido.eval()
    caminho_pesos = pasta_execucao / "modelo" / "pesos.pth"
    torch.save(envolvido.state_dict(), caminho_pesos)

    # 2. Configuração do modelo.
    configuracao = _configuracao_do_modelo(dimensoes, hiperparametros)
    (pasta_execucao / "modelo" / "configuracao_modelo.json").write_text(
        json.dumps(configuracao, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 3. Vetorizador (vocabulário, IDF e mapas).
    vetorizador.guardar_artefactos(str(pasta_execucao / "vetorizador"))

    # 4. Categorias na localização canónica da constituição §4.
    mapa_id: dict[int, str] = getattr(vetorizador, "mapa_id_para_categoria", {}) or {}
    mapa_categoria: dict[str, int] = (
        getattr(vetorizador, "mapa_categoria_para_id", {}) or {}
    )
    (pasta_execucao / "categorias" / "id_para_categoria.json").write_text(
        json.dumps(
            {str(chave): valor for chave, valor in mapa_id.items()},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (pasta_execucao / "categorias" / "categoria_para_id.json").write_text(
        json.dumps(mapa_categoria, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 5. Métricas (informativo; o motor lê em modo passivo).
    conteudo_metricas: dict[str, Any] = dict(metricas) if metricas else {}
    conteudo_metricas.setdefault("macro_f1", None)
    conteudo_metricas.setdefault("macro_f1_referencia", None)
    (pasta_execucao / "metricas.json").write_text(
        json.dumps(conteudo_metricas, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 6. Manifesto — caminhos relativos à pasta da execução.
    escrever_manifesto(
        id_execucao,
        {
            "id_execucao": id_execucao,
            "semente": semente,
            "vetorizador": "vetorizador/vocabulario.json",
            "idf": "vetorizador/idf.npy",
            "categorias": "categorias/id_para_categoria.json",
            "configuracao_modelo": "modelo/configuracao_modelo.json",
            "pesos": "modelo/pesos.pth",
            "metricas": "metricas.json",
        },
        pasta_artefactos,
    )

    _registo.info(
        "Execução '%s' guardada em %s | entradas=%d | classes=%d",
        id_execucao,
        pasta_execucao,
        configuracao["numero_entradas"],
        configuracao["numero_saidas"],
    )
    return pasta_execucao
