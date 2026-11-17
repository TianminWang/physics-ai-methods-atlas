"""Tests for v0.5 single-source, three-branch interactive preview."""
from __future__ import annotations

import json
from pathlib import Path

from scripts.build_prototype import ROOT, TRACKS, build_prototype


def test_preview_uses_three_research_tracks():
    view = build_prototype()
    assert {x["id"] for x in view["tracks"]} == {"inverse", "operator", "generative"}
    assert len(view["workflow"]) == 6
    assert len(set(view["workflow"])) == 6
    assert len(view["nodes"]) >= 25


def test_each_selected_method_is_a_unique_canonical_node():
    view = build_prototype()
    methods = [n for n in view["nodes"] if n["kind"] == "method"]
    assert len(methods) == len({n["id"] for n in methods})
    expected = {"method." + slug for tr in TRACKS for slug in tr["methods"]}
    assert {x["id"] for x in methods} == expected
    assert all((ROOT / n["source_path"]).exists() for n in view["nodes"])


def test_all_visible_edges_reference_existing_nodes():
    view = build_prototype()
    ids = {n["id"] for n in view["nodes"]}
    assert all(e["source"] in ids and e["target"] in ids for e in view["edges"])
    assert len(view["edges"]) == len({e["id"] for e in view["edges"]})


def test_genealogy_draws_predecessor_before_successor():
    view = build_prototype()
    edges = {e["id"]: e for e in view["edges"]}
    fno_to_pino = edges["relation.pino--extends--fno"]
    assert fno_to_pino["source"] == "method.fno"
    assert fno_to_pino["target"] == "method.pino"
    assert fno_to_pino["type"] == "extends"
    assert fno_to_pino["evidence"]
    assert fno_to_pino["color"] == view["palette"][fno_to_pino["primary_stage_id"]]


def test_stage_to_family_roles_are_not_method_ancestry():
    view = build_prototype()
    roles = [x for x in view["edges"] if x["type"] == "uses_method"]
    assert roles
    assert all(x["source"].startswith("stage.") for x in roles)
    assert all(x["role"]["zh"] and x["role"]["en"] for x in roles)
    assert all(x["color"] == view["palette"][x["source"]] for x in roles)


def test_optional_reading_and_landmark_sources_are_derived():
    view = build_prototype()
    methods = {x["id"]: x for x in view["nodes"] if x["kind"] == "method"}
    fno = methods["method.fno"]
    assert fno["readings"]
    assert any("Fourier" in item["title"] for item in fno["readings"])
    assert any(item["significance"] == "landmark" for item in fno["sources"])
    assert all(p["url"].startswith("https://") for p in fno["readings"])


def test_bilingual_descriptions_and_distinct_stages():
    view = build_prototype()
    stages = [n for n in view["nodes"] if n["kind"] == "stage"]
    assert len({n["color"] for n in stages}) == 6
    assert all(n["label"]["zh"] and n["label"]["en"] for n in stages)
    assert view["palette"]["stage.inverse-calibration"] != view["palette"]["stage.physics-forward"]


def test_preview_is_deterministic_and_json_serializable():
    left = build_prototype()
    right = build_prototype()
    assert left == right
    assert json.loads(json.dumps(left, ensure_ascii=False)) == left


def test_featured_subgraph_is_a_true_subset_of_the_canonical_track():
    data = build_prototype()
    for tr in data["tracks"]:
        assert tr["featured_ids"]
        assert set(tr["featured_ids"]).issubset(set(tr["method_ids"]))
        assert len(tr["featured_ids"]) < len(tr["method_ids"])
    graph_edges = [e for e in data["edges"] if e["type"] in {"extends", "combines"}]
    assert any(e["short_label"] for e in graph_edges)
