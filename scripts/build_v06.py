"""Generate the v0.6 unified, stage-aware interactive method-map prototype.

One canonical graph. Layout zones are UI-only *presentation* groups: they do
NOT assert one unique scholarly parent. Every method retains all family links.

Run: python -m scripts.build_v06 --site build/unified-v06
"""
from __future__ import annotations

import argparse
import json
import shutil
from collections import defaultdict, deque
from pathlib import Path

from scripts.validate import ROOT, load_catalog, validate_catalog

VIEW_ZONES = (
    ("numerical", "数值与物理建模", "Numerics & physical modeling",
     ("numerical-discretization", "numerical-solvers", "hemodynamic-models",
      "reduced-modeling", "differentiable-simulation")),
    ("inverse", "优化与反问题", "Optimization & inverse problems",
     ("optimization-regularization", "inverse-identifiability", "learned-inverse")),
    ("probabilistic", "概率推断与数据同化", "Probabilistic inference & assimilation",
     ("probabilistic-inference", "bayesian-computation", "sbi-methods",
      "data-assimilation", "uncertainty-quantification", "observation-modeling")),
    ("neural", "神经求解与算子学习", "Neural solvers & operators",
     ("physics-informed-learning", "operator-learning", "graph-neural-operators",
      "attention-neural-operators", "learned-mesh-simulation")),
    ("generative", "生成式建模", "Generative modeling",
     ("generative-modeling", "generative-inverse", "latent-generative",
      "normalizing-flows", "diffusion-score-models", "physics-guided-generative")),
    ("dynamics", "动力学与决策控制", "Dynamics & planning",
     ("dynamics-identification", "latent-world-models", "model-based-control",
      "offline-reinforcement-learning", "control-planning")),
)

EVOLUTION_TYPES = {"extends", "combines", "specializes", "contrasts_with"}
BIBLIO_TYPES = {"introduces", "analyzes", "applies", "surveys", "compares"}


def family_ancestors(family: str, parents: dict[str, set[str]]) -> dict[str, int]:
    distances = {family: 0}
    queue = deque([family])
    while queue:
        current = queue.popleft()
        for ancestor in parents.get(current, ()):
            if ancestor not in distances or distances[ancestor] > distances[current] + 1:
                distances[ancestor] = distances[current] + 1
                queue.append(ancestor)
    return distances


def localized(record: dict, field: str, translations: dict,
              entity_id: str, default: str = "") -> dict[str, str]:
    translated = (
        record.get(field + "_zh")
        or translations.get({"name": "labels", "summary": "summaries",
                             "core_idea": "core_ideas"}.get(field, ""), {}).get(entity_id)
        or record.get(field, default)
    )
    return {"zh": translated, "en": record.get(field, default)}


