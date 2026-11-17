"""Build a deterministic, evidence-linked interactive layout prototype from canonical Atlas records.

The prototype is intentionally limited to three real method lineages. No literature,
method, or relationship is copied into a second editable database.

Usage:
    python -m scripts.build_prototype --output prototype/data/preview.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.export_unified import export_unified
from scripts.validate import ROOT, load_catalog, validate_catalog

TRACKS = (
    {
        "id": "inverse",
        "featured": (
            "nonlinear-least-squares", "gauss-newton", "levenberg-marquardt",
            "tikhonov-regularization", "bayesian-inverse-problems",
            "bayesian-model-discrepancy", "learned-forward-inversion",
        ),
        "title": {"zh": "传统与概率反问题", "en": "Classical & probabilistic inversion"},
        "description": {"zh": "从最小二乘、正则化到贝叶斯与代理反演", "en": "Least squares, regularization, Bayesian and surrogate inversion"},
        "families": ("optimization-regularization", "probabilistic-inference", "learned-inverse"),
        "methods": (
            "nonlinear-least-squares", "gauss-newton", "levenberg-marquardt",
            "tikhonov-regularization", "adjoint-sensitivity",
            "pde-constrained-optimization", "bayesian-inverse-problems",
            "bayesian-model-discrepancy", "learned-forward-inversion",
        ),
    },
    {
        "id": "operator",
        "featured": (
            "neural-operator", "pinn", "deeponet", "fno",
            "physics-informed-deeponet", "pino", "geo-fno",
        ),
        "title": {"zh": "神经算子与物理约束", "en": "Neural operators & physics"},
        "description": {"zh": "算子家族、频谱/基展开与物理约束融合", "en": "Operator families, spectral bases, physics-guided training"},
        "families": ("operator-learning", "physics-informed-learning", "graph-neural-operators"),
        "methods": (
            "neural-operator", "deeponet", "fno", "pinn",
            "physics-informed-deeponet", "pino", "geo-fno",
            "derivative-informed-operator", "multipole-graph-neural-operator",
            "galerkin-transformer",
        ),
    },
    {
        "id": "generative",
        "featured": (
            "variational-inference", "variational-autoencoder",
            "normalizing-flow", "flow-matching", "diffusion-probabilistic-model",
            "score-based-sde", "diffusion-posterior-sampling", "physics-informed-diffusion",
        ),
        "title": {"zh": "生成式建模与反问题", "en": "Generative models & inverse problems"},
        "description": {"zh": "从生成模型与概率路径到条件反演和物理约束", "en": "Generative priors, probabilistic paths, inverse guidance"},
        "families": ("generative-modeling", "generative-inverse", "diffusion-score-models", "physics-guided-generative"),
        "methods": (
            "variational-inference", "variational-autoencoder",
            "normalizing-flow", "flow-matching", "diffusion-probabilistic-model",
            "score-based-sde", "diffusion-posterior-sampling",
            "physics-informed-diffusion", "generative-range-prior",
        ),
    },
)
EDGE_CAPTIONS = {
    "relation.levenberg-marquardt--extends--gauss-newton": ("阻尼稳定化", "Damped steps"),
    "relation.bayesian-model-discrepancy--specializes--bayesian-inverse-problems": ("模型失配", "Model discrepancy"),
    "relation.physics-informed-deeponet--extends--deeponet": ("PDE 残差监督", "PDE residuals"),
    "relation.physics-informed-deeponet--combines--pinn": ("融合 PINN 约束", "PINN constraint"),
    "relation.pino--extends--fno": ("加入物理约束", "Physics constraints"),
    "relation.pino--combines--pinn": ("融合 PINN 损失", "PINN losses"),
    "relation.geo-fno--extends--fno": ("适应复杂几何", "General geometry"),
    "relation.derivative-informed-operator--extends--neural-operator": ("导数监督", "Derivative targets"),
    "relation.score-based-sde--extends--diffusion-probabilistic-model": ("连续时间 SDE", "Continuous SDE"),
    "relation.diffusion-posterior-sampling--extends--score-based-sde": ("观测引导采样", "Data guidance"),
    "relation.physics-informed-diffusion--extends--diffusion-probabilistic-model": ("物理残差损失", "Physics residuals"),
    "relation.flow-matching--extends--normalizing-flow": ("速度场回归", "Vector-field fitting"),
    "relation.variational-autoencoder--combines--variational-inference": ("摊销变分推断", "Amortized inference"),
}

EDGE_TYPES = {
    "feeds_into", "feeds_back_to", "uses_method", "member_of_family",
    "subfamily_of", "specializes", "extends", "combines", "contrasts_with",
}


def build_prototype(root: Path = ROOT) -> dict:
    errors = validate_catalog(root)
    if errors:
        raise ValueError("Invalid canonical Atlas data:\n" + "\n".join(errors))
    zh = export_unified(root, "zh")
    en = export_unified(root, "en")
    records, _ = load_catalog(root)
    translations = json.loads((root / "locales" / "zh-CN.json").read_text(encoding="utf-8"))
    zh_index = {n["id"]: n for n in zh["nodes"]}
    en_index = {n["id"]: n for n in en["nodes"]}
    method_ids = {
        "method." + name for track in TRACKS for name in track["methods"]
    }
    family_ids = {
        "family." + name for track in TRACKS for name in track["families"]
    }
    stage_ids = set(zh["workflow_axis"])
    visible = method_ids | family_ids | stage_ids

    missing = visible - set(zh_index)
    if missing:
        raise ValueError("Prototype track references missing Atlas IDs: " + ", ".join(sorted(missing)))

    links_by_method = {}
    for key, record in records.items():
        if not key.startswith("relation."):
            continue
        if record.get("source_id", "").startswith("paper.") and record.get("target_id") in method_ids:
            links_by_method.setdefault(record["target_id"], []).append(record)

    nodes = []
    for entity_id in sorted(visible):
        record = records[entity_id]
        kind = entity_id.split(".", 1)[0]
        display_zh = zh_index[entity_id]
        display_en = en_index[entity_id]
        readings = []
        sources = []
        if kind == "method":
            for reading in record.get("start_here", []):
                ref = records[reading["reference_id"]]
                readings.append({
                    "id": reading["reference_id"],
                    "title": ref["title"] if reading["reference_id"].startswith("paper.") else ref["title"],
                    "url": ref.get("url"),
                    "why": reading["why"],
                    "focus": reading["focus"],
                    "locator": reading.get("locator"),
                })
            for rel in sorted(links_by_method.get(entity_id, []), key=lambda r: r["id"]):
                paper = records[rel["source_id"]]
                sources.append({
                    "id": paper["id"], "title": paper["title"],
                    "url": paper.get("url"), "year": paper["year"],
                    "role": rel["type"], "significance": rel.get("significance"),
                    "claim": rel["claim"],
                })

        nodes.append({
            "id": entity_id,
            "kind": kind,
            "label": {"zh": display_zh["label"], "en": display_en["label"]},
            "summary": {
                "zh": record.get("summary_zh", record.get("summary", "")),
                "en": record.get("summary", ""),
            },
            "core_idea": {
                "zh": translations.get("core_ideas", {}).get(entity_id, record.get("core_idea_zh", record.get("core_idea", ""))),
                "en": record.get("core_idea", ""),
            },
            "limitations": {
                "zh": [translations["limitations_summary"][entity_id]] if entity_id in translations.get("limitations_summary", {}) else record.get("limitations", []),
                "en": record.get("limitations", []),
            },
            "color": record.get("color"),
            "order": record.get("order"),
            "status": display_en.get("status"),
            "readings": readings,
            "sources": sources,
            "source_path": (
                "data/" + {"stage": "stages", "family": "families", "method": "methods"}[kind]
                + "/" + entity_id.split(".", 1)[1] + ".json"
            ),
        })

    edges = []
    for edge in zh["edges"]:
        if edge["type"] not in EDGE_TYPES:
            continue
        if edge["source"] not in visible or edge["target"] not in visible:
            continue
        original = edge["data"]
        is_genealogy = edge["type"] in {"specializes", "extends", "combines"}
        # Canonical method direction is successor -> predecessor; display is predecessor -> successor.
        start = edge["target"] if is_genealogy else edge["source"]
        end = edge["source"] if is_genealogy else edge["target"]
        edges.append({
            "id": edge["id"], "source": start, "target": end,
            "type": edge["type"], "category": edge["category"],
            "label": {
                "zh": edge["label"],
                "en": "",  # assigned from English projection below
            },
            "color": edge["stroke"], "line_style": edge["line_style"],
            "short_label": {
                "zh": EDGE_CAPTIONS[edge["id"]][0],
                "en": EDGE_CAPTIONS[edge["id"]][1],
            } if edge["id"] in EDGE_CAPTIONS else None,
            "stage_ids": edge.get("stage_ids", []),
            "primary_stage_id": edge.get("primary_stage_id"),
            "role": {
                "zh": original.get("role_zh", ""),
                "en": original.get("role", ""),
            },
            "innovation": {
                "zh": original.get("innovation_detail_zh", original.get("claim_zh", "")),
                "en": original.get("innovation_detail", original.get("claim", "")),
            },
            "bottleneck": {
                "zh": original.get("bottleneck_zh", ""),
                "en": original.get("bottleneck", ""),
            },
            "tradeoff": original.get("tradeoff", ""),
            "evidence": [
                {
                    "title": records[ref]["title"],
                    "url": records[ref]["url"],
                    "id": ref,
                }
                for ref in original.get("evidence_paper_ids", [])
            ],
        })
    en_edges = {e["id"]: e for e in en["edges"]}
    for edge in edges:
        edge["label"]["en"] = en_edges[edge["id"]]["label"]

    output = {
        "version": "0.5.0",
        "description": "Derived preview of three real branches of the canonical Physics AI Methods Atlas",
        "workflow": zh["workflow_axis"],
        "palette": zh["palette"],
        "tracks": [
            {
                "id": track["id"],
                "title": track["title"],
                "description": track["description"],
                "family_ids": ["family." + x for x in track["families"]],
                "method_ids": ["method." + x for x in track["methods"]],
                "featured_ids": ["method." + x for x in track["featured"]],
            }
            for track in TRACKS
        ],
        "nodes": nodes,
        "edges": sorted(edges, key=lambda e: e["id"]),
        "counts": {"method_count": len(method_ids), "family_count": len(family_ids)},
    }
    assert len({n["id"] for n in nodes}) == len(nodes)
    assert len({e["id"] for e in edges}) == len(edges)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "prototype" / "data" / "preview.json")
    parser.add_argument("--site", type=Path, default=None, help="Build a portable standalone HTML preview directory")
    args = parser.parse_args()
    payload = build_prototype()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.site is not None:
        from shutil import copyfile
        args.site.mkdir(parents=True, exist_ok=True)
        source_html = (ROOT / "prototype" / "index.html").read_text(encoding="utf-8")
        # Standalone ZIP can be opened directly from file:// without a server.
        json_blob = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
        embedded = '<script id="atlas-embedded-data" type="application/json">' + json_blob + '</script>'
        if "</body>" not in source_html:
            raise ValueError("Prototype HTML is missing a closing body tag")
        source_html = source_html.replace("</body>", embedded + chr(10) + "</body>")
        (args.site / "index.html").write_text(source_html, encoding="utf-8")
        for asset in ("style.css", "app.js"):
            copyfile(ROOT / "prototype" / asset, args.site / asset)
        print(f"Portable static preview: {args.site}")
    print(
        f"Prototype built: {len(payload['nodes'])} unique nodes, "
        f"{len(payload['edges'])} typed links, {len(payload['tracks'])} tracks -> {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
