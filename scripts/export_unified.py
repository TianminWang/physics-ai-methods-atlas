"""Build deterministic bilingual workflow + method-DAG projections.

Generate:
  python -m scripts.export_unified --lang zh --output build/unified-zh.json
  python -m scripts.export_unified --lang en --output build/unified-en.json

This is not the final interactive UI. It is a render-ready contract for Phase v1.0.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.validate import ROOT, load_catalog, validate_catalog

DISPLAY_KINDS = {"stage", "family", "method", "concern"}
VISUAL_RELATIONS = {
    "feeds_into", "feeds_back_to", "uses_method", "member_of_family",
    "subfamily_of", "concern_applies_to",
    "specializes", "extends", "combines", "depends_on", "contrasts_with",
}
SUMMARY_RELATIONS = {"feeds_into", "feeds_back_to", "uses_method", "subfamily_of"}
EVOLUTION_RELATIONS = {"extends", "combines"}
DEFAULT_EDGE_COLOR = "#64748B"


def _locale_labels(root: Path, lang: str) -> dict[str, str]:
    if lang != "zh":
        return {}
    path = root / "locales" / "zh-CN.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["labels"]


def export_unified(root: Path = ROOT, lang: str = "zh") -> dict:
    if lang not in {"zh", "en"}:
        raise ValueError("lang must be zh or en")
    errors = validate_catalog(root)
    if errors:
        raise ValueError("Cannot export invalid knowledge graph:\n" + "\n".join(errors))
    records, _ = load_catalog(root)
    labels = _locale_labels(root, lang)
    stages = sorted(
        (record for key, record in records.items() if key.startswith("stage.")),
        key=lambda x: (x["order"], x["id"]),
    )
    palette = {record["id"]: record["color"] for record in stages}
    nodes = []
    for key, record in sorted(records.items()):
        kind = key.split(".", 1)[0]
        if kind not in DISPLAY_KINDS:
            continue
        label = (record.get("name_zh") or labels.get(key) or record["name"]
                 if lang == "zh" else record["name"])
        nodes.append({
            "id": key, "kind": kind, "label": label,
            "label_en": record["name"],
            "status": record.get("coverage_status", record.get("status", "active")),
            "color": record["color"] if kind == "stage" else None,
            "order": record.get("order"),
            "data": record,
        })
    display_ids = {node["id"] for node in nodes}
    links = []
    for key, record in sorted(records.items()):
        if not key.startswith("relation.") or record["type"] not in VISUAL_RELATIONS:
            continue
        if record["source_id"] not in display_ids or record["target_id"] not in display_ids:
            continue
        kind = record["type"]
        if kind in EVOLUTION_RELATIONS:
            category = "genealogy"
            label = (record.get("innovation_detail_zh") or
                     record["innovation_detail"]) if lang == "zh" else record["innovation_detail"]
            stage_id = record.get("primary_stage_id")
            color = palette.get(stage_id, DEFAULT_EDGE_COLOR)
            line_style = "solid" if kind == "extends" else "double"
        elif kind == "uses_method":
            category = "functional"
            label = record["role_zh"] if lang == "zh" else record["role"]
            color = palette.get(record["source_id"], DEFAULT_EDGE_COLOR)
            line_style = "dashed"
        elif kind in {"feeds_into", "feeds_back_to"}:
            category = "workflow"
            label = record.get("claim_zh", record["claim"]) if lang == "zh" else record["claim"]
            color = palette.get(record["source_id"], DEFAULT_EDGE_COLOR)
            line_style = "solid" if kind == "feeds_into" else "dashed"
        else:
            category = "crosscutting" if kind == "concern_applies_to" else "taxonomy"
            label = record.get("claim_zh", record["claim"]) if lang == "zh" else record["claim"]
            color = DEFAULT_EDGE_COLOR
            line_style = "dotted" if category == "crosscutting" else "thin"
        links.append({
            "id": key, "source": record["source_id"], "target": record["target_id"],
            "type": kind, "category": category, "label": label,
            "stroke": color, "line_style": line_style,
            "primary_stage_id": record.get("primary_stage_id"),
            "stage_ids": record.get("stage_ids", []),
            "data": record,
        })
    summary_nodes = sorted(
        node["id"] for node in nodes if node["kind"] in {"stage", "family"}
    )
    summary_links = [
        link["id"] for link in links if link["type"] in SUMMARY_RELATIONS
    ]
    return {
        "schema_version": "2.1.0",
        "lang": lang,
        "workflow_axis": [record["id"] for record in stages],
        "palette": palette,
        "nodes": nodes,
        "edges": links,
        "views": {
            "overview": {"node_ids": summary_nodes, "edge_ids": summary_links},
            "expanded": {"node_ids": sorted(display_ids),
                         "edge_ids": [edge["id"] for edge in links]},
        },
        "legend": {
            "functional": "dashed stage-to-family/method link; color = workflow stage",
            "genealogy": "solid/double evidence-backed method evolution; color = primary addressed stage",
            "taxonomy": "neutral method/family classification, not historical change",
            "crosscutting": "neutral concern link, not another workflow step",
            "workflow": "ordered input/feedback links; updates can form cycles",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lang", choices=["zh", "en"], default="zh")
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "unified-zh.json")
    args = parser.parse_args()
    data = export_unified(lang=args.lang)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"Unified graph ({args.lang}): {len(data['nodes'])} display nodes, "
        f"{len(data['edges'])} typed edges → {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
