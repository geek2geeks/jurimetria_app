"""CLI de inferência — P7"""

from __future__ import annotations

import argparse
import html
import json
import logging
import os
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import cast

from src.dados.carregador_acordaos_json import carregar_acordaos_json
from src.dados.esquemas import Acordao
from src.inferencia.formatador_saida import (
    ConfiguracaoSaida,
    carregar_dotenv,
    explicar_offline,
    explicar_via_llm,
    formatar,
)
from src.inferencia.motor_inferencia import MotorInferencia, ResultadoInferencia

_registo = logging.getLogger(__name__)


def construir_argumentos() -> argparse.Namespace:
    analisador = argparse.ArgumentParser(
        description=(
            "P7 — Inferência sobre acórdãos. "
            "Processa um ficheiro JSON isolado ou todos os JSONs de uma pasta."
        )
    )

    # Fonte dos acórdãos — mutuamente exclusivos, mas ambos opcionais
    # (o padrão vem de PASTA_DADOS no .env).
    grupo = analisador.add_mutually_exclusive_group()
    grupo.add_argument(
        "--ficheiro-json",
        metavar="FICHEIRO",
        help="Caminho para um único JSON estruturado de acórdão.",
    )
    grupo.add_argument(
        "--pasta-dados",
        metavar="PASTA",
        help="Pasta com vários JSONs de acórdãos (processa todos).",
    )

    # Execução — opcional: se ausente, usa ID_EXECUCAO do .env.
    analisador.add_argument(
        "--id-execucao",
        metavar="ID",
        default=None,
        help=(
            "ID da execução treinada (subpasta de artefactos/). "
            "Se omitido, usa ID_EXECUCAO do .env (default: execucao_teste)."
        ),
    )
    analisador.add_argument(
        "--pasta-artefactos",
        metavar="PASTA",
        default=None,
        help="Pasta-mãe das execuções. Se omitida, usa PASTA_ARTEFACTOS do .env (default: artefactos).",
    )
    analisador.add_argument(
        "--dotenv",
        default=".env",
        metavar="FICHEIRO",
        help="Caminho do .env a carregar (default: ./.env).",
    )
    analisador.add_argument(
        "--exportar-resumo",
        metavar="FICHEIROS",
        default=None,
        help=(
            "Exporta o resumo executivo. Formato deduzido pela extensão: "
            ".txt/.md (texto), .json (dados), .html (relatório com gráficos). "
            "Aceita vários destinos separados por vírgula, ex.: "
            "'relatorios/resumo.html,relatorios/resumo.json'. "
            "Se omitido, usa EXPORTAR_RESUMO do .env (se definido)."
        ),
    )
    return analisador.parse_args()


def _ficheiros_json(args: argparse.Namespace, pasta_dados_env: str) -> list[Path]:
    """Resolve a lista de JSONs a processar a partir dos argumentos e do .env."""

    if args.ficheiro_json:
        return [Path(args.ficheiro_json)]
    pasta: Path = Path(args.pasta_dados or pasta_dados_env)
    jsons: list[Path] = sorted(pasta.rglob("*.json"))
    if not jsons:
        _registo.error("Nenhum .json encontrado em '%s'.", pasta)
    return jsons


def _processar_ficheiro(
    caminho: Path,
    motor: MotorInferencia,
    configuracao: ConfiguracaoSaida,
) -> str | None:
    """Carrega, prevê e imprime o resultado de um ficheiro JSON."""

    acordaos: list[Acordao] = carregar_acordaos_json(str(caminho))
    if not acordaos:
        _registo.warning("'%s' não produziu acórdãos — ignorado.", caminho.name)
        return None

    acordao: Acordao = acordaos[0]
    resultado: ResultadoInferencia = motor.prever(acordao, com_explicacao=False)

    explicacao: str = (
        explicar_via_llm(
            resultado,
            resultado.termos_relevantes,
            resultado.excerto_sumario,
            configuracao,
        )
        if configuracao.usar_llm
        else explicar_offline(resultado, resultado.termos_relevantes)
    )

    print(f"\n[{caminho.name}]")
    print(formatar(resultado, explicacao, configuracao.formato))
    return resultado.categoria_prevista


