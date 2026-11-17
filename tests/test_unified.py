"""Unified-axis, method-family and semantic color-encoding regression tests."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from scripts.export_unified import export_unified
from scripts.validate import ROOT, validate_catalog


def fixture(tmp_path: Path) -> Path:
    for directory in ("data", "schemas", "locales"):
        shutil.copytree(ROOT / directory, tmp_path / directory)
    return tmp_path


def edit(root: Path, relative: str, change) -> None:
    path = root / relative
    document = json.loads(path.read_text(encoding="utf-8"))
    change(document)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_unified_views_are_bilingual_and_deterministic():
    zh = export_unified(lang="zh")
    en = export_unified(lang="en")
    assert export_unified(lang="zh") == zh
    assert [x["id"] for x in zh["nodes"]] == [x["id"] for x in en["nodes"]]
    stages = [n for n in zh["nodes"] if n["kind"] == "stage"]
    assert len(stages) == 6
    assert len({x["color"] for x in stages}) == 6
    assert next(n for n in zh["nodes"] if n["id"] == "method.fno")["label"] == "傅里叶神经算子（FNO）"
    assert next(n for n in en["nodes"] if n["id"] == "method.fno")["label"] == "Fourier Neural Operator"
    assert all(n["kind"] in {"stage", "family"} for n in zh["nodes"]
               if n["id"] in zh["views"]["overview"]["node_ids"])


def test_no_duplicate_method_nodes_with_multiple_family_memberships():
    projection = export_unified()
    methods = [n for n in projection["nodes"] if n["kind"] == "method"]
    assert len({n["id"] for n in methods}) == len(methods)
    assert len(methods) == len(list((ROOT / "data" / "methods").glob("*.json")))
    family_links = [e for e in projection["edges"]
                    if e["type"] == "member_of_family" and e["source"] == "method.pino"]
    assert len(family_links) >= 2
    assert len([n for n in methods if n["id"] == "method.pino"]) == 1


def test_functional_roles_are_colored_by_stage_not_family():
    projection = export_unified()
    edges = [e for e in projection["edges"] if e["type"] == "uses_method"]
    assert edges
    assert all(e["category"] == "functional" and e["line_style"] == "dashed" for e in edges)
    assert all(e["stroke"] == projection["palette"][e["source"]] for e in edges)
    assert all(e["data"]["role_zh"] and e["data"]["role"] for e in edges)


def test_genealogy_has_bottleneck_and_primary_stage_coloring():
    projection = export_unified()
    edges = [e for e in projection["edges"] if e["category"] == "genealogy"]
    assert len(edges) >= 10
    assert all(e["data"]["innovation_detail"] and e["data"]["bottleneck"] for e in edges)
    assert all(e["data"]["innovation_detail_zh"] and e["data"]["bottleneck_zh"] for e in edges)
    for edge in edges:
        stage = edge["primary_stage_id"]
        if stage:
            assert stage in edge["stage_ids"]
            assert edge["stroke"] == projection["palette"][stage]


def test_invalid_primary_stage_in_an_evolution_edge_is_rejected(tmp_path):
    root = fixture(tmp_path)
    path = "data/relations/geo-fno--extends--fno.json"
    edit(root, path, lambda x: x.update(primary_stage_id="stage.intervention-planning"))
    assert any("primary_stage_id must appear in stage_ids" in e for e in validate_catalog(root))


def test_undocumented_evolution_bottleneck_fails(tmp_path):
    root = fixture(tmp_path)
    edit(root, "data/relations/pino--extends--fno.json",
         lambda x: x.pop("bottleneck_zh"))
    assert any("bottleneck_zh" in e for e in validate_catalog(root))


def test_duplicate_stage_colors_fail(tmp_path):
    root = fixture(tmp_path)
    edit(root, "data/stages/observation.json", lambda x: x.update(color="#2563EB"))
    assert any("stage color duplicated" in e for e in validate_catalog(root))


def test_family_taxonomy_cycle_is_rejected(tmp_path):
    root = fixture(tmp_path)
    suffix = "family-physical-modeling--subfamily-of--family-numerical-solvers"
    obj = {"schema_version":"2.1.0","id":f"relation.{suffix}",
           "source_id":"family.physical-modeling","target_id":"family.numerical-solvers",
           "type":"subfamily_of","claim":"Intentional test-only family cycle."}
    (root / "data" / "relations" / f"{suffix}.json").write_text(json.dumps(obj), encoding="utf-8")
    assert any("method-family taxonomy: cycle detected" in e for e in validate_catalog(root))


def test_malformed_functional_role_is_rejected(tmp_path):
    root = fixture(tmp_path)
    path = "data/relations/stage-physics-forward--uses-method--family-operator-learning.json"
    edit(root, path, lambda x: x.pop("role_zh"))
    assert any("role_zh" in e for e in validate_catalog(root))


def test_feedback_loop_is_legitimate_and_not_an_ancestry_cycle():
    assert not any("cycle detected" in e for e in validate_catalog())
    x = export_unified()
    assert any(e["type"] == "feeds_back_to" for e in x["edges"])

def test_verified_functional_role_requires_paper_evidence(tmp_path):
    root = fixture(tmp_path)
    path = "data/relations/stage-physics-forward--uses-method--family-operator-learning.json"
    edit(root, path, lambda x: x.update(evidence_scope="application_verified"))
    assert any("verified functional claims require evidence_paper_ids" in e
               for e in validate_catalog(root))
