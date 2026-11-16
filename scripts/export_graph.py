"""Export normalized, UI-ready graph data from the authoritative JSON records.

Run: python -m scripts.export_graph --output build/atlas-graph.json
The result is generated and intentionally not tracked in git.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.validate import ROOT, load_catalog, validate_catalog


def export_graph(root: Path = ROOT) -> dict:
    errors = validate_catalog(root)
    if errors:
        raise ValueError("Cannot export an invalid atlas:\n" + "\n".join(errors))
    records, _ = load_catalog(root)
    nodes = []
    edges = []
    for entity_id, record in sorted(records.items()):
        kind = entity_id.split(".", 1)[0]
        if kind == "relation":
            edges.append(dict(record))
        else:
            nodes.append({
                "id": entity_id,
                "kind": kind,
                "label": record.get("name", record.get("title", entity_id)),
                "data": record,
            })
    return {"schema_version": "1.0.0", "nodes": nodes, "edges": edges}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "build" / "atlas-graph.json"
    )
    args = parser.parse_args()
    graph = export_graph()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    print(
        f"Exported {len(graph['nodes'])} nodes, {len(graph['edges'])} "
        f"edges to {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