def _grupo_do_ficheiro(caminho: Path, pasta_raiz: Path) -> str:
    """Devolve o primeiro componente do caminho relativo a `pasta_raiz`."""

    try:
        relativo: Path = caminho.resolve().relative_to(pasta_raiz.resolve())
        return relativo.parts[0] if len(relativo.parts) > 1 else "(raiz)"
    except ValueError:
        return "(externo)"


def _resumo_como_dados(
    contagens: dict[str, "Counter[str]"],
    pasta_raiz: Path,
    ficheiros_lidos: int | None = None,
    sem_rotulo: int = 0,
    erros: int = 0,
) -> dict[str, object]:
    """Constrói a estrutura de dados canónica do resumo.

    `total.ficheiros` conta apenas os acórdãos efetivamente CLASSIFICADOS.
    Ficheiros lidos que não produziram categoria (JSON sem acórdão, decisão
    vazia ou não reconhecida — ADR-05) ou que falharam saem dessa soma. Sem
    os campos de conciliação abaixo, esses desaparecem em silêncio e o total
    do relatório não bate com o número de ficheiros em disco:

        ficheiros_lidos = total.ficheiros + sem_rotulo + erros

    Args:
        contagens: categorias contadas por grupo (subpasta de 1.º nível).
        pasta_raiz: pasta analisada, base do agrupamento.
        ficheiros_lidos: ficheiros encontrados em disco. Se `None`, assume o
            total classificado (comportamento anterior, sem conciliação).
        sem_rotulo: ficheiros lidos que não produziram categoria.
        erros: ficheiros que levantaram exceção durante o processamento.
    """

    categorias: list[str] = ["MANTIDA", "REVOGADA", "ANULADA", "NAO_CONHECIDA", "OUTRA"]
    grupos: list[dict[str, object]] = []
    total_global: int = 0
    total_por_categoria: Counter[str] = Counter()

    for nome in sorted(contagens.keys()):
        contador: Counter[str] = contagens[nome]
        total: int = sum(contador.values())
        total_global += total
        total_por_categoria.update(contador)
        grupos.append(
            {
                "nome": nome,
                "total": total,
                "categorias": {
                    cat: {
                        "n": contador.get(cat, 0),
                        "pct": round(
                            (contador.get(cat, 0) / total * 100.0) if total else 0.0, 2
                        ),
                    }
                    for cat in categorias
                },
            }
        )

    return {
        "pasta_raiz": str(pasta_raiz),
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "ficheiros_lidos": (
            ficheiros_lidos if ficheiros_lidos is not None else total_global
        ),
        "sem_rotulo": sem_rotulo,
        "erros": erros,
        "categorias": categorias,
        "grupos": grupos,
        "total": {
            "ficheiros": total_global,
            "categorias": {
                cat: {
                    "n": total_por_categoria.get(cat, 0),
                    "pct": round(
                        (
                            (total_por_categoria.get(cat, 0) / total_global * 100.0)
                            if total_global
                            else 0.0
                        ),
                        2,
                    ),
                }
                for cat in categorias
            },
        },
    }


def _subpastas(dados: dict[str, object]) -> int:
    """Conta subpastas reais — '(raiz)' é a pasta analisada, não uma subpasta."""

    grupos: list[dict[str, object]] = cast(list[dict[str, object]], dados["grupos"])
    return sum(1 for grupo in grupos if grupo["nome"] not in {"(raiz)", "(externo)"})


