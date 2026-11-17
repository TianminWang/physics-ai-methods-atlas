"""Build the three-phase, one-canvas scholarly method DAG viewer.

Canonical methods and literature come from scripts.build_v06; v0.7 config adds
only presentation taxonomy, three-phase grouping and color semantics.

Requires Graphviz dot at build time (not when viewing offline HTML).
Usage: python -m scripts.build_v07 --site build/viewer-v07
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import unicodedata
from collections import defaultdict, deque
from pathlib import Path

from scripts.build_v06 import build_graph as build_v06
from scripts.validate import ROOT

LAYOUT_TYPES = {"extends", "combines", "specializes"}
LINEAGE_TYPES = {"extends", "combines"}
CONFIG = ROOT / "config" / "v07.json"


def _wrap_label(label: str, limit: int = 19) -> str:
    """Split human-readable labels without breaking Asian and Latin glyph widths."""
    # Short bilingual labels preserve the method's original identity.
    if len(label) <= 22 and sum(
        2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in label
    ) <= limit:
        return label
    words = re.findall(r"\S+\s*|\s+", label)
    lines, current, width = [], "", 0
    for word in words:
        size = sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in word)
        if width + size > limit and current.strip():
            lines.append(current.strip())
            current, width = "", 0
        if size > limit:
            for c in word:
                n = 2 if unicodedata.east_asian_width(c) in "WF" else 1
                if width+n > limit:
                    lines.append(current.strip()); current, width = "", 0
                current += c; width += n
        else:
            current += word; width += size
    if current.strip():
        lines.append(current.strip())
    if len(lines) > 2:
        return lines[0] + "\n" + lines[1][:14] + "…"
    return "\n".join(lines)


def _dot_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def _check_acyclic(methods: list[str], links: list[dict]) -> None:
    neighbors: dict[str, set[str]] = {x: set() for x in methods}
    incoming = dict.fromkeys(methods, 0)
    for e in links:
        a, b = e["source"], e["target"]
        if b not in neighbors[a]:
            neighbors[a].add(b); incoming[b] += 1
    q = deque(sorted(m for m in methods if incoming[m] == 0))
    visited = 0
    while q:
        current = q.popleft()
        visited += 1
        for nxt in sorted(neighbors[current]):
            incoming[nxt] -= 1
            if incoming[nxt] == 0:
                q.append(nxt)
    if visited != len(methods):
        raise ValueError("Combined layout of extends / combines / specializes is cyclic; review relation semantics.")


def build_payload(base: dict, config: dict) -> dict:
    methods = base["methods"]
    method_ids = {m["id"] for m in methods}
    assigned = config["method_paradigm"]
    if method_ids != set(assigned):
        raise ValueError(
            f"Method taxonomy mismatch: missing {sorted(method_ids-set(assigned))}, "
            f"extra {sorted(set(assigned)-method_ids)}"
        )
    paradigm_ids = {p["id"] for p in config["paradigms"]}
    if len(paradigm_ids) != len(config["paradigms"]) or set(assigned.values())-paradigm_ids:
        raise ValueError("Invalid paradigm classification IDs")
    phase_ids = {p["id"] for p in config["phases"]}
    if len(phase_ids) != 3 or len({p["color"] for p in config["phases"]}) != 3:
        raise ValueError("Expected three distinct top-level research phases/colors")
    old_stages = {s["id"] for s in base["stages"]}
    child_stage_ids = [sid for p in config["phases"] for sid in p["stage_ids"]]
    if set(child_stage_ids) != old_stages or len(child_stage_ids) != len(old_stages):
        raise ValueError("Every original workflow sub-capability must map to exactly one top-level phase")

    stage_to_phase = {sid: p["id"] for p in config["phases"] for sid in p["stage_ids"]}
    phase_colors = {p["id"]: p["color"] for p in config["phases"]}
    paradigm_colors = {p["id"]: p for p in config["paradigms"]}

    family_names = {f["id"]: f["name"] for f in base["families"]}
    enriched = []
    for method in methods:
        p = paradigm_colors[assigned[method["id"]]]
        n = dict(method)
        n.pop("zone", None)
        n["paradigm"] = p["id"]
        n["paradigm_color"] = p["color"]
        n["paradigm_fill"] = p["fill"]
        n["family_names"] = [family_names[f] for f in n["families"]]
        enriched.append(n)

    edges = []
    for source in base["method_edges"]:
        item = dict(source)
        p = stage_to_phase.get(source.get("primary_stage"))
        item["primary_phase"] = p
        item["phase_ids"] = sorted({stage_to_phase[s] for s in source["stages"]})
        item["color"] = (
            phase_colors[p] if p and source["type"] in LINEAGE_TYPES else "#9AA8B9"
        )
        edges.append(item)

    # Preserve actual, scoped stage→family/method claims; never upgrade
    # family-level relevance to an empirically verified direct method claim.
    phase_roles = {}
    for phase in config["phases"]:
        coll = defaultdict(list)
        for stage in phase["stage_ids"]:
            for method_id, roles in base["stage_roles"][stage].items():
                for role in roles:
                    coll[method_id].append({**role, "stage_id": stage})
        phase_roles[phase["id"]] = dict(sorted(coll.items()))

    layout_edges = [e for e in edges if e["type"] in LAYOUT_TYPES]
    _check_acyclic(sorted(method_ids), layout_edges)

    return {
        "version": "0.7.0",
        "scope": "Full current Atlas methods; evidence and role claims remain canonical",
        "phases": config["phases"],
        "subcapabilities": [{
            **stage,
            "phase": stage_to_phase[stage["id"]],
            "name": config["substage_overrides"].get(stage["id"], stage["name"]),
        } for stage in base["stages"]],
        "paradigms": config["paradigms"],
        "methods": enriched,
        "method_edges": edges,
        "functional": base["functional"],
        "phase_roles": phase_roles,
        "summary": {
            "methods": len(enriched),
            "method_links": len(edges),
            "layout_links": len(layout_edges),
            "lineage_links": sum(e["type"] in LINEAGE_TYPES for e in layout_edges),
            "functional_links": len(base["functional"]),
        },
    }


def create_dot(payload: dict) -> tuple[str, dict[str, str], dict[str, str]]:
    methods = payload["methods"]
    paradigm = {p["id"]: p for p in payload["paradigms"]}
    node_ids = {m["id"]: "n_" + m["id"].replace(".", "_").replace("-", "_")
                for m in methods}
    edge_ids = {e["id"]: "e_" + re.sub(r"[^a-zA-Z0-9_]", "_", e["id"])
                for e in payload["method_edges"]}
    # No category rectangles or visual-region placement. Graphviz's layered
    # DAG algorithm resolves ranks and edge crossings from documented relations.
    parts = [
        "digraph Atlas {",
        'graph [rankdir=LR, bgcolor="transparent", pad=0.48, nodesep=0.35, '
        'ranksep=1.15, splines=true, outputorder=edgesfirst, pack=true, '
        'packmode="array_u4", fontname="Noto Sans CJK SC"];',
        'node [shape=box, style="rounded,filled", fontname="Noto Sans CJK SC", '
        'fontsize=13, margin="0.15,0.10", width=2.48, height=0.72, '
        'fixedsize=true, penwidth=1.6];',
        'edge [arrowsize=0.7, penwidth=2.1];',
    ]
    for method in methods:
        cat = paradigm[method["paradigm"]]
        title = _wrap_label(method["label"]["zh"])
        parts.append(
            f'{_dot_quote(method["id"])} [id={_dot_quote(node_ids[method["id"]])}, '
            f'label={_dot_quote(title)}, fillcolor={_dot_quote(cat["fill"])}, '
            f'color={_dot_quote(cat["color"])}, fontcolor="#253D54"];'
        )
    for edge in payload["method_edges"]:
        if edge["type"] == "contrasts_with":
            continue  # non-genealogical comparisons are opt-in UI relations
        t = edge["type"]
        color = "#B9C3CE" if t == "specializes" else edge["color"]
        style = "dotted" if t == "specializes" else (
            "dashed" if t == "combines" else "solid"
        )
        weight = 3 if t == "specializes" else 8
        parts.append(
            f'{_dot_quote(edge["source"])} -> {_dot_quote(edge["target"])} '
            f'[id={_dot_quote(edge_ids[edge["id"]])}, color={_dot_quote(color)}, '
            f'style={style}, weight={weight}, minlen=1, '
            f'penwidth={1.2 if t=="specializes" else 2.5}];'
        )
    parts.append("}")
    return "\n".join(parts), node_ids, edge_ids


def build_svg(payload: dict) -> str:
    dot, node_ids, edge_ids = create_dot(payload)
    try:
        cmd = subprocess.run(["dot", "-Tsvg"], input=dot, text=True,
                             check=True, capture_output=True, timeout=35)
    except FileNotFoundError as exc:
        raise RuntimeError("Graphviz 'dot' is required to build the DAG; install graphviz") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Graphviz DAG layout failed: " + exc.stderr[-2000:]) from exc
    svg = cmd.stdout[cmd.stdout.find("<svg"):cmd.stdout.rfind("</svg>")+6]
    if not svg.startswith("<svg"):
        raise RuntimeError("Graphviz returned no SVG element")

    # Bind stable canonical IDs to real SVG click targets, never to visual
    # positions or family grouping. DOT positions are recomputed on every build.
    for method_id, graphviz_id in node_ids.items():
        marker = f'<g id="{graphviz_id}" class="node">'
        if marker not in svg:
            raise RuntimeError("Graphviz omitted method node: " + method_id)
        svg = svg.replace(marker,
            f'<g id="{graphviz_id}" class="node atlas-node" '
            f'data-method-id="{method_id}" role="button" tabindex="0">', 1)
    for relation_id, graphviz_id in edge_ids.items():
        marker = f'<g id="{graphviz_id}" class="edge">'
        if marker in svg:
            svg = svg.replace(marker,
                f'<g id="{graphviz_id}" class="edge atlas-edge" '
                f'data-edge-id="{relation_id}" role="button" tabindex="0">', 1)
    svg = svg.replace("<svg ", '<svg id="atlas-dag" class="atlas-dag" ', 1)
    return svg


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT/"build"/"atlas-v07.json")
    parser.add_argument("--site", type=Path, default=None)
    args = parser.parse_args()
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    payload = build_payload(build_v06(), config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    svg = build_svg(payload)
    if args.site:
        source = ROOT / "viewer-v07"
        args.site.mkdir(parents=True, exist_ok=True)
        html = (source / "index.html").read_text(encoding="utf-8")
        if '<div id="dag-slot"></div>' not in html or "</body>" not in html:
            raise ValueError("Viewer template missing SVG insertion point")
        html = html.replace('<div id="dag-slot"></div>', svg)
        inline_data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
        html = html.replace("</body>", '<script id="atlas-data" type="application/json">'
            +inline_data+"</script>\n</body>")
        (args.site/"index.html").write_text(html, encoding="utf-8")
        for file in ("app.js","style.css"):
            shutil.copyfile(source/file, args.site/file)
        print("v0.7 offline Graphviz DAG viewer:", args.site)
    print(f"v0.7: {payload['summary']['methods']} methods, "
          f"{payload['summary']['layout_links']} structural DAG edges, "
          f"{payload['summary']['functional_links']} functional mappings, "
          f"3 research phases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
