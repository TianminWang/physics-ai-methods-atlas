"""v0.8 evidence-first graph layout, no-fabrication and isolate handling."""
from __future__ import annotations

import json
import re

from scripts.build_v06 import build_graph as build_v06
from scripts.build_v07 import CONFIG
from scripts.build_v08 import (
    GENEALOGY, build_payload_v08, connected_components,
    create_compact_dot, create_compact_svg,
)


def dataset():
    return build_payload_v08(
        build_v06(), json.loads(CONFIG.read_text(encoding="utf-8"))
    )


def test_complete_canonical_methods_partition_without_duplication():
    p = dataset()
    full = {m["id"] for m in p["methods"]}
    linked = set(p["core_method_ids"])
    unlinked = set(p["unlinked_method_ids"])
    assert len(full) >= 61
    assert linked and unlinked and linked.isdisjoint(unlinked)
    assert linked | unlinked == full
    assert p["summary"]["core_methods"] == len(linked)
    assert p["summary"]["unlinked_methods"] == len(unlinked)


def test_main_canvas_includes_exactly_methods_with_real_lineage_edges():
    p = dataset()
    expected = {
        mid for e in p["method_edges"] if e["type"] in GENEALOGY
        for mid in (e["source"], e["target"])
    }
    assert set(p["core_method_ids"]) == expected
    assert all(e["evidence"] for e in p["method_edges"]
               if e["type"] in GENEALOGY)
    # "Unlinked" means no documented evolution edge; taxonomy is still allowed.
    assert any(
        e["type"] == "specializes" and
        (e["source"] in p["unlinked_method_ids"] or
         e["target"] in p["unlinked_method_ids"])
        for e in p["method_edges"]
    )


def test_components_are_faithful_without_artificial_connectors():
    p = dataset()
    methods = set(p["core_method_ids"])
    parts = p["components"]
    assert all(c["size"] >= 2 for c in parts)
    assert set().union(*(set(c["method_ids"]) for c in parts)) == methods
    assert sum(c["size"] for c in parts) == len(methods)
    assert all(c["id"].startswith("lineage-") for c in parts)
    evolution = [e for e in p["method_edges"] if e["type"] in GENEALOGY]
    assert len(connected_components(methods, evolution)) == len(parts)


def test_graphviz_prefers_evolution_and_relaxes_classification_rank():
    p = dataset()
    dot, node_ids, edge_ids = create_compact_dot(p)
    assert 'rankdir=LR' in dot
    assert 'packmode="graph"' in dot
    assert len(node_ids) == len(p["core_method_ids"])
    assert len(edge_ids) >= p["summary"]["lineage_links"]
    assert "constraint=true" in dot
    # taxonomy may be visible but should not force a historical DAG rank
    taxonomy_lines = [line for line in dot.splitlines()
                      if "style=dotted" in line]
    assert taxonomy_lines
    assert all("constraint=false" in line for line in taxonomy_lines)
    assert "constraint=false" in dot


def test_graphviz_clickable_svg_contains_exactly_main_canvas_methods():
    p = dataset()
    svg = create_compact_svg(p)
    ids = re.findall(r'data-method-id="([^"]+)"', svg)
    assert len(ids) == len(set(ids)) == len(p["core_method_ids"])
    assert set(ids) == set(p["core_method_ids"])
    assert 'data-edge-id="relation.pino--extends--fno"' in svg
    assert 'data-edge-id="relation.levenberg-marquardt--extends--gauss-newton"' in svg
    assert not any(x in svg for x in
                   ['data-method-id="' + id + '"' for id in p["unlinked_method_ids"]])


def test_stage_colors_and_family_roles_unchanged():
    p = dataset()
    phases = {v["id"]: v for v in p["phases"]}
    edge = next(e for e in p["method_edges"]
                if e["id"] == "relation.pino--extends--fno")
    assert edge["primary_phase"] == "modeling"
    assert edge["color"] == phases["modeling"]["color"]
    roles = p["phase_roles"]["inference"]["method.fno"]
    assert not any(r["level"] == "direct" for r in roles)
    assert any(r["level"] in {"family", "ancestor_family"} for r in roles)
    assert p["layout_policy"]["no_fabricated_edges"] is True


def test_deterministic_json_contract_and_representative_sources():
    p = dataset()
    assert p == dataset()
    assert json.loads(json.dumps(p, ensure_ascii=False)) == p
    fno = next(m for m in p["methods"] if m["id"] == "method.fno")
    assert fno["readings"] and any(s["landmark"] for s in fno["sources"])
    assert all(s["url"].startswith("https://") for s in fno["readings"])