def _resumo_como_texto(dados: dict[str, object]) -> str:
    """Mesmo formato do bloco impresso no terminal."""
    linhas: list[str] = []
    linhas.append("=" * 62)
    linhas.append(f" RESUMO EXECUTIVO — {dados['pasta_raiz']}")
    linhas.append(f" Gerado em: {dados['gerado_em']}")
    linhas.append("=" * 62)
    linhas.append("")
    linhas.append(f"Por subpasta (1.º nível abaixo de '{dados['pasta_raiz']}/'):")

    categorias: list[str] = cast(list[str], dados["categorias"])
    grupos: list[dict[str, object]] = cast(list[dict[str, object]], dados["grupos"])
    for grupo in grupos:
        cats_grupo: dict[str, dict[str, object]] = cast(
            dict[str, dict[str, object]], grupo["categorias"]
        )
        linhas.append("")
        linhas.append(f"  [{grupo['nome']}]  {grupo['total']} ficheiro(s):")
        for cat in categorias:
            info: dict[str, object] = cats_grupo[cat]
            linhas.append(f"    {cat:<15} {info['n']:>5}  ({info['pct']:5.1f}%)")

    total: dict[str, object] = cast(dict[str, object], dados["total"])
    total_cats: dict[str, dict[str, object]] = cast(
        dict[str, dict[str, object]], total["categorias"]
    )
    linhas.append("")
    linhas.append("-" * 62)
    linhas.append(
        f"Total geral em '{dados['pasta_raiz']}': {total['ficheiros']} ficheiro(s)"
    )
    linhas.append("-" * 62)
    for cat in categorias:
        info = total_cats[cat]
        linhas.append(f"  {cat:<15} {info['n']:>5}  ({info['pct']:5.1f}%)")

    # Conciliação — torna visível o que não foi classificado.
    linhas.append("")
    linhas.append("-" * 62)
    linhas.append("Conciliação")
    linhas.append("-" * 62)
    linhas.append(f"  {'Ficheiros lidos':<28} {dados['ficheiros_lidos']:>5}")
    linhas.append(f"  {'Classificados':<28} {total['ficheiros']:>5}")
    linhas.append(f"  {'Sem rótulo (descartados)':<28} {dados['sem_rotulo']:>5}")
    linhas.append(f"  {'Erros de processamento':<28} {dados['erros']:>5}")
    linhas.append(f"  {'Subpastas':<28} {_subpastas(dados):>5}")
    linhas.append("=" * 62)
    return "\n".join(linhas) + "\n"


def _resumo_como_json(dados: dict[str, object]) -> str:
    return json.dumps(dados, ensure_ascii=False, indent=2) + "\n"


def _resumo_como_html(dados: dict[str, object]) -> str:
    """Relatório HTML standalone, dark, com gráficos interactivos (Chart.js via CDN)."""
    dados_json: str = json.dumps(dados, ensure_ascii=False)
    pasta_raiz_esc: str = html.escape(str(dados["pasta_raiz"]))
    gerado_em_esc: str = html.escape(str(dados["gerado_em"]))
    total: dict[str, object] = cast(dict[str, object], dados["total"])
    total_ficheiros: int = cast(int, total["ficheiros"])

    return f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Resumo Executivo — Jurimetria PT</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script>
  // Verificação imediata — se o Chart.js não carregou, mostra aviso visível.
  if (typeof Chart === 'undefined') {{
    document.addEventListener('DOMContentLoaded', function () {{
      const aviso = document.createElement('div');
      aviso.style.cssText = 'background:#3d1a1a;border:1px solid #f85149;color:#f85149;' +
        'padding:1rem 1.5rem;border-radius:8px;margin:1rem 0;font-family:sans-serif;';
      aviso.innerHTML = '<strong>Chart.js não carregou.</strong><br>' +
        'Verifique a ligação à Internet, ou descarregue o ficheiro offline em ' +
        '<code>chart.umd.min.js</code> e ajuste o <code>src</code> deste relatório.';
      document.querySelector('.container').prepend(aviso);
    }});
  }}
