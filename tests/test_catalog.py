"""Checks that method-reading suggestions stay advisory and graph data is consistent."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from scripts.export_graph import export_graph
from scripts.validate import ROOT, validate_catalog


def copy_data(tmp_path: Path) -> Path:
    shutil.copytree(ROOT / "data", tmp_path / "data")
    shutil.copytree(ROOT / "schemas", tmp_path / "schemas")
    return tmp_path


def mutate(root, name, callback):
    file = root / name
    obj = json.loads(file.read_text(encoding="utf-8"))
    callback(obj)
    file.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def test_catalog_valid():
    assert validate_catalog() == []


def test_graph_export_reproducible():
    graph = export_graph()
    assert graph == export_graph()
    assert any(n["id"] == "method.fno" for n in graph["nodes"])


def test_curated_nodes_can_have_no_recommendations(tmp_path):
    root = copy_data(tmp_path)
    mutate(root, "data/methods/fno.json", lambda o: o.update(start_here=[]))
    assert validate_catalog(root) == []


def test_three_recommendations_are_not_disallowed_by_quota(tmp_path):
    root = copy_data(tmp_path)
    def edit(o):
        o["start_here"] = o["start_here"] + [
            {"reference_id": "paper.raissi-2019-pinn", "why": "Physical constraints context", "focus": "Differential residual loss"},
            {"reference_id": "paper.lu-2021-deeponet", "why": "Competing operator architecture", "focus": "Branch and trunk networks"},
        ]
    mutate(root, "data/methods/fno.json", edit)
    errors = validate_catalog(root)
    assert not any("maxItems" in e or "require 1–2" in e for e in errors)
    assert any("requires a paper→method relation" in e for e in errors)


def test_missing_starting_reference_detected(tmp_path):
    root = copy_data(tmp_path)
    mutate(root, "data/methods/fno.json", lambda o: o["start_here"][0].update(reference_id="paper.nonexistent"))
    assert any("missing starting reference" in e for e in validate_catalog(root))


def test_unverified_starting_paper_detected(tmp_path):
    root = copy_data(tmp_path)
    mutate(root, "data/papers/li-2021-fno.json", lambda o: o.update(verification_status="provisional"))
    assert any("is not verified" in e for e in validate_catalog(root))


def test_landmark_significance_requires_justification(tmp_path):
    root = copy_data(tmp_path)
    mutate(root, "data/relations/li-2021-fno--introduces--fno.json", lambda o: o.pop("significance_reason"))
    assert any("significance_reason" in e or "justify" in e for e in validate_catalog(root))


def test_bad_relation_types_detected(tmp_path):
    root = copy_data(tmp_path)
    mutate(root, "data/relations/pinn--belongs-to--physics-ai.json", lambda o: o.update(type="introduces"))
    assert any("invalid source/target types" in e for e in validate_catalog(root))


def test_taxonomy_cycle_detected(tmp_path):
    root = copy_data(tmp_path)
    for x, y, slug in [
        ("area.forward-modeling","area.inverse-problems","cycle-a"),
        ("area.inverse-problems","area.forward-modeling","cycle-b"),
    ]:
        item = {"schema_version":"2.0.0","id":f"relation.{slug}",
                "source_id":x,"target_id":y,"type":"subarea_of",
                "claim":"Intentional cyclic relationship for a regression test."}
        (root / "data" / "relations" / f"{slug}.json").write_text(json.dumps(item), encoding="utf-8")
    assert any("area taxonomy: cycle detected" in e for e in validate_catalog(root))


def test_duplicate_doi_detected(tmp_path):
    root = copy_data(tmp_path)
    mutate(root, "data/papers/lu-2021-deeponet.json",
           lambda o: o.update(identifiers={"doi":"10.1016/j.jcp.2018.10.045"}))
    assert any("duplicate doi" in e for e in validate_catalog(root))
