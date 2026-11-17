"""Tests for the three-phase atlas projection and the real Graphviz DAG layout."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from scripts.build_v06 import build_graph as build_v06
from scripts.build_v07 import CONFIG, LAYOUT_TYPES, build_payload, build_svg, create_dot, _check_acyclic

def _data():
    config=json.loads(CONFIG.read_text(encoding="utf-8"))
    return build_payload(build_v06(),config)

def test_three_phases_partition_existing_six_capabilities():
    result=_data()
    assert len(result["phases"])==3
    stage_ids=[sid for p in result["phases"] for sid in p["stage_ids"]]
    assert len(stage_ids)==len(set(stage_ids))==6
    assert set(stage_ids)=={s["id"] for s in result["subcapabilities"]}
    assert len({p["color"] for p in result["phases"]})==3

def test_all_methods_classified_once_without_changing_scholarly_family_memberships():
    base=build_v06()
    result=_data()
    assert len(result["methods"])==len(base["methods"])==61
    assert {m["id"] for m in result["methods"]}=={m["id"] for m in base["methods"]}
    pino=next(m for m in result["methods"] if m["id"]=="method.pino")
    assert len(pino["families"])>=2
    assert pino["paradigm"]=="hybrid"

def test_lineage_color_uses_three_phase_targets_but_original_stage_evidence_remains():
    result=_data()
    idx={e["id"]:e for e in result["method_edges"]}
    assert idx["relation.pino--extends--fno"]["primary_phase"]=="modeling"
    assert idx["relation.levenberg-marquardt--extends--gauss-newton"]["primary_phase"]=="inference"
    assert idx["relation.method-dreamer-latent-imagination--extends--method-planet-latent-planning"]["primary_phase"]=="twin"
    colors={p["id"]:p["color"] for p in result["phases"]}
    for e in result["method_edges"]:
        if e["type"] in {"extends","combines"} and e["primary_phase"]:
            assert e["color"]==colors[e["primary_phase"]]
            assert e["evidence"] and e["bottleneck"]["zh"]
        if e["type"]=="specializes":
            assert e["color"]=="#9AA8B9"

def test_stage_to_method_mapping_preserves_direct_vs_inherited():
    result=_data()
    roles=result["phase_roles"]["inference"]
    direct=roles["method.diffusion-posterior-sampling"]
    assert any(r["level"]=="direct" and r["evidence"] for r in direct)
    assert any(r["level"] in {"family","ancestor_family"} for r in roles["method.fno"])
    assert not any(r["level"]=="direct" for r in roles["method.fno"])
    assert roles["method.levenberg-marquardt"]

def test_combined_structural_edges_are_dag_and_no_fabricated_connectors():
    result=_data()
    structural=[e for e in result["method_edges"] if e["type"] in LAYOUT_TYPES]
    _check_acyclic([m["id"] for m in result["methods"]],structural)
    assert len(structural)>=30
    assert all(e["type"] in LAYOUT_TYPES for e in structural)
    assert len(result["method_edges"])==43

def test_parenthesized_acronyms_remain_intact_when_wrapping():
    from scripts.build_v07 import _wrap_label
    label = _wrap_label("物理信息神经算子（PINO）")
    assert "（PINO）" in label
    assert "PINO\n" not in label


def test_graphviz_layout_contains_all_clickable_unique_methods_and_evolution_edges():
    result=_data()
    svg=build_svg(result)
    assert svg.startswith("<svg")
    assert len(re.findall(r'data-method-id="method\.',svg))==61
    assert 'data-edge-id="relation.pino--extends--fno"' in svg
    assert 'data-edge-id="relation.levenberg-marquardt--extends--gauss-newton"' in svg
    assert 'class="atlas-dag"' in svg
    assert 'fillcolor' not in svg or svg.count("class=\"node atlas-node\"")>=61

def test_export_deterministic_and_json_serializable():
    first=_data()
    assert first==_data()
    assert json.loads(json.dumps(first,ensure_ascii=False))==first