</script>
<style>
:root {{
  --bg: #0d1117;
  --bg-elevated: #161b22;
  --bg-card: #1c2128;
  --border: #30363d;
  --text: #e6edf3;
  --text-dim: #8b949e;
  --text-muted: #6e7681;
  --accent: #58a6ff;
  --mantida: #3fb950;
  --revogada: #f85149;
  --anulada: #d29922;
  --nao-conhecida: #8b949e;
  --outra: #bc8cff;
  --descartado: #484f58;
  --shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body {{
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue",
               Arial, sans-serif;
  line-height: 1.5;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}}

.container {{ max-width: 1280px; margin: 0 auto; padding: 3rem 1.5rem; }}

header {{
  border-bottom: 1px solid var(--border);
  padding-bottom: 2rem;
  margin-bottom: 2.5rem;
}}
header .eyebrow {{
  color: var(--accent);
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}}
header h1 {{ font-size: 2rem; font-weight: 700; letter-spacing: -0.025em; }}
header h1 code {{
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  background: var(--bg-card);
  padding: 0.2rem 0.6rem;
  border-radius: 6px;
  font-size: 0.85em;
  color: var(--accent);
  border: 1px solid var(--border);
}}
header .meta {{
  color: var(--text-muted);
  font-size: 0.875rem;
  margin-top: 0.75rem;
  font-variant-numeric: tabular-nums;
}}

section {{ margin-bottom: 3rem; }}
section h2 {{
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-dim);
  margin-bottom: 1.25rem;
}}

.aviso-conciliacao {{
  border: 1px solid var(--border);
  border-left: 3px solid var(--anulada);
  border-radius: 8px;
  background: var(--bg-card);
  padding: 0.9rem 1.2rem;
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
  color: var(--text-dim);
}}
.aviso-conciliacao strong {{ color: var(--text); }}

.kpis {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(180px, 100%), 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}}
.kpi {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.5rem;
  min-width: 0;
  transition: border-color 0.2s, transform 0.2s;
}}
.kpi:hover {{ border-color: var(--accent); transform: translateY(-2px); }}
.kpi .label {{
  color: var(--text-muted);
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}}
.kpi .value {{
  font-size: 2rem;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.025em;
}}
.kpi .value small {{
  color: var(--text-muted);
  font-size: 0.875rem;
  font-weight: 400;
  margin-left: 0.25rem;
}}
.kpi .sub {{ color: var(--text-dim); font-size: 0.8125rem; margin-top: 0.35rem; }}
.kpi .badge {{
  display: inline-block;
  width: 0.625rem;
  height: 0.625rem;
  border-radius: 50%;
  margin-right: 0.5rem;
  vertical-align: 0.05em;
}}

.global-chart {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
}}
.global-chart .chart-wrapper {{ position: relative; height: 260px; }}

.grid-grupos {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(360px, 100%), 1fr));
  gap: 1.5rem;
}}
.card-grupo {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.75rem;
  min-width: 0;
  transition: border-color 0.2s;
}}
.card-grupo:hover {{ border-color: var(--accent); }}
.card-grupo .header-grupo {{
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}}
.card-grupo .nome {{
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.025em;
}}
.card-grupo .nome .tag-raiz {{
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-muted);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 0.1rem 0.45rem;
  margin-left: 0.5rem;
  vertical-align: 0.15em;
}}
.card-grupo .total {{
  color: var(--text-muted);
  font-size: 0.875rem;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}}
.card-grupo .chart-wrapper {{ position: relative; height: 200px; margin-bottom: 1rem; }}
.card-grupo .tabela {{ font-size: 0.8125rem; }}
.card-grupo .linha {{
  display: flex;
  justify-content: space-between;
  padding: 0.375rem 0;
  border-bottom: 1px solid var(--border);
  font-variant-numeric: tabular-nums;
}}
.card-grupo .linha:last-child {{ border-bottom: none; }}
.card-grupo .linha .cat {{ color: var(--text-dim); }}
.card-grupo .linha .cat .badge {{
  display: inline-block;
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  margin-right: 0.5rem;
  vertical-align: 0.1em;
}}
.card-grupo .linha .num {{ color: var(--text); font-weight: 500; }}
.card-grupo .linha .pct {{ color: var(--text-muted); margin-left: 0.5rem; }}

