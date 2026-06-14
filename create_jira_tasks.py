"""Cria as tarefas iniciais do JurisTriage PT no Jira Cloud.

O modo predefinido apenas mostra o que seria criado. Usa ``--apply`` depois de
configurar um token novo no ficheiro local ``.env``.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


REPOSITORY_URL = "https://github.com/geek2geeks/jurimetria_app"
TASK_LABEL = "juristriage-sprint-1"


@dataclass(frozen=True)
class JiraTask:
    """Definição local de uma tarefa e do respetivo responsável."""

    person: str
    summary: str
    spec_path: str
    details: str


TASKS = (
    JiraTask(
        "Alessandro",
        "JurisTriage P1 - Ingestão de dados PDF e JSON em bruto",
        "docs/specs/spec_01_alessandro_ingestao.md",
        "Implementar carregadores incrementais de PDF e JSON que devolvam objetos RawDocument.",
    ),
    JiraTask(
        "Daniela",
        "JurisTriage P2 - Análise posicional, esquemas e adaptação JSON",
        "docs/specs/spec_02_daniela_dataprep.md",
        "Definir os contratos de dados com Pedro e converter as diferentes fontes para Acordao.",
    ),
    JiraTask(
        "Gustavo",
        "JurisTriage P3 - Limpeza de texto e normalização de categorias",
        "docs/specs/spec_03_gustavo_nlp.md",
        "Limpar os descritores e o sumário e normalizar a categoria de decisão aprovada.",
    ),
    JiraTask(
        "Gleicy",
        "JurisTriage P4 - Vetorização TF-IDF e divisão dos dados com NumPy",
        "docs/specs/spec_04_gleicy_numpy.md",
        "Implementar a divisão entre treino e teste e a vetorização TF-IDF sem usar scikit-learn para criar variáveis.",
    ),
    JiraTask(
        "Helton",
        "JurisTriage P5 - Modelo e treino com PyTorch",
        "docs/specs/spec_05_helton_pytorch.md",
        "Implementar a rede neuronal, o treino e a serialização dos pesos através de state_dict.",
    ),
    JiraTask(
        "Luciana",
        "JurisTriage P6 - Modelo de referência, métricas e avaliação",
        "docs/specs/spec_06_luciana_mlops_baseline.md",
        "Comparar o modelo com um modelo de referência e exportar as métricas de avaliação.",
    ),
    JiraTask(
        "Sandro",
        "JurisTriage P7 - Inferência e modelo de linguagem opcional",
        "docs/specs/spec_07_sandro_mlops_llm.md",
        "Criar inferência local orientada pelo manifesto; o modelo de linguagem é apenas opcional.",
    ),
    JiraTask(
        "Pedro",
        "JurisTriage P8 - Integração, qualidade, CI e manifesto",
        "docs/specs/spec_08_pedro_scrum_lead.md",
        "Proteger os contratos de dados, integrar o fluxo de processamento, manter a CI e produzir os manifestos.",
    ),
)


def adf_description(task: JiraTask) -> dict[str, Any]:
    """Cria uma descrição Atlassian Document Format para a API Jira v3."""

    spec_url = f"{REPOSITORY_URL}/blob/main/{task.spec_path}"
    paragraphs = (
        f"Objetivo: {task.details}",
        f"Responsável: {task.person}.",
        f"Especificação: {spec_url}",
        "Fluxo de trabalho: esclarecer, planear, analisar, implementar, testar e abrir um pedido de integração (PR).",
        "O apoio de IA deve ser declarado no PR. Todo o código deve ser compreendido, testado e sujeito a validação humana.",
    )
    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": paragraph}],
            }
            for paragraph in paragraphs
        ],
    }


class JiraClient:
    """Cliente mínimo para pesquisa e criação idempotente de tarefas."""

    def __init__(self, base_url: str, email: str, token: str) -> None:
        self.base_url = base_url.rstrip("/")
        encoded = base64.b64encode(f"{email}:{token}".encode("utf-8")).decode("ascii")
        self.headers = {
            "Authorization": f"Basic {encoded}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        """Executa um pedido Jira e devolve a resposta JSON."""

        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=data,
            headers=self.headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read().decode("utf-8")
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Jira devolveu HTTP {error.code}: {detail}") from error
        except urllib.error.URLError as error:
            raise RuntimeError(f"Nao foi possivel contactar o Jira: {error.reason}") from error

    def find_issue(self, project_key: str, summary: str) -> str | None:
        """Procura uma tarefa existente com o mesmo resumo."""

        escaped_summary = summary.replace('"', '\\"')
        jql = (
            f'project = "{project_key}" AND labels = "{TASK_LABEL}" '
            f'AND summary ~ "\\"{escaped_summary}\\""'
        )
        query = urllib.parse.urlencode(
            {"jql": jql, "fields": "key,summary", "maxResults": 50}
        )
        result = self.request("GET", f"/rest/api/3/search/jql?{query}")
        for issue in result.get("issues", []):
            if issue.get("fields", {}).get("summary") == summary:
                return str(issue["key"])
        return None

    def find_assignable_users(
        self,
        project_key: str,
        query_text: str,
    ) -> list[dict[str, Any]]:
        """Procura utilizadores que podem receber tarefas no projeto."""

        query = urllib.parse.urlencode(
            {
                "project": project_key,
                "query": query_text,
                "maxResults": 50,
            }
        )
        result = self.request(
            "GET",
            f"/rest/api/3/user/assignable/search?{query}",
        )
        if not isinstance(result, list):
            raise RuntimeError("O Jira devolveu um formato inesperado ao procurar utilizadores.")
        return result

    def create_issue(
        self,
        project_key: str,
        task: JiraTask,
        assignee_account_id: str,
    ) -> str:
        """Cria uma tarefa atribuída e devolve a chave Jira."""

        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": task.summary,
                "description": adf_description(task),
                "issuetype": {"name": "Task"},
                "labels": [TASK_LABEL, f"juristriage-p{TASKS.index(task) + 1}"],
                "assignee": {"accountId": assignee_account_id},
            }
        }
        result = self.request("POST", "/rest/api/3/issue", payload)
        return str(result["key"])


def load_assignees(path: Path) -> dict[str, str]:
    """Lê o mapa local Pessoa -> Atlassian accountId."""

    if not path.exists():
        return {}
    content = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(content, dict):
        raise ValueError("O ficheiro de responsaveis deve conter um objeto JSON.")
    return {str(name): str(account_id) for name, account_id in content.items()}


def load_members(path: Path) -> dict[str, str]:
    """Lê o mapa local Pessoa -> email da conta Atlassian."""

    if not path.exists():
        raise FileNotFoundError(
            f"Ficheiro de membros não encontrado: {path}. "
            "Cria-o a partir de jira_members.example.json."
        )
    content = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(content, dict):
        raise ValueError("O ficheiro de membros deve conter um objeto JSON.")
    return {str(name): str(email) for name, email in content.items()}


def resolve_assignees(
    client: JiraClient,
    project_key: str,
    members: dict[str, str],
) -> dict[str, str]:
    """Resolve emails para accountIds, exigindo um resultado inequívoco."""

    resolved: dict[str, str] = {}
    for task in TASKS:
        email = members.get(task.person, "").strip()
        if not email:
            raise ValueError(f"Falta o email Atlassian de {task.person}.")
        users = client.find_assignable_users(project_key, email)
        exact = [
            user
            for user in users
            if str(user.get("emailAddress", "")).casefold() == email.casefold()
        ]
        candidates = exact or users
        if len(candidates) != 1:
            raise RuntimeError(
                f"Não foi possível identificar {task.person} de forma inequívoca "
                f"com o email {email}. Resultados: {len(candidates)}."
            )
        account_id = str(candidates[0].get("accountId", "")).strip()
        if not account_id:
            raise RuntimeError(f"O Jira não devolveu accountId para {task.person}.")
        resolved[task.person] = account_id
        print(f"Resolvido: {task.person}")
    return resolved


def parse_args() -> argparse.Namespace:
    """Lê os argumentos da linha de comandos."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Cria tarefas reais. Sem esta opção, apenas simula.",
    )
    parser.add_argument(
        "--assignees",
        type=Path,
        default=None,
        help="JSON local com o mapa Pessoa -> Atlassian accountId.",
    )
    parser.add_argument(
        "--members",
        type=Path,
        default=None,
        help="JSON local com o mapa Pessoa -> email Atlassian.",
    )
    parser.add_argument(
        "--resolve-assignees",
        action="store_true",
        help="Resolve emails para accountIds e grava o ficheiro local de responsáveis.",
    )
    return parser.parse_args()


