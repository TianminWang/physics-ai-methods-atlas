"""Regression checks for the v0.4 scholarly method/lineage expansion."""
from __future__ import annotations

from pathlib import Path

from scripts.validate import ROOT, load_catalog, validate_catalog
from scripts.export_unified import export_unified


def test_new_methods_are_unique_and_indexed():
    records, errors = load_catalog()
    assert errors == []
    methods = {k: r for k, r in records.items() if k.startswith("method.")}
    assert len(methods) >= 61
    assert all(r["name"] and r.get("summary") for r in methods.values())
    assert len([k for k in methods if k in {n["id"] for n in export_unified()["nodes"]}]) == len(methods)


def test_all_new_landmark_sources_are_linked_to_methods():
    records, _ = load_catalog()
    selected = [
        "goodfellow-2014-gan",
        "kingma-2014-vae",
        "chung-2023-dps",
        "bastek-2025-physics-diffusion",
        "li-2020-mgno",
        "hafner-2019-planet",
        "hafner-2020-dreamer",
        "kennedy-2001-model-discrepancy",
    ]
    for suffix in selected:
        pid = f"paper.{suffix}"
        assert records[pid]["verification_status"] == "verified"
        assert any(
            r.get("source_id") == pid and r.get("target_id", "").startswith("method.")
            and r.get("type") in {"introduces", "analyzes", "applies", "surveys", "compares"}
            for k, r in records.items() if k.startswith("relation.")
        )


def test_generative_inverse_and_physics_constraints_keep_distinct_stage_targets():
    records, _ = load_catalog()
    dps = records["relation.method-diffusion-posterior-sampling--extends--method-score-based-sde"]
    pid = records["relation.method-physics-informed-diffusion--extends--method-diffusion-probabilistic-model"]
    assert dps["primary_stage_id"] == "stage.inverse-calibration"
    assert pid["primary_stage_id"] == "stage.physics-forward"
    assert dps["evidence_paper_ids"] == ["paper.chung-2023-dps"]
    assert pid["evidence_paper_ids"] == ["paper.bastek-2025-physics-diffusion"]
    assert "bottleneck_zh" in dps and "bottleneck_zh" in pid


def test_numerical_methods_are_not_fabricated_as_a_single_history():
    records, _ = load_catalog()
    methods = {"method.finite-difference", "method.finite-volume", "method.finite-element"}
    for k, r in records.items():
        if k.startswith("relation.") and r.get("type") in {"extends", "combines"}:
            assert not (r.get("source_id") in methods and r.get("target_id") in methods)


def test_reference_first_policy_is_still_advisory():
    records, _ = load_catalog()
    # A classic numerical method can start with a monograph, rather than a paper.
    fvm = records["method.finite-volume"]
    assert fvm["start_here"][0]["reference_id"] == "book.leveque-finite-volume"
    assert not any("curated methods require" in message for message in validate_catalog())


def test_world_model_to_medical_intervention_remains_a_hypothesis():
    records, _ = load_catalog()
    cql = records["relation.method-conservative-q-learning--addresses--problem-virtual-pci-counterfactual"]
    assert "potential" in cql["claim"].lower()
    assert "not established" in cql["claim"].lower() or "not" in cql["claim"].lower()
    dreamer = records["relation.method-dreamer-latent-imagination--extends--method-planet-latent-planning"]
    assert dreamer["primary_stage_id"] == "stage.intervention-planning"


def test_new_task_and_family_projections_share_single_source():
    records, _ = load_catalog()
    assert "family.generative-inverse" in records
    assert "problem.generative-pde-inference" in records
    zh = export_unified(lang="zh")
    en = export_unified(lang="en")
    assert len(zh["nodes"]) == len(en["nodes"])
    assert len(zh["edges"]) == len(en["edges"])
    assert next(n for n in zh["nodes"] if n["id"] == "method.diffusion-posterior-sampling")["label"] == "扩散后验采样（DPS）"
