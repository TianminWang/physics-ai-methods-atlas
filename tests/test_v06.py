"""v0.6 unified graph: provenance, functional mapping, DAGs and nonexclusive taxonomy."""
from __future__ import annotations
import json
from pathlib import Path
from scripts.build_v06 import ROOT, build_graph
from scripts.validate import load_catalog

def test_unique_global_methods_and_all_six_stages():
    result=build_graph()
    records,_=load_catalog()
    methods={k for k in records if k.startswith("method.")}
    assert set(n["id"] for n in result["methods"])==methods
    assert len(result["methods"])==len(methods)
    assert len(result["stages"])==6

def test_all_methods_have_one_visual_placement_but_keep_multiple_families():
    result=build_graph()
    ids=[i for z in result["zones"] for i in z["method_ids"]]
    assert len(ids)==len(set(ids))==len(result["methods"])
    pino=next(n for n in result["methods"] if n["id"]=="method.pino")
    assert len(pino["families"])>1

def test_stage_map_expands_family_roles_without_fake_direct_evidence():
    result=build_graph()
    inv=result["stage_roles"]["stage.inverse-calibration"]
    assert inv
    direct=inv["method.diffusion-posterior-sampling"]
    assert any(x["level"]=="direct" and x["evidence"] for x in direct)
    fno=inv["method.fno"]
    assert any(x["level"] in ("family","ancestor_family") for x in fno)
    assert all(x["level"]!="direct" or x["via_family_id"] is None for x in fno)
    assert any(x["via_family_id"] for x in fno if x["level"]!="direct")

def test_no_stage_subset_is_required_to_be_connected():
    result=build_graph()
    focus=set(result["stage_roles"]["stage.inverse-calibration"])
    edges=[e for e in result["method_edges"] if e["type"] in ("extends","combines")
           and e["source"] in focus and e["target"] in focus]
    # Unconnected pieces are valid; no artificial lineage edges link
    # Gaussian optimization directly to score-based posterior samplers.
    assert "method.levenberg-marquardt" in focus
    assert "method.diffusion-posterior-sampling" in focus
    assert not any({e["source"],e["target"]}==
                   {"method.levenberg-marquardt","method.diffusion-posterior-sampling"}
                   for e in edges)

def test_lineage_colors_and_links_are_extracted_not_inferred_from_location():
    result=build_graph()
    palette={s["id"]:s["color"] for s in result["stages"]}
    evo=next(e for e in result["method_edges"] if e["id"]=="relation.pino--extends--fno")
    assert evo["source"]=="method.fno" and evo["target"]=="method.pino"
    assert evo["color"]==palette[evo["primary_stage"]]
    assert evo["bottleneck"]["zh"]
    assert evo["evidence"][0]["id"]=="paper.li-2024-pino"

def test_method_citation_and_reading_are_optional_and_preserved():
    result=build_graph()
    for node in result["methods"]:
        for reference in node["readings"]:
            assert reference["id"].startswith(("paper.","book."))
            assert reference["url"].startswith("https://")
    fno=next(n for n in result["methods"] if n["id"]=="method.fno")
    assert any(s["landmark"] for s in fno["sources"])

def test_deterministic_bilingual_json_data():
    first=build_graph()
    assert first==build_graph()
    assert json.loads(json.dumps(first,ensure_ascii=False))==first
    assert next(n for n in first["methods"] if n["id"]=="method.fno")["label"]["zh"]=="傅里叶神经算子（FNO）"
    assert first["summary"]["functional_edges"]>=50
    assert first["summary"]["methods"]>=61
