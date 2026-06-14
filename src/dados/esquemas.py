"""Contratos de dados internos do JurisTriage PT.

Estes três contratos são a "linguagem comum" do projeto (constituição §3) e
copropriedade de Pedro (P8) e Daniela (P2). Nenhuma alteração de campos deve
ser feita sem acordo dos dois (constituição §7).

Fluxo:
    DocumentoBruto -> Acordao -> RegistoClassificacao

Regra de fuga de informação (constituição §5, ADR-02):
    As ÚNICAS fontes de texto autorizadas para as características (X) são
    `descritores` e `sumario`. Os campos `ecli`, `url`, `tribunal`,
    `texto_integral` e `decisao_bruta` revelam (ou ajudam a revelar) a
    resposta e NUNCA podem entrar na matriz de características.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# Campos do Acordao proibidos como característica (X). Documentado aqui para
# que P4 (vetorização) e P8 (construtor) possam validar programaticamente.
CAMPOS_FUGA_INFORMACAO: tuple[str, ...] = (
    "ecli",
    "url",
    "tribunal",
    "texto_integral",
    "decisao_bruta",
)


@dataclass
class DocumentoBruto:
    """Documento acabado de carregar, antes da análise de metadados (P1)."""

    nome_ficheiro: str
    caminho: str
    texto: str
    numero_paginas: int
    origem: str  # "pdf" ou "json"


@dataclass
class Acordao:
    """Acórdão estruturado — contrato central (P2).

    A partir do P2, todo o projeto consome `Acordao`, independentemente de a
    fonte ter sido um PDF (parsing posicional) ou um JSON (adaptador).
    """

    # --- Identificação / metadados ---
    ecli: str | None = None  # LEAKAGE: contém o código do tribunal
    url: str | None = None  # LEAKAGE
    tribunal: str | None = None  # LEAKAGE (court_code do JSON)
    ano: int | None = None
    relator: str | None = None
    numero_documento: str | None = None
    data_acordao: str | None = None
    meio_processual: str | None = None
    votacao: str | None = None
    area_tematica: str | None = None
    # --- Fontes de características (X) ---
    descritores: list[str] = field(default_factory=list)  # X
    sumario: str | None = None  # X
    # --- Alvo (Y) e texto sensível ---
    decisao_bruta: str | None = None  # origem do rótulo Y; LEAKAGE como X
    texto_integral: str | None = None  # LEAKAGE (decisão dispositiva)
    # --- Proveniência ---
    origem: str = "json"  # "pdf" ou "json"
    extracao_bem_sucedida: bool = True

    def texto_caracteristicas(self) -> str:
        """Composição canónica do texto de entrada do modelo (X).

        Fonte única de verdade para o que vira características, partilhada por
        treino (P4) e inferência (P7) para evitar desalinhamento entre as duas
        fases. Junta os `descritores` e o `sumario`; nunca inclui campos de
        fuga de informação. O texto devolvido ainda deve passar pela limpeza
        do P3 antes da vetorização.
        """
        partes: list[str] = []
        if self.descritores:
            partes.append(" ; ".join(self.descritores))
        if self.sumario:
            partes.append(self.sumario)
        return " ".join(partes).strip()


@dataclass
class RegistoClassificacao:
    """Registo pronto para aprendizagem automática (construído pelo P8).

    `texto` já está limpo (P3) e contém apenas características autorizadas.
    `categoria_normalizada` é o rótulo Y (uma das cinco classes).
    `tribunal`/`ano` são metadados de análise de erros, NUNCA características.
    """

    id_documento: str
    texto: str
    categoria_normalizada: str
    tribunal: str | None = None
    ano: int | None = None