footer {{
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border);
  color: var(--text-muted);
  font-size: 0.75rem;
  text-align: center;
}}
footer a {{ color: var(--accent); text-decoration: none; }}
footer a:hover {{ text-decoration: underline; }}

@media (max-width: 640px) {{
  .container {{ padding: 1.5rem 1rem; }}
  header h1 {{ font-size: 1.5rem; }}
  .kpi .value {{ font-size: 1.5rem; }}
}}
</style>
</head>
<body>
<div class="container">

<header>
  <div class="eyebrow">Jurimetria PT · Inferência (P7)</div>
  <h1>Resumo Executivo — <code>{pasta_raiz_esc}</code></h1>
  <div class="meta">Gerado em {gerado_em_esc} · {total_ficheiros} ficheiro(s) classificado(s)</div>
</header>

<div id="conciliacao"></div>

<section>
  <h2>Indicadores principais</h2>
  <div class="kpis" id="kpis"></div>
</section>

<section>
  <h2>Distribuição global</h2>
  <div class="global-chart">
    <div class="chart-wrapper"><canvas id="chart-global"></canvas></div>
  </div>
</section>

<section>
  <h2>Por subpasta (1.º nível abaixo da raiz)</h2>
  <div class="grid-grupos" id="grid-grupos"></div>
</section>

<footer>
  Relatório gerado pelo Motor de Inferência (P7) ·
  Não constitui aconselhamento jurídico.
</footer>

</div>

<script>
const dados = {dados_json};

const cores = {{
  "MANTIDA":        getComputedStyle(document.documentElement).getPropertyValue('--mantida').trim(),
  "REVOGADA":       getComputedStyle(document.documentElement).getPropertyValue('--revogada').trim(),
  "ANULADA":        getComputedStyle(document.documentElement).getPropertyValue('--anulada').trim(),
  "NAO_CONHECIDA":  getComputedStyle(document.documentElement).getPropertyValue('--nao-conhecida').trim(),
  "OUTRA":          getComputedStyle(document.documentElement).getPropertyValue('--outra').trim(),
}};

const textoDim = getComputedStyle(document.documentElement).getPropertyValue('--text-dim').trim();
const bgCard = getComputedStyle(document.documentElement).getPropertyValue('--bg-card').trim();

// Defaults globais do Chart.js para tema dark
Chart.defaults.color = textoDim;
Chart.defaults.borderColor = getComputedStyle(document.documentElement).getPropertyValue('--border').trim();
Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";

// === Conciliação de contagem ===
// '(raiz)' é a pasta analisada, não uma subpasta: não entra nesta contagem.
const ehRaiz = (g) => g.nome === '(raiz)' || g.nome === '(externo)';
const subpastas = dados.grupos.filter(g => !ehRaiz(g)).length;
const classificados = dados.total.ficheiros;
const lidos = dados.ficheiros_lidos != null ? dados.ficheiros_lidos : classificados;
const semRotulo = dados.sem_rotulo != null ? dados.sem_rotulo : 0;
const errosProc = dados.erros != null ? dados.erros : 0;
const descartados = semRotulo + errosProc;

if (lidos !== classificados) {{
  document.getElementById('conciliacao').innerHTML =
    '<div class="aviso-conciliacao"><strong>' + descartados + ' de ' + lidos +
    ' ficheiro(s) não entraram na classificação.</strong> ' + semRotulo +
    ' sem rótulo (decisão vazia ou não reconhecida, ADR-05) e ' + errosProc +
    ' com erro de processamento. Os gráficos abaixo cobrem apenas os ' +
    classificados + ' classificados.</div>';
}}

