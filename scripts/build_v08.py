"""Build the evidence-first, compact, full-width v0.8 interactive methods DAG.

Only documented extends/combines edges determine the primary canvas's
connectivity. Methods without a known evolution edge remain in the *same
canonical Atlas*, but are discoverable in a collapsible, searchable shelf.

Build: python -m scripts.build_v08 --site build/viewer-v08

Requires Graphviz at build time only.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from collections import defaultdict, deque
from pathlib import Path

from scripts.build_v06 import build_graph as build_v06
from scripts.build_v07 import (
    CONFIG, _check_acyclic, _dot_quote, _wrap_label, build_payload,
)
from scripts.validate import ROOT

GENEALOGY = {"extends", "combines"}
STRUCTURAL = GENEALOGY | {"specializes"}
GRAYOUT = "#AEBBC9"


def connected_components(method_ids: set[str], edges: list[dict]) -> list[list[str]]:
    """Weak components of the *actual documented method evolution* subgraph."""
    adjacent: dict[str, set[str]] = {mid: set() for mid in method_ids}
    for rel in edges:
        if rel["type"] not in GENEALOGY:
            continue
        source, target = rel["source"], rel["target"]
        if source not in adjacent or target not in adjacent:
            raise ValueError(f"Broken evolution edge endpoints: {rel['id']}")
        adjacent[source].add(target)
        adjacent[target].add(source)
    result = []
    seen = set()
    for start in sorted(method_ids):
        if start in seen:
            continue
        queue = deque([start])
        component = []
        seen.add(start)
        while queue:
            current = queue.popleft()
            component.append(current)
            for neighbor in sorted(adjacent[current]):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        result.append(sorted(component))
    result.sort(key=lambda c: (-len(c), c[0]))
    return result


def build_payload_v08(base: dict, config: dict) -> dict:
    payload = build_payload(base, config)
    all_ids = {m["id"] for m in payload["methods"]}
    evolution = [e for e in payload["method_edges"] if e["type"] in GENEALOGY]
    ids_in_lineage = {
        mid for e in evolution for mid in (e["source"], e["target"])
    }
    if not ids_in_lineage:
        raise ValueError("No scholarly evolution edges to lay out")
    missing = all_ids - ids_in_lineage

    components = [
        {"id": f"lineage-{i+1:02d}", "method_ids": c,
         "size": len(c)}
        for i, c in enumerate(connected_components(ids_in_lineage, evolution))
    ]
    assert all(c["size"] >= 2 for c in components)
    assert set().union(*(set(c["method_ids"]) for c in components)) == ids_in_lineage

    taxonomy = [e for e in payload["method_edges"] if e["type"] == "specializes"]
    comparisons = [e for e in payload["method_edges"] if e["type"] == "contrasts_with"]

    payload["version"] = "0.8.0"
    payload["core_method_ids"] = sorted(ids_in_lineage)
    payload["unlinked_method_ids"] = sorted(missing)
    payload["components"] = components
    payload["layout_policy"] = {
        "main_canvas": "Only methods incident to documented extends/combines relations",
        "unlinked_shelf": "Methods without a documented evolution/combination link",
        "rank_constraints": "Only documented extends/combines edges",
        "taxonomy_display": "Optional neutral links, no rank constraint",
        "comparison_display": "Optional neutral links, no rank constraint",
        "no_fabricated_edges": True,
    }
    payload["summary"].update({
        "core_methods": len(ids_in_lineage),
        "unlinked_methods": len(missing),
        "evolution_components": len(components),
        "taxonomy_links": len(taxonomy),
        "comparison_links": len(comparisons),
    })
    _check_acyclic(sorted(ids_in_lineage), evolution)
    if len(ids_in_lineage) + len(missing) != len(all_ids):
        raise ValueError("Incomplete method partition in layout")
    return payload


def create_compact_dot(payload: dict) -> tuple[str, dict[str, str], dict[str, str]]:
    core = set(payload["core_method_ids"])
    nodes = [n for n in payload["methods"] if n["id"] in core]
    paradigms = {p["id"]: p for p in payload["paradigms"]}
    node_ids = {
        m["id"]: "method_" + re.sub(r"[^A-Za-z0-9_]", "_", m["id"])
        for m in nodes
    }
    edge_ids = {
        e["id"]: "link_" + re.sub(r"[^A-Za-z0-9_]", "_", e["id"])
        for e in payload["method_edges"]
        if e["source"] in core and e["target"] in core
    }

    # packmode=graph minimizes whitespace between independent scholarly DAG
    # components. Rank constraints are only placed on real evolution/fusion.
    parts = [
        "digraph Atlas {",
        'graph [rankdir=LR, bgcolor="transparent", pad=0.38, '
        'nodesep=0.36, ranksep=0.87, splines=true, '
        'pack=true, packmode="graph", packmargin=22, '
        'outputorder=edgesfirst, fontname="Noto Sans CJK SC"];',
        'node [shape=box, style="rounded,filled", fontname="Noto Sans CJK SC", '
        'fontsize=13, width=2.5, height=0.73, fixedsize=true, '
        'margin="0.12,0.10", penwidth=1.65];',
        'edge [arrowsize=0.72, penwidth=2.4];',
    ]
    for method in nodes:
        cat = paradigms[method["paradigm"]]
        parts.append(
            f'{_dot_quote(method["id"])} '
            f'[id={_dot_quote(node_ids[method["id"]])}, '
            f'label={_dot_quote(_wrap_label(method["label"]["zh"]))}, '
            f'fillcolor={_dot_quote(cat["fill"])}, '
            f'color={_dot_quote(cat["color"])}, fontcolor="#253D54"];'
        )

    for edge in payload["method_edges"]:
        if edge["source"] not in core or edge["target"] not in core:
            continue
        kind = edge["type"]
        if kind in GENEALOGY:
            color = edge["color"]
            style = "dashed" if kind == "combines" else "solid"
            constraint, weight, penwidth = "true", 12, 2.6
            arrowhead = "normal"
        elif kind == "specializes":
            color, style, constraint = GRAYOUT, "dotted", "false"
            weight, penwidth, arrowhead = 0, 1.3, "normal"
        else:
            color, style, constraint = "#C6CED8", "dotted", "false"
            weight, penwidth, arrowhead = 0, 1.2, "none"
        parts.append(
            f'{_dot_quote(edge["source"])} -> {_dot_quote(edge["target"])} '
            f'[id={_dot_quote(edge_ids[edge["id"]])}, '
            f'color={_dot_quote(color)}, style={style}, '
            f'constraint={constraint}, weight={weight}, minlen=1, '
            f'penwidth={penwidth}, arrowhead={arrowhead}];'
        )
    parts.append("}")
    return "\n".join(parts), node_ids, edge_ids


def create_compact_svg(payload: dict) -> str:
    dot, node_ids, edge_ids = create_compact_dot(payload)
    try:
        result = subprocess.run(["dot", "-Tsvg"], input=dot, text=True,
                                check=True, timeout=45, capture_output=True)
    except FileNotFoundError as exc:
        raise RuntimeError("Graphviz dot is required at build time") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Graphviz rendering failed: " + exc.stderr[-2000:]) from exc
    svg = result.stdout
    svg = svg[svg.find("<svg"):svg.rfind("</svg>") + 6]
    if not svg.startswith("<svg"):
        raise RuntimeError("Graphviz did not return SVG")
    for method_id, gv_id in node_ids.items():
        old = f'<g id="{gv_id}" class="node">'
        if old not in svg:
            raise ValueError(f"Node missing in Graphviz output: {method_id}")
        svg = svg.replace(
            old,
            f'<g id="{gv_id}" class="node atlas-node" '
            f'data-method-id="{method_id}" role="button" tabindex="0">',
            1
        )
    for relation_id, gv_id in edge_ids.items():
        old = f'<g id="{gv_id}" class="edge">'
        if old not in svg:
            raise ValueError(f"Edge missing in Graphviz output: {relation_id}")
        svg = svg.replace(
            old,
            f'<g id="{gv_id}" class="edge atlas-edge" '
            f'data-edge-id="{relation_id}" role="button" tabindex="0">',
            1
        )
    svg = svg.replace("<svg ", '<svg id="atlas-dag" class="atlas-dag" ', 1)
    return svg


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT/"build"/"atlas-v08.json")
    parser.add_argument("--site", type=Path, default=None)
    args = parser.parse_args()

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    payload = build_payload_v08(build_v06(), config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

    if args.site:
        source = ROOT/"viewer-v08"
        args.site.mkdir(parents=True, exist_ok=True)
        html = (source/"index.html").read_text(encoding="utf-8")
        if '<div id="dag-slot"></div>' not in html or "</body>" not in html:
            raise ValueError("Viewer template lacks insertion anchors")
        html = html.replace('<div id="dag-slot"></div>', create_compact_svg(payload))
        embedded = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
        html = html.replace(
            "</body>", f'<script id="atlas-data" type="application/json">'
            f'{embedded}</script>\n</body>'
        )
        (args.site/"index.html").write_text(html, encoding="utf-8")
        # Keep the historical common typography and shell without a network
        # dependency; v0.8 source stylesheet is an additive override.
        common = (ROOT/"viewer-v07"/"style.css").read_text(encoding="utf-8")
        override = (source/"style.css").read_text(encoding="utf-8")
        (args.site/"style.css").write_text(common+"\n\n"+override, encoding="utf-8")
        shutil.copyfile(source/"app.js", args.site/"app.js")
        print("v0.8 standalone viewer:", args.site)

    print(
        f"v0.8: {payload['summary']['methods']} canonical methods; "
        f"{payload['summary']['core_methods']} evolution-linked on canvas; "
        f"{payload['summary']['unlinked_methods']} without documented lineage; "
        f"{payload['summary']['evolution_components']} independent evolution components"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
