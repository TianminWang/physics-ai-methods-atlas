"""v0.9 audit: taxonomy and capability proposals must remain faithful to source data."""
from __future__ import annotations

import json
from pathlib import Path

from scripts.audit_v09 import ROOT, audit


def test_audit_preserves_existing_source_record_counts():
    result=audit()
    inventory=result["inventory"]
    assert inventory["entities"]["method"] == 61
    assert inventory["entities"]["family"] == 34
    assert inventory["entities"]["problem"] == 15
    assert inventory["entities"]["paper"] == 58
    assert inventory["entities"]["book"] == 12
    assert inventory["total_relations"] == 530


def test_evolution_is_distinct_from_taxonomy_and_application():
    inventory=audit()["inventory"]
    assert inventory["evolution_links"] == 16
    assert inventory["relation_types"]["specializes"] == 16
    assert inventory["stage_functional_links"] == 55
    assert inventory["problem_method_links"] == 93
    assert inventory["methods_in_evolution"] == 24
    assert len(inventory["methods_without_evolution"]) == 37


def test_six_existing_family_roots_and_nonexclusive_memberships_are_preserved():
    inventory=audit()["inventory"]
    assert len(inventory["family_taxonomy_roots"]) == 6
    assert inventory["family_memberships"] == 67
    assert len(inventory["methods_with_multiple_families"]) == 6
    assert inventory["methods_without_family"] == []


def test_problem_scenarios_are_separate_from_reusable_capabilities():
    result=audit()
    assert len(result["inventory"]["method_problem_coverage"]) == 15
    assert all(n>0 for n in result["inventory"]["method_problem_coverage"].values())
    assert result["ontology"]["capabilities_proposed"] == 19
    assert result["ontology"]["capabilities_by_phase"] == {
        "inference":8,"modeling":6,"twin":5
    }


def test_proposed_node_roles_include_different_levels():
    proposed=json.loads(
        (ROOT/"audits"/"v09"/"method-kind-proposals.json").read_text(encoding="utf-8")
    )["method_kinds"]
    assert proposed["method.bayesian-inverse-problems"]["primary_kind"] == "problem_formulation"
    assert proposed["method.markov-chain-monte-carlo"]["primary_kind"] == "method_family"
    assert proposed["method.no-u-turn-sampler"]["primary_kind"] == "algorithm"
    assert proposed["method.difftaichi"]["primary_kind"] == "software_framework"
    assert proposed["method.windkessel"]["primary_kind"] == "physical_model"
    assert proposed["method.fno"]["primary_kind"] == "model_architecture"


def test_relation_review_queue_does_not_change_scholarly_data():
    q=json.loads(
        (ROOT/"audits"/"v09"/"relation-review-queue.json").read_text(encoding="utf-8")
    )
    assert q["status"]=="NOT_VERIFIED_NO_CANONICAL_RELATION_MUTATION"
    assert len(q["candidates"]) == 10
    assert len({item["id"] for item in q["candidates"]}) == 10
    assert any("flow-matching" in item["id"] for item in q["candidates"])


def test_audit_is_deterministic_and_json_serializable():
    result=audit()
    assert audit()==result
    assert json.loads(json.dumps(result,ensure_ascii=False))==result