// === KPIs ===
const kpis = document.getElementById('kpis');
const totalCat = dados.total.categorias;
const ranked = dados.categorias
  .map(c => ({{ nome: c, n: totalCat[c].n, pct: totalCat[c].pct }}))
  .sort((a, b) => b.n - a.n);

kpis.innerHTML = `
  <div class="kpi">
    <div class="label">Ficheiros lidos</div>
    <div class="value">${{lidos.toLocaleString('pt-PT')}}</div>
    <div class="sub">encontrados em disco</div>
  </div>
  <div class="kpi">
    <div class="label">Classificados</div>
    <div class="value">${{classificados.toLocaleString('pt-PT')}}</div>
    <div class="sub">soma das cinco categorias</div>
  </div>
  <div class="kpi">
    <div class="label"><span class="badge" style="background:var(--descartado)"></span>Descartados</div>
    <div class="value">${{descartados.toLocaleString('pt-PT')}}</div>
    <div class="sub">${{semRotulo}} sem rótulo · ${{errosProc}} com erro</div>
  </div>
  <div class="kpi">
    <div class="label">Subpastas</div>
    <div class="value">${{subpastas}}</div>
    <div class="sub">a raiz é contada à parte</div>
  </div>
` + ranked.slice(0, 2).map(c => `
  <div class="kpi">
    <div class="label"><span class="badge" style="background:${{cores[c.nome]}}"></span>${{c.nome}}</div>
    <div class="value">${{c.pct.toFixed(1)}}<small>%</small></div>
    <div class="sub">${{c.n}} ficheiro(s)</div>
  </div>
`).join('');

// === Gráfico global (barra horizontal) ===
new Chart(document.getElementById('chart-global'), {{
  type: 'bar',
  data: {{
    labels: dados.categorias,
    datasets: [{{
      data: dados.categorias.map(c => totalCat[c].n),
      backgroundColor: dados.categorias.map(c => cores[c]),
      borderRadius: 6,
      borderSkipped: false,
    }}],
  }},
  options: {{
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{
        backgroundColor: bgCard,
        padding: 12,
        callbacks: {{
          label: (ctx) => {{
            const n = ctx.parsed.x;
            const pct = totalCat[ctx.label].pct;
            return ` ${{n}} ficheiros (${{pct.toFixed(1)}}%)`;
          }},
        }},
      }},
    }},
    scales: {{
      x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ precision: 0 }} }},
      y: {{ grid: {{ display: false }} }},
    }},
  }},
}});

