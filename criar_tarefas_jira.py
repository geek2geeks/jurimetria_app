"""Cria as tarefas iniciais do JurisTriage PT no Jira Cloud.

O modo predefinido apenas mostra o que seria criado. Usa ``--aplicar`` depois de
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


URL_REPOSITORIO = "https://github.com/geek2geeks/jurimetria_app"
ETIQUETA_TAREFAS = "juristriage-sprint-1"


@dataclass(frozen=True)
class TarefaJira:
    """Definição local de uma tarefa e do respetivo responsável."""

    pessoa: str
    titulo: str
    caminho_especificacao: str
    objetivo: str


TAREFAS = (
    TarefaJira(
        "Alessandro",
        "JurisTriage P1 - Ingestão de dados PDF e JSON em bruto",
        "docs/especificacoes/especificacao_01_alessandro_ingestao.md",
        "Implementar carregadores incrementais de PDF e JSON que devolvam objetos DocumentoBruto.",
    ),
    TarefaJira(
        "Daniela",
        "JurisTriage P2 - Análise posicional, esquemas e adaptação JSON",
        "docs/especificacoes/especificacao_02_daniela_metadados.md",
        "Definir os contratos de dados com Pedro e converter as diferentes fontes para Acordao.",
    ),
    TarefaJira(
        "Gustavo",
        "JurisTriage P3 - Limpeza de texto e normalização de categorias",
        "docs/especificacoes/especificacao_03_gustavo_limpeza_texto.md",
        "Limpar os descritores e o sumário e normalizar a categoria de decisão aprovada.",
    ),
    TarefaJira(
        "Gleicy",
        "JurisTriage P4 - Vetorização TF-IDF e divisão dos dados com NumPy",
        "docs/especificacoes/especificacao_04_gleicy_vetorizacao_numpy.md",
        "Implementar a divisão entre treino e teste e a vetorização TF-IDF sem usar scikit-learn nessas operações.",
    ),
    TarefaJira(
        "Helton",
        "JurisTriage P5 - Modelo e treino com PyTorch",
        "docs/especificacoes/especificacao_05_helton_modelo_pytorch.md",
        "Implementar a rede neuronal, o treino e a serialização dos pesos através de state_dict.",
    ),
    TarefaJira(
        "Luciana",
        "JurisTriage P6 - Modelo de referência, métricas e avaliação",
        "docs/especificacoes/especificacao_06_luciana_metricas.md",
        "Comparar o modelo com um modelo de referência e exportar as métricas de avaliação.",
    ),
    TarefaJira(
        "Sandro",
        "JurisTriage P7 - Inferência e modelo de linguagem opcional",
        "docs/especificacoes/especificacao_07_sandro_inferencia.md",
        "Criar inferência local orientada pelo manifesto; o modelo de linguagem é apenas opcional.",
    ),
    TarefaJira(
        "Pedro",
        "JurisTriage P8 - Integração, qualidade, testes automáticos e manifesto",
        "docs/especificacoes/especificacao_08_pedro_integracao.md",
        "Proteger os contratos de dados, integrar o fluxo de processamento, manter os testes automáticos e produzir os manifestos.",
    ),
)


def criar_descricao_adf(tarefa: TarefaJira) -> dict[str, Any]:
    """Cria uma descrição Atlassian Document Format para a API Jira v3."""

    url_especificacao = (
        f"{URL_REPOSITORIO}/blob/main/{tarefa.caminho_especificacao}"
    )
    paragrafos = (
        f"Objetivo: {tarefa.objetivo}",
        f"Responsável: {tarefa.pessoa}.",
        f"Especificação: {url_especificacao}",
        "Fluxo de trabalho: esclarecer, planear, analisar, implementar, testar e abrir um pedido de integração.",
        "Nomes: seguir a secção 9 da Constituição e usar identificadores descritivos em português.",
        "O apoio de IA deve ser declarado no pedido de integração. Todo o código deve ser compreendido, testado e sujeito a validação humana.",
    )
    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": paragraph}],
            }
            for paragraph in paragrafos
        ],
    }


class ClienteJira:
    """Cliente mínimo para pesquisa e criação idempotente de tarefas."""

    def __init__(self, url_base: str, email: str, token: str) -> None:
        self.url_base = url_base.rstrip("/")
        credenciais_codificadas = base64.b64encode(
            f"{email}:{token}".encode("utf-8")
        ).decode("ascii")
        self.cabecalhos = {
            "Authorization": f"Basic {credenciais_codificadas}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def pedir(
        self,
        metodo: str,
        caminho: str,
        conteudo: dict[str, Any] | None = None,
    ) -> Any:
        """Executa um pedido Jira e devolve a resposta JSON."""

        dados_pedido = (
            json.dumps(conteudo).encode("utf-8") if conteudo is not None else None
        )
        pedido = urllib.request.Request(
            f"{self.url_base}{caminho}",
            data=dados_pedido,
            headers=self.cabecalhos,
            method=metodo,
        )
        try:
            with urllib.request.urlopen(pedido, timeout=30) as resposta:
                corpo_resposta = resposta.read().decode("utf-8")
                return json.loads(corpo_resposta) if corpo_resposta else {}
        except urllib.error.HTTPError as erro:
            detalhe = erro.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Jira devolveu HTTP {erro.code}: {detalhe}") from erro
        except urllib.error.URLError as erro:
            raise RuntimeError(
                f"Não foi possível contactar o Jira: {erro.reason}"
            ) from erro

    def procurar_tarefa(self, chave_projeto: str, titulo: str) -> str | None:
        """Procura uma tarefa existente com o mesmo resumo."""

        titulo_escapado = titulo.replace('"', '\\"')
        jql = (
            f'project = "{chave_projeto}" AND labels = "{ETIQUETA_TAREFAS}" '
            f'AND summary ~ "\\"{titulo_escapado}\\""'
        )
        consulta = urllib.parse.urlencode(
            {"jql": jql, "fields": "key,summary", "maxResults": 50}
        )
        resultado = self.pedir("GET", f"/rest/api/3/search/jql?{consulta}")
        for tarefa in resultado.get("issues", []):
            if tarefa.get("fields", {}).get("summary") == titulo:
                return str(tarefa["key"])
        return None

    def procurar_utilizadores_atribuiveis(
        self,
        chave_projeto: str,
        texto_consulta: str,
    ) -> list[dict[str, Any]]:
        """Procura utilizadores que podem receber tarefas no projeto."""

        consulta = urllib.parse.urlencode(
            {
                "project": chave_projeto,
                "query": texto_consulta,
                "maxResults": 50,
            }
        )
        resultado = self.pedir(
            "GET",
            f"/rest/api/3/user/assignable/search?{consulta}",
        )
        if not isinstance(resultado, list):
            raise RuntimeError("O Jira devolveu um formato inesperado ao procurar utilizadores.")
        return resultado

    def criar_tarefa(
        self,
        chave_projeto: str,
        tarefa: TarefaJira,
        id_conta_responsavel: str,
    ) -> str:
        """Cria uma tarefa atribuída e devolve a chave Jira."""

        conteudo = {
            "fields": {
                "project": {"key": chave_projeto},
                "summary": tarefa.titulo,
                "description": criar_descricao_adf(tarefa),
                "issuetype": {"name": "Task"},
                "labels": [
                    ETIQUETA_TAREFAS,
                    f"juristriage-p{TAREFAS.index(tarefa) + 1}",
                ],
                "assignee": {"accountId": id_conta_responsavel},
            }
        }
        resultado = self.pedir("POST", "/rest/api/3/issue", conteudo)
        return str(resultado["key"])


def carregar_responsaveis(caminho: Path) -> dict[str, str]:
    """Lê o mapa local Pessoa -> Atlassian accountId."""

    if not caminho.exists():
        return {}
    conteudo = json.loads(caminho.read_text(encoding="utf-8"))
    if not isinstance(conteudo, dict):
        raise ValueError("O ficheiro de responsáveis deve conter um objeto JSON.")
    return {
        str(nome): str(id_conta)
        for nome, id_conta in conteudo.items()
    }


def carregar_membros(caminho: Path) -> dict[str, str]:
    """Lê o mapa local Pessoa -> email da conta Atlassian."""

    if not caminho.exists():
        raise FileNotFoundError(
            f"Ficheiro de membros não encontrado: {caminho}. "
            "Cria-o a partir de membros_jira.exemplo.json."
        )
    conteudo = json.loads(caminho.read_text(encoding="utf-8"))
    if not isinstance(conteudo, dict):
        raise ValueError("O ficheiro de membros deve conter um objeto JSON.")
    return {str(nome): str(email) for nome, email in conteudo.items()}


def resolver_responsaveis(
    cliente: ClienteJira,
    chave_projeto: str,
    membros: dict[str, str],
) -> dict[str, str]:
    """Resolve emails para accountIds, exigindo um resultado inequívoco."""

    responsaveis_resolvidos: dict[str, str] = {}
    for tarefa in TAREFAS:
        email = membros.get(tarefa.pessoa, "").strip()
        if not email:
            raise ValueError(f"Falta o email Atlassian de {tarefa.pessoa}.")
        utilizadores = cliente.procurar_utilizadores_atribuiveis(
            chave_projeto, email
        )
        correspondencias_exatas = [
            utilizador
            for utilizador in utilizadores
            if str(utilizador.get("emailAddress", "")).casefold()
            == email.casefold()
        ]
        candidatos = correspondencias_exatas or utilizadores
        if len(candidatos) != 1:
            raise RuntimeError(
                f"Não foi possível identificar {tarefa.pessoa} de forma inequívoca "
                f"com o email {email}. Resultados: {len(candidatos)}."
            )
        id_conta = str(candidatos[0].get("accountId", "")).strip()
        if not id_conta:
            raise RuntimeError(
                f"O Jira não devolveu accountId para {tarefa.pessoa}."
            )
        responsaveis_resolvidos[tarefa.pessoa] = id_conta
        print(f"Resolvido: {tarefa.pessoa}")
    return responsaveis_resolvidos


def ler_argumentos() -> argparse.Namespace:
    """Lê os argumentos da linha de comandos."""

    analisador = argparse.ArgumentParser(description=__doc__)
    analisador.add_argument(
        "--aplicar",
        "--apply",
        dest="aplicar",
        action="store_true",
        help="Cria tarefas reais. Sem esta opção, apenas simula.",
    )
    analisador.add_argument(
        "--responsaveis",
        "--assignees",
        dest="responsaveis",
        type=Path,
        default=None,
        help="JSON local com o mapa Pessoa -> Atlassian accountId.",
    )
    analisador.add_argument(
        "--membros",
        "--members",
        dest="membros",
        type=Path,
        default=None,
        help="JSON local com o mapa Pessoa -> email Atlassian.",
    )
    analisador.add_argument(
        "--resolver-responsaveis",
        "--resolve-assignees",
        dest="resolver_responsaveis",
        action="store_true",
        help="Resolve emails para accountIds e grava o ficheiro local de responsáveis.",
    )
    return analisador.parse_args()


def executar() -> int:
    """Valida a configuração e cria apenas as tarefas ainda inexistentes."""

    load_dotenv()
    argumentos = ler_argumentos()
    chave_projeto = os.getenv(
        "JIRA_CHAVE_PROJETO",
        os.getenv("JIRA_PROJECT_KEY", "SCRUM"),
    )
    caminho_responsaveis = argumentos.responsaveis or Path(
        os.getenv(
            "JIRA_FICHEIRO_RESPONSAVEIS",
            os.getenv("JIRA_ASSIGNEES_FILE", "responsaveis_jira.json"),
        )
    )
    caminho_membros = argumentos.membros or Path(
        os.getenv(
            "JIRA_FICHEIRO_MEMBROS",
            os.getenv("JIRA_MEMBERS_FILE", "membros_jira.json"),
        )
    )
    responsaveis = carregar_responsaveis(caminho_responsaveis)

    url_base = os.getenv("JIRA_URL_BASE", os.getenv("JIRA_BASE_URL", ""))
    email = os.getenv("JIRA_EMAIL", "")
    token = os.getenv("JIRA_TOKEN_API", os.getenv("JIRA_API_TOKEN", ""))
    if argumentos.resolver_responsaveis or argumentos.aplicar:
        if not url_base or not email or not token:
            print(
                "Define JIRA_URL_BASE, JIRA_EMAIL e JIRA_TOKEN_API no .env local.",
                file=sys.stderr,
            )
            return 2

    cliente = (
        ClienteJira(url_base, email, token)
        if url_base and email and token
        else None
    )
    if argumentos.resolver_responsaveis:
        assert cliente is not None
        membros = carregar_membros(caminho_membros)
        responsaveis = resolver_responsaveis(
            cliente, chave_projeto, membros
        )
        caminho_responsaveis.write_text(
            json.dumps(responsaveis, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"AccountIds gravados localmente em {caminho_responsaveis}.")

    pessoas_em_falta = [
        tarefa.pessoa
        for tarefa in TAREFAS
        if not responsaveis.get(tarefa.pessoa)
    ]

    print(f"Projeto Jira: {chave_projeto}")
    print(f"Modo: {'APLICAR' if argumentos.aplicar else 'SIMULAÇÃO'}")
    for tarefa in TAREFAS:
        estado_atribuicao = (
            "atribuição configurada"
            if tarefa.pessoa in responsaveis
            else "sem accountId"
        )
        print(f"- {tarefa.pessoa}: {tarefa.titulo} ({estado_atribuicao})")

    if not argumentos.aplicar:
        print(
            "Nenhuma alteração foi enviada ao Jira. "
            "Usa --aplicar depois da validação."
        )
        return 0

    if pessoas_em_falta:
        print(
            "Faltam accountIds Atlassian para: "
            + ", ".join(pessoas_em_falta),
            file=sys.stderr,
        )
        return 2

    assert cliente is not None
    for tarefa in TAREFAS:
        chave_existente = cliente.procurar_tarefa(
            chave_projeto, tarefa.titulo
        )
        if chave_existente:
            print(f"Já existe: {chave_existente} - {tarefa.titulo}")
            continue
        chave_criada = cliente.criar_tarefa(
            chave_projeto,
            tarefa,
            responsaveis[tarefa.pessoa],
        )
        print(f"Criada: {chave_criada} - {tarefa.titulo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(executar())
