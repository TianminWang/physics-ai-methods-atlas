"""Regression tests for the Atlas's essential data-integrity rules."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from scripts.export_graph import export_graph
from scripts.validate import ROOT, validate_catalog


def _working_copy(tmp_path: Path) -> Path:
    shutil.copytree(ROOT / "data", tmp_path / "data")
    shutil.copytree(ROOT / "schemas", tmp_path / "schemas")
    return tmp_path


def _edit(root: Path, relpath: str, modify) -> None:
    path = root / relpath
    data = json.loads(path.read_text(encoding="utf-8"))
    modify(data)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )


def test_seed_catalog_valid():
    assert validate_catalog() == []


def test_export_is_deterministic_and_has_typed_links():
    first = export_graph()
    assert first == export_graph()
    assert any(e["type"] == "introduces" for e in first["edges"])
    assert any(n["id"] == "method.fno" for n in first["nodes"])


def test_curated_node_requires_must_read(tmp_path):
    root = _working_copy(tmp_path)
    _edit(root, "data/methods/fno.json", lambda x: x.update(core_reading=[]))
    assert any("curated methods require" in e for e in validate_catalog(root))


def test_core_reading_cannot_exceed_two(tmp_path):
    root = _working_copy(tmp_path)
    def change(x):
        x["core_reading"] = x["core_reading"] * 3
    _edit(root, "data/methods/fno.json", change)
    assert any("too long" in e or "maxItems" in e for e in validate_catalog(root))


def test_core_reading_must_link_paper_to_method(tmp_path):
    root = _working_copy(tmp_path)
    _edit(root, "data/methods/fno.json", lambda x: x["core_reading"][0].update(
        paper_id="paper.raissi-2019-pinn"
    ))
    assert any("needs a paper→method relation" in e for e in validate_catalog(root))


def test_wrong_relationship_endpoint_types_are_caught(tmp_path):
    root = _working_copy(tmp_path)
    path = next((root / "data" / "relations").glob("*.json"))
    data = json.loads(path.read_text(encoding="utf-8"))
    data.update(type="introduces")
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    assert any("invalid source/target types" in e for e in validate_catalog(root))


def test_taxonomy_cycles_are_caught(tmp_path):
    root = _working_copy(tmp_path)
    rels = [
        ("area.forward-modeling", "area.inverse-problems", "cycle-a"),
        ("area.inverse-problems", "area.forward-modeling", "cycle-b"),
    ]
    for src, dst, slug in rels:
        content = {
            "schema_version": "1.0.0",
            "id": f"relation.{slug}", "source_id": src, "target_id": dst,
            "type": "subarea_of", "claim": "Intentionally cyclic test relation."
        }
        path = root / "data" / "relations" / f"{slug}.json"
        path.write_text(json.dumps(content, indent=2), encoding="utf-8")
    assert any("area taxonomy: cycle detected" in e for e in validate_catalog(root))


def test_duplicate_paper_doi_is_caught(tmp_path):
    root = _working_copy(tmp_path)
    _edit(root, "data/papers/lu-2021-deeponet.json", lambda x: x.update(
        identifiers={"doi": "10.1016/j.jcp.2018.10.045"}
    ))
    assert any("duplicate doi" in e for e in validate_catalog(root))


def test_unverified_core_paper_is_caught(tmp_path):
    root = _working_copy(tmp_path)
    _edit(root, "data/papers/li-2021-fno.json", lambda x: x.update(
        verification_status="provisional"
    ))
    assert any("is not verified" in e for e in validate_catalog(root))