def build_graph(root: Path = ROOT) -> dict:
    issues = validate_catalog(root)
    if issues:
        raise ValueError("Invalid Atlas:\n" + "\n".join(issues))
    records, _ = load_catalog(root)
    translations = json.loads((root / "locales" / "zh-CN.json").read_text(encoding="utf-8"))

    stages = sorted(
        (v for k, v in records.items() if k.startswith("stage.")),
        key=lambda r: r["order"],
    )
    palette = {stage["id"]: stage["color"] for stage in stages}
    methods = {k: v for k, v in records.items() if k.startswith("method.")}
    families = {k: v for k, v in records.items() if k.startswith("family.")}
    links = [v for k, v in records.items() if k.startswith("relation.")]

    parents: dict[str, set[str]] = defaultdict(set)
    memberships: dict[str, set[str]] = defaultdict(set)
    functional: list[dict] = []
    for link in links:
        if link["type"] == "subfamily_of":
            parents[link["source_id"]].add(link["target_id"])
        elif link["type"] == "member_of_family":
            memberships[link["source_id"]].add(link["target_id"])
        elif link["type"] == "uses_method":
            functional.append({
                "id": link["id"], "stage": link["source_id"], "target": link["target_id"],
                "type": "direct_method" if link["target_id"].startswith("method.") else "family",
                "role": {
                    "zh": link.get("role_zh", link["role"]),
                    "en": link["role"],
                },
                "scope": link.get("evidence_scope", "conceptual"),
                "evidence": [
                    {"id": key, "title": records[key]["title"], "url": records[key]["url"]}
                    for key in link.get("evidence_paper_ids", [])
                ],
            })
    ancestors_by_method: dict[str, dict[str, int]] = {}
    for method_id in methods:
        reachable: dict[str, int] = {}
        for family in memberships.get(method_id, set()):
            for ancestor, distance in family_ancestors(family, parents).items():
                if ancestor not in reachable or distance < reachable[ancestor]:
                    reachable[ancestor] = distance
        ancestors_by_method[method_id] = reachable

    # Only a viewport preference; all other memberships are fully retained.
    zones = []
    placement: dict[str, str] = {}
    zone_members: dict[str, list[str]] = defaultdict(list)
    for slug, zh, en, anchors in VIEW_ZONES:
        zones.append({
            "id": slug, "label": {"zh": zh, "en": en},
            "anchor_families": ["family." + name for name in anchors],
        })
    for method_id in sorted(methods):
        scores = []
        for zone in zones:
            exact = set(zone["anchor_families"]) & memberships.get(method_id, set())
            inherited = set(zone["anchor_families"]) & set(ancestors_by_method[method_id])
            # A direct family wins over a distant ancestor; tie-break is stable
            # and *only determines a single viewport location*, not taxonomy.
            direct_score = 2 if exact else 0
            closest = min((ancestors_by_method[method_id][x] for x in inherited), default=999)
            scores.append((direct_score, -closest, -len(inherited), zone["id"]))
        selected = max(scores, key=lambda x: (x[0], x[1], x[2], -next(
            i for i, z in enumerate(zones) if z["id"] == x[3]
        )))[3]
        if max(s[0] for s in scores) == 0 and all(s[1] == -999 for s in scores):
            raise ValueError(f"No presentational zone found for {method_id}")
        placement[method_id] = selected
        zone_members[selected].append(method_id)

    stage_roles: dict[str, dict[str, list[dict]]] = {
        s["id"]: defaultdict(list) for s in stages
    }
    for rel in functional:
        targets = []
        if rel["target"].startswith("method."):
            targets = [(rel["target"], "direct", 0)]
        else:
            targets = [
                (mid, "family" if dist == 0 else "ancestor_family", dist)
                for mid, reach in ancestors_by_method.items()
                if (dist := reach.get(rel["target"])) is not None
            ]
        for mid, level, distance in targets:
            # Family-level applicability MUST NOT be silently upgraded to
            # direct paper-verified method applicability.
            stage_roles[rel["stage"]][mid].append({
                "relation_id": rel["id"], "level": level,
                "via_family_id": rel["target"] if level != "direct" else None,
                "family_distance": distance, "scope": rel["scope"],
                "role": rel["role"], "evidence": rel["evidence"],
            })

    nodes = []
    for mid, m in sorted(methods.items()):
        readings = []
        for recommendation in m.get("start_here", []):
            reference = records[recommendation["reference_id"]]
            readings.append({
                "id": reference["id"], "title": reference["title"], "url": reference["url"],
                "focus": recommendation.get("focus", ""),
                "why": recommendation.get("why", ""),
                "locator": recommendation.get("locator", ""),
            })
        sources = []
        for r in links:
            if r["target_id"] != mid or r["type"] not in BIBLIO_TYPES:
                continue
            paper = records[r["source_id"]]
            sources.append({
                "id": paper["id"], "title": paper["title"], "url": paper["url"],
                "year": paper["year"], "role": r["type"],
                "landmark": r.get("significance") == "landmark",
                "claim": r.get("claim", ""),
            })
        nodes.append({
            "id": mid, "label": localized(m, "name", translations, mid),
            "summary": localized(m, "summary", translations, mid),
            "core": localized(m, "core_idea", translations, mid),
            "limitations": {
                "zh": ([translations["limitations_summary"][mid]] if mid in
                       translations.get("limitations_summary", {})
                       else m.get("limitations", [])),
                "en": m.get("limitations", []),
            },
            "zone": placement[mid],
            "families": sorted(memberships.get(mid, set())),
            "ancestor_families": ancestors_by_method[mid],
            "readings": readings, "sources": sorted(sources, key=lambda x: (-int(x["landmark"]), -x["year"], x["id"])),
            "source_path": "data/methods/" + mid.split(".", 1)[1] + ".json",
            "status": m.get("status", "draft"),
        })

    method_edges = []
    for link in links:
        if link["type"] not in EVOLUTION_TYPES:
            continue
        if link["source_id"] not in methods or link["target_id"] not in methods:
            continue
        if link["type"] in ("extends", "combines", "specializes"):
            source, target = link["target_id"], link["source_id"]
        else:
            source, target = link["source_id"], link["target_id"]
        method_edges.append({
            "id": link["id"], "source": source, "target": target, "type": link["type"],
            "innovation": {
                "zh": link.get("innovation_detail_zh") or link.get("claim_zh") or link["claim"],
                "en": link.get("innovation_detail") or link["claim"],
            },
            "bottleneck": {"zh": link.get("bottleneck_zh", ""), "en": link.get("bottleneck", "")},
            "tradeoff": {"zh": link.get("tradeoff_zh", link.get("tradeoff", "")),
                         "en": link.get("tradeoff", "")},
            "stages": link.get("stage_ids", []),
            "primary_stage": link.get("primary_stage_id"),
            "color": palette.get(link.get("primary_stage_id"), "#9AA8B9"),
            "evidence": [
                {"id": key, "title": records[key]["title"], "url": records[key]["url"]}
                for key in link.get("evidence_paper_ids", [])
            ],
            "source_path": "data/relations/" + link["id"].split(".", 1)[1] + ".json",
        })

    return {
        "version": "0.6.0",
        "provenance": "Generated solely from the versioned canonical Atlas records",
        "stages": [{
            "id": s["id"], "order": s["order"], "color": s["color"],
            "name": localized(s, "name", translations, s["id"]),
            "summary": localized(s, "summary", translations, s["id"]),
        } for s in stages],
        "families": [{
            "id": key, "name": localized(value, "name", translations, key),
            "summary": localized(value, "summary", translations, key),
        } for key, value in sorted(families.items())],
        "zones": [{**z, "method_ids": sorted(zone_members[z["id"]])} for z in zones],
        "methods": nodes, "method_edges": sorted(method_edges, key=lambda x: x["id"]),
        "functional": sorted(functional, key=lambda x: x["id"]),
        "stage_roles": {sid: {mid: sorted(roles, key=lambda x: (
            {"direct": 0, "family": 1, "ancestor_family": 2}[x["level"]],
            x["family_distance"], x["relation_id"]
        )) for mid, roles in sorted(methods_map.items())}
            for sid, methods_map in stage_roles.items()},
        "summary": {
            "methods": len(methods), "families": len(families),
            "genealogy_edges": len(method_edges),
            "functional_edges": len(functional),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "unified-v06.json")
    parser.add_argument("--site", type=Path, default=None,
                        help="Create offline HTML, CSS and JS in this directory")
    args = parser.parse_args()
    payload = build_graph()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.site is not None:
        source = ROOT / "viewer-v06"
        args.site.mkdir(parents=True, exist_ok=True)
        html = (source / "index.html").read_text(encoding="utf-8")
        if "</body>" not in html:
            raise ValueError("Invalid HTML template, missing closing body")
        embedded = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
        html = html.replace("</body>", '<script type="application/json" id="atlas-data">'
                            + embedded + "</script>\n</body>")
        (args.site / "index.html").write_text(html, encoding="utf-8")
        for asset in ("style.css", "app.js"):
            shutil.copyfile(source / asset, args.site / asset)
        print("Offline viewer exported to", args.site)
    print(
        f"v0.6 graph: {len(payload['methods'])} methods, "
        f"{len(payload['method_edges'])} method links, "
        f"{len(payload['functional'])} functional mapping edges"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
