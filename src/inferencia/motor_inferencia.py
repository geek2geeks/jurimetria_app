"""P7 — Motor de inferência (Sandro Tarabay / SCRUM-11)."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import numpy.typing as npt
import torch

from src.caracteristicas.vetorizador_tfidf import VetorizadorTfidfNumPy
from src.dados.esquemas import Acordao
from src.dados.manifesto import ler_manifesto
from src.inferencia.configuracao_gpu import configurar_dispositivo, preparar_modelo
from src.pre_processamento.limpeza_texto import limpar_texto
from src.treino.classificador_mlp import ClassificadorMLP

_registo = logging.getLogger(__name__)


@dataclass
class ResultadoInferencia:
    """Resultado tipado de uma previsão isolada."""

    categoria_prevista: str
    indice_previsto: int
    distribuicao: dict[str, float]
    termos_relevantes: list[str]
    excerto_sumario: str
    explicacao_gerada: str | None = None


class MotorInferencia:
    """Carrega uma execução treinada e classifica novos acórdãos."""

    def __init__(
        self,
        id_execucao: str,
        pasta_artefactos: str | Path = "artefactos",
    ) -> None:
        """Inicializa o motor carregando todos os artefactos pelo manifesto."""

        self.id_execucao: str = id_execucao
        self.pasta_artefactos: Path = Path(pasta_artefactos)
        self.pasta_execucao: Path = self.pasta_artefactos / id_execucao

        # 1. Manifesto — índice de todos os artefactos.
        manifesto: dict[str, object] = ler_manifesto(id_execucao, pasta_artefactos)

        semente_bruta: object = manifesto.get("semente", 42)
        self.semente: int = semente_bruta if isinstance(semente_bruta, int) else 42

        # 2. Vetorizador (vocabulário + IDF).
        pasta_vetorizador: Path = (
            self.pasta_execucao / Path(str(manifesto["vetorizador"])).parent
        )
        self.vetorizador: VetorizadorTfidfNumPy = VetorizadorTfidfNumPy.carregar(
            pasta_vetorizador
        )

        # 3. Mapa de categorias (índice int → nome str).
        mapa_bruto: dict[str, object] = json.loads(
            (self.pasta_execucao / str(manifesto["categorias"])).read_text(
                encoding="utf-8"
            )
        )
        self.id_para_categoria: dict[int, str] = {
            int(chave): str(valor) for chave, valor in mapa_bruto.items()
        }

        # 4. Modelo: reconstruir arquitetura → carregar pesos → eval → GPU/CPU.
        configuracao_modelo: dict[str, int] = json.loads(
            (self.pasta_execucao / str(manifesto["configuracao_modelo"])).read_text(
                encoding="utf-8"
            )
        )
        modelo_base: ClassificadorMLP = ClassificadorMLP.de_configuracao(
            configuracao_modelo
        )

        # 5. Métricas do treino (produzidas pelo P6) — informativo, leitura passiva.
        self.metricas_treino: dict[str, object] | None = None
        caminho_metricas: object = manifesto.get("metricas")
        if isinstance(caminho_metricas, str):
            try:
                self.metricas_treino = json.loads(
                    (self.pasta_execucao / caminho_metricas).read_text(encoding="utf-8")
                )
            except (FileNotFoundError, json.JSONDecodeError) as erro:
                _registo.warning(
                    "metricas.json não disponível (%s) — a continuar.", erro
                )

        # 6. Dispositivo (CPU ou GPU, conforme .env) — antes do load_state_dict.
        self.dispositivo: torch.device
        ids_gpu: list[int]
        self.dispositivo, ids_gpu = configurar_dispositivo()

        # 7. Carregar pesos → eval → DataParallel (se >1 GPU).
        estado: dict[str, torch.Tensor] = torch.load(
            self.pasta_execucao / str(manifesto["pesos"]),
            map_location=self.dispositivo,
        )
        modelo_base.load_state_dict(estado)
        self.modelo: torch.nn.Module = preparar_modelo(
            modelo_base, self.dispositivo, ids_gpu
        )
        self.modelo.eval()

        _registo.info(
            "Execução '%s' carregada | dispositivo=%s | classes=%d | vocabulário=%d",
            id_execucao,
            self.dispositivo,
            len(self.id_para_categoria),
            len(self.vetorizador.vocabulario),
        )

    def prever(
        self,
        acordao: Acordao,
        com_explicacao: bool = False,
    ) -> ResultadoInferencia:
        """Classifica um `Acordao` e devolve um `ResultadoInferencia`."""

        # Composição canónica da entrada — idêntica à do treino (evita skew).
        texto: str = limpar_texto(acordao.texto_caracteristicas())
        caracteristicas: npt.NDArray[np.float32] = self.vetorizador.transformar([texto])

        tensor_entrada: torch.Tensor = torch.from_numpy(caracteristicas).to(
            self.dispositivo
        )
        with torch.no_grad():
            logits: torch.Tensor = self.modelo(tensor_entrada)
            probabilidades: npt.NDArray[np.float32] = (
                torch.softmax(logits, dim=1).cpu().numpy()[0]
            )

        indice: int = int(np.argmax(probabilidades))
        categoria: str = self.id_para_categoria[indice]
        distribuicao: dict[str, float] = {
            self.id_para_categoria[i]: float(probabilidades[i])
            for i in range(len(probabilidades))
        }
        termos: list[str] = self._termos_relevantes(caracteristicas[0])
        excerto: str = (acordao.sumario or "").strip()[:400]
        explicacao: str | None = (
            self._explicar_offline(categoria, distribuicao, termos)
            if com_explicacao
            else None
        )

        return ResultadoInferencia(
            categoria_prevista=categoria,
            indice_previsto=indice,
            distribuicao=distribuicao,
            termos_relevantes=termos,
            excerto_sumario=excerto,
            explicacao_gerada=explicacao,
        )

    def _termos_relevantes(
        self,
        vetor: npt.NDArray[np.float32],  # shape (n_vocab,)
    ) -> list[str]:
        """Devolve os top-5 tokens por peso TF-IDF no vetor normalizado."""

        if float(vetor.sum()) <= 0.0:
            return []
        inverso: dict[int, str] = {
            idx: token for token, idx in self.vetorizador.vocabulario.items()
        }
        termos: list[str] = []
        for idx in np.argsort(vetor)[::-1][:5]:
            peso: float = float(vetor[idx])
            if peso > 0.0:
                termos.append(inverso[int(idx)])
        return termos

    def _explicar_offline(
        self,
        categoria: str,
        distribuicao: dict[str, float],
        termos: list[str],
    ) -> str:
        """Explicação determinística sem rede — fallback seguro do LLM."""

        confianca: float = distribuicao[categoria]
        partes: list[str] = [
            f"Classe prevista: {categoria} (confiança {confianca:.0%})."
        ]
        if termos:
            partes.append(
                "Termos com maior peso na decisão: " + ", ".join(termos) + "."
            )
        partes.append(
            "Explicação automática e aproximada; não constitui aconselhamento jurídico."
        )
        return " ".join(partes)