// === Donuts por subpasta ===
const grid = document.getElementById('grid-grupos');
dados.grupos.forEach((grupo, idx) => {{
  const id = `donut-${{idx}}`;
  const linhas = dados.categorias.map(cat => {{
    const info = grupo.categorias[cat];
    return `<div class="linha">
      <span class="cat"><span class="badge" style="background:${{cores[cat]}}"></span>${{cat}}</span>
      <span><span class="num">${{info.n}}</span><span class="pct">(${{info.pct.toFixed(1)}}%)</span></span>
    </div>`;
  }}).join('');

  grid.insertAdjacentHTML('beforeend', `
    <div class="card-grupo">
      <div class="header-grupo">
        <span class="nome">${{grupo.nome}}${{ehRaiz(grupo) ? '<span class="tag-raiz">raiz</span>' : ''}}</span>
        <span class="total">${{grupo.total}} ficheiro(s)</span>
      </div>
      <div class="chart-wrapper"><canvas id="${{id}}"></canvas></div>
      <div class="tabela">${{linhas}}</div>
    </div>
  `);

  new Chart(document.getElementById(id), {{
    type: 'doughnut',
    data: {{
      labels: dados.categorias,
      datasets: [{{
        data: dados.categorias.map(c => grupo.categorias[c].n),
        backgroundColor: dados.categorias.map(c => cores[c]),
        borderColor: bgCard,
        borderWidth: 2,
      }}],
    }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      cutout: '65%',
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          backgroundColor: bgCard,
          padding: 12,
          callbacks: {{
            label: (ctx) => {{
              const n = ctx.parsed;
              const pct = grupo.categorias[ctx.label].pct;
              return ` ${{n}} (${{pct.toFixed(1)}}%)`;
            }},
          }},
        }},
      }},
    }},
  }});
}});
</script>
</body>
</html>
"""


def _destinos_de_exportacao(valor: str | None) -> list[Path]:
    """Divide a lista de destinos separada por vírgulas, ignorando vazios."""

    if not valor:
        return []
    return [Path(parte.strip()) for parte in valor.split(",") if parte.strip()]


def _exportar_resumo(
    contagens: dict[str, "Counter[str]"],
    pasta_raiz: Path,
    caminho_saida: str | Path,
    ficheiros_lidos: int | None = None,
    sem_rotulo: int = 0,
    erros: int = 0,
) -> None:
    """Exporta o resumo para ficheiro, formato deduzido pela extensão.

    .txt, .md  → texto plano
    .json      → dados estruturados (consumido pelo site de apresentação)
    .html      → relatório dark com gráficos interactivos (Chart.js via CDN)
    """
    caminho: Path = Path(caminho_saida)
    extensao: str = caminho.suffix.lower()
    dados: dict[str, object] = _resumo_como_dados(
        contagens,
        pasta_raiz,
        ficheiros_lidos=ficheiros_lidos,
        sem_rotulo=sem_rotulo,
        erros=erros,
    )

    if extensao in {".txt", ".md"}:
        conteudo: str = _resumo_como_texto(dados)
    elif extensao == ".json":
        conteudo = _resumo_como_json(dados)
    elif extensao == ".html":
        conteudo = _resumo_como_html(dados)
    else:
        _registo.warning(
            "Extensão '%s' não reconhecida; a exportar como texto plano.", extensao
        )
        conteudo = _resumo_como_texto(dados)

    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(conteudo, encoding="utf-8")
    _registo.info("Resumo executivo exportado para %s", caminho.resolve())


def _exibir_metricas_treino(motor: MotorInferencia, formato: str) -> None:
    """Mostra (uma só vez) as métricas que o P6/Luciana gravou no treino.

    Leitura PASSIVA do `metricas.json` que o motor já carregou. Não chama
    funções do P6 — só exibe o contexto da qualidade do modelo carregado.
    Pula silenciosamente se não houver métricas (ex.: execução de scaffolding).
    """
    if not motor.metricas_treino:
        return

    def _percentagem(valor: object) -> str:
        return f"{float(valor):.2%}" if isinstance(valor, (int, float)) else "—"

    metricas = motor.metricas_treino
    exatidao = metricas.get("exatidao")
    macro_f1 = metricas.get("macro_f1")
    baseline = metricas.get("macro_f1_referencia") or metricas.get("macro_f1_baseline")
    nota = metricas.get("nota")

    if formato == "json":
        # No formato JSON, anexar como bloco separado para um consumidor automático.
        print(json.dumps({"metricas_treino": metricas}, ensure_ascii=False, indent=2))
        return

    # Em texto e markdown, mostramos um pequeno cabeçalho informativo.
    if formato == "markdown":
        print("### Métricas do treino (P6 — Luciana)")
        print()
        print(f"- Exatidão: {_percentagem(exatidao)}")
        print(f"- Macro-F1: {_percentagem(macro_f1)}")
        print(f"- Macro-F1 da baseline: {_percentagem(baseline)}")
        if nota:
            print(f"- Nota: {nota}")
        print()
        return

    print()
    print("--- Modelo carregado (métricas do treino, P6) ---")
    print(f"  Exatidão              : {_percentagem(exatidao)}")
    print(f"  Macro-F1 do modelo    : {_percentagem(macro_f1)}")
    print(f"  Macro-F1 da baseline  : {_percentagem(baseline)}")
    if nota:
        print(f"  Nota                  : {nota}")
    print("--------------------------------------------------")


def principal() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(name)s | %(message)s"
    )
    args: argparse.Namespace = construir_argumentos()

    # 1. Carregar .env.
    carregar_dotenv(args.dotenv)
    configuracao: ConfiguracaoSaida = ConfiguracaoSaida.a_partir_do_ambiente()

    id_execucao: str = args.id_execucao or os.environ.get(
        "ID_EXECUCAO", "execucao_teste"
    )
    pasta_artefactos: str = args.pasta_artefactos or os.environ.get(
        "PASTA_ARTEFACTOS", "artefactos"
    )
    pasta_dados_env: str = os.environ.get("PASTA_DADOS", "data")

    _registo.info(
        "execucao=%s | llm=%s | formato=%s",
        id_execucao,
        configuracao.usar_llm,
        configuracao.formato,
    )

    # 2. Resolver ficheiros a processar.
    ficheiros: list[Path] = _ficheiros_json(args, pasta_dados_env)
    if not ficheiros:
        return 1

    # 3. Carregar motor (uma só vez para todos os ficheiros).
    motor: MotorInferencia = MotorInferencia(
        id_execucao, pasta_artefactos=pasta_artefactos
    )

    # 3b. Exibir métricas do treino (P6) — informativo, leitura passiva.
    _exibir_metricas_treino(motor, configuracao.formato)

    # 4. Processar cada ficheiro, acumulando contagens por subpasta.
    #    `sem_rotulo` e `erros` são contados explicitamente para que o resumo
    #    possa conciliar ficheiros lidos com ficheiros classificados.
    contagens: defaultdict[str, Counter[str]] = defaultdict(Counter)
    pasta_raiz: Path | None = (
        Path(args.pasta_dados or pasta_dados_env) if not args.ficheiro_json else None
    )
    erros: int = 0
    sem_rotulo: int = 0
    for caminho in ficheiros:
        try:
            categoria: str | None = _processar_ficheiro(caminho, motor, configuracao)
            if categoria is None:
                sem_rotulo += 1
                continue
            if pasta_raiz is not None:
                grupo: str = _grupo_do_ficheiro(caminho, pasta_raiz)
                contagens[grupo][categoria] += 1
        except Exception as erro:  # noqa: BLE001
            _registo.error("Erro ao processar '%s': %s", caminho.name, erro)
            erros += 1

    # 5. Exportação do resumo executivo (opcional — só se EXPORTAR_RESUMO/CLI definido).
    #    Resumo só faz sentido com lote (>1 ficheiro). Aceita vários destinos
    #    separados por vírgula, ex.: 'relatorios/resumo.html,relatorios/resumo.json'.
    destinos: list[Path] = _destinos_de_exportacao(
        args.exportar_resumo or os.environ.get("EXPORTAR_RESUMO")
    )
    total_processados: int = sum(sum(c.values()) for c in contagens.values())
    if pasta_raiz is not None and destinos and total_processados > 1:
        for destino in destinos:
            try:
                _exportar_resumo(
                    dict(contagens),
                    pasta_raiz,
                    destino,
                    ficheiros_lidos=len(ficheiros),
                    sem_rotulo=sem_rotulo,
                    erros=erros,
                )
            except Exception as erro:  # noqa: BLE001
                _registo.error("Falha ao exportar resumo para '%s': %s", destino, erro)
                erros += 1

    if sem_rotulo:
        _registo.info(
            "%d ficheiro(s) lido(s) sem categoria atribuída (descartados do resumo).",
            sem_rotulo,
        )
    if erros:
        _registo.warning("%d ficheiro(s) com erro.", erros)
    return 0 if erros == 0 else 1


if __name__ == "__main__":
    raise SystemExit(principal())
