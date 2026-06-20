"""Adiciona um comentário de atualização às tarefas SCRUM-5..12 no Jira Cloud.

Revisão da Sprint 1 após a adoção da estratégia "JSON como source of truth" e
as correções de consistência. NÃO altera estados nem descrições: apenas
acrescenta um comentário (ação não destrutiva e com rasto de auditoria).

Modo predefinido: simulação (mostra o que seria enviado). Usa ``--aplicar``
depois de teres JIRA_BASE_URL, JIRA_EMAIL e JIRA_API_TOKEN no ``.env`` local
(ou nas variáveis de ambiente). O token nunca é escrito no código.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import urllib.error
import urllib.request

from dotenv import load_dotenv

# (chave Jira, pessoa, nota de atualização)
ATUALIZACOES: tuple[tuple[str, str, str], ...] = (
    (
        "SCRUM-5",
        "Alessandro (P1)",
        "Cada PDF tem um JSON irmao (extraction_success=true) que e a source of truth. "
        "Os teus carregadores tratam texto bruto; o JSON estruturado pertence ao adaptador da Daniela. "
        "Ja existe esquemas.py de referencia em src/dados/. Ver docs/esquema_json_corpus.md.",
    ),
    (
        "SCRUM-6",
        "Daniela (P2)",
        "Ja existem implementacoes de referencia de esquemas.py e carregador_acordaos_json.py em src/dados/ "
        "(rever e estender, ajustar campos so por acordo com o Pedro). Valida o teu parser de PDF contra o JSON "
        "irmao do mesmo documento, que serve de gabarito. Schema e mapeamento em docs/esquema_json_corpus.md.",
    ),
    (
        "SCRUM-7",
        "Gustavo (P3)",
        "A limpeza tem de tolerar o caractere de substituicao (U+FFFD) gravado no corpus. Usa a tabela-seed "
        "decisao->classe de docs/esquema_json_corpus.md (testa 'improcedente' antes de 'procedente'). "
        "Cerca de 9,5% das decisoes vem vazias: descartar do treino, nao mapear para OUTRA.",
    ),
    (
        "SCRUM-8",
        "Gleicy (P4)",
        "O texto de entrada (X) vem de Acordao.texto_caracteristicas() = descritores + sumario. O artefacto de "
        "configuracao do vetorizador chama-se configuracao.json (nao config.json). fit so no treino; transform no resto.",
    ),
    (
        "SCRUM-9",
        "Helton (P5)",
        "Requisito do enunciado (RF09): comparar pelo menos duas configuracoes (ex.: nº de camadas, ativacao ou "
        "batch size) e registar a curva de perda de cada uma. Guardar apenas state_dict em pesos.pth.",
    ),
    (
        "SCRUM-10",
        "Luciana (P6)",
        "Sem mudanca material. Manter Macro-F1 vs baseline de classe maioritaria como criterio (dados desequilibrados).",
    ),
    (
        "SCRUM-11",
        "Sandro (P7)",
        "A inferencia deve usar a MESMA composicao do treino: descritores + sumario (Acordao.texto_caracteristicas()) "
        "e a mesma limpeza do P3. Omitir os descritores degrada as caracteristicas face ao treino.",
    ),
    (
        "SCRUM-12",
        "Pedro (P8)",
        "esquemas.py de referencia disponivel para congelar; criados docs/criterios_avaliacao.md, "
        "docs/esquema_json_corpus.md e artefactos/exemplos/manifesto.exemplo.json. O construtor_registos usa a "
        "limpeza do P3 e a composicao canonica de X.",
    ),
)


def _comentario_adf(nota: str) -> dict:
    """Constrói o corpo do comentário em Atlassian Document Format (API v3)."""
    return {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "Atualizacao da Sprint 1 (estrategia JSON source-of-truth + correcoes): "},
                        {"type": "text", "text": nota},
                    ],
                }
            ],
        }
    }


def _cabecalhos(email: str, token: str) -> dict[str, str]:
    credenciais = base64.b64encode(f"{email}:{token}".encode("utf-8")).decode("ascii")
    return {
        "Authorization": f"Basic {credenciais}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aplicar", action="store_true", help="Enviar mesmo os comentários para o Jira.")
    argumentos = parser.parse_args()

    load_dotenv()
    url_base = os.getenv("JIRA_BASE_URL", "").rstrip("/")
    email = os.getenv("JIRA_EMAIL", "")
    token = os.getenv("JIRA_API_TOKEN", "")

    print("=== Atualização das tarefas Jira (SCRUM-5..12) ===\n")
    for chave, pessoa, nota in ATUALIZACOES:
        print(f"[{chave}] {pessoa}\n    {nota}\n")

    if not argumentos.aplicar:
        print("Modo simulação. Nada foi enviado. Usa --aplicar para escrever no Jira.")
        return 0

    if not (url_base and email and token):
        print(
            "ERRO: faltam credenciais. Define JIRA_BASE_URL, JIRA_EMAIL e JIRA_API_TOKEN "
            "no .env local antes de usar --aplicar (ou corre via MCP no Hermes)."
        )
        return 1

    cabecalhos = _cabecalhos(email, token)
    for chave, _pessoa, nota in ATUALIZACOES:
        url = f"{url_base}/rest/api/3/issue/{chave}/comment"
        dados = json.dumps(_comentario_adf(nota)).encode("utf-8")
        pedido = urllib.request.Request(url, data=dados, headers=cabecalhos, method="POST")
        try:
            with urllib.request.urlopen(pedido) as resposta:
                print(f"OK {chave}: {resposta.status}")
        except urllib.error.HTTPError as erro:
            print(f"FALHA {chave}: {erro.code} {erro.reason}")
        except urllib.error.URLError as erro:
            print(f"FALHA {chave}: {erro.reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