def main() -> int:
    """Valida a configuração e cria apenas as tarefas ainda inexistentes."""

    load_dotenv()
    args = parse_args()
    project_key = os.getenv("JIRA_PROJECT_KEY", "SCRUM")
    assignee_path = args.assignees or Path(
        os.getenv("JIRA_ASSIGNEES_FILE", "jira_assignees.json")
    )
    member_path = args.members or Path(
        os.getenv("JIRA_MEMBERS_FILE", "jira_members.json")
    )
    assignees = load_assignees(assignee_path)

    base_url = os.getenv("JIRA_BASE_URL", "")
    email = os.getenv("JIRA_EMAIL", "")
    token = os.getenv("JIRA_API_TOKEN", "")
    if args.resolve_assignees or args.apply:
        if not base_url or not email or not token:
            print(
                "Define JIRA_BASE_URL, JIRA_EMAIL e JIRA_API_TOKEN no .env local.",
                file=sys.stderr,
            )
            return 2

    client = JiraClient(base_url, email, token) if base_url and email and token else None
    if args.resolve_assignees:
        assert client is not None
        members = load_members(member_path)
        assignees = resolve_assignees(client, project_key, members)
        assignee_path.write_text(
            json.dumps(assignees, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"AccountIds gravados localmente em {assignee_path}.")

    missing = [task.person for task in TASKS if not assignees.get(task.person)]

    print(f"Projeto Jira: {project_key}")
    print(f"Modo: {'APLICAR' if args.apply else 'SIMULACAO'}")
    for task in TASKS:
        status = "atribuicao configurada" if task.person in assignees else "sem accountId"
        print(f"- {task.person}: {task.summary} ({status})")

    if not args.apply:
        print("Nenhuma alteracao foi enviada ao Jira. Usa --apply depois da validacao.")
        return 0

    if missing:
        print(
            "Faltam accountIds Atlassian para: " + ", ".join(missing),
            file=sys.stderr,
        )
        return 2

    assert client is not None
    for task in TASKS:
        existing = client.find_issue(project_key, task.summary)
        if existing:
            print(f"Ja existe: {existing} - {task.summary}")
            continue
        key = client.create_issue(project_key, task, assignees[task.person])
        print(f"Criada: {key} - {task.summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
