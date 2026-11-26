"""Read-only v0.9 methodological structure audit.

The audit never alters data/*.json, scholarly evidence or the website.
It checks the existing repository, then evaluates separately stored ontology
*proposals* for consistency. A valid schema does NOT certify historical claims.

Usage: python -m scripts.audit_v09 --output build/audit-v09.json
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

from scripts.validate import ROOT, load_catalog, validate_catalog

PROPOSAL_DIR = ROOT / "audits" / "v09"
PAPER_METHOD_ROLES = {"introduces", "analyzes", "applies", "surveys", "compares"}
LINEAGE_ROLES = {"extends", "combines"}


def _load_proposal(name: str, root: Path) -> dict:
    return json.loads((root / "audits" / "v09" / name).read_text(encoding="utf-8"))


def _components(method_ids: set[str], relations: list[dict]) -> list[list[str]]:
    """Weakly connected components formed ONLY by existing evolution edges."""
    adjacent = {key: set() for key in method_ids}
    for r in relations:
        if r["type"] not in LINEAGE_ROLES:
            continue
        a, b = r["source_id"], r["target_id"]
        adjacent[a].add(b)
        adjacent[b].add(a)
    seen = set()
    groups = []
    for start in sorted(method_ids):
        if start in seen:
            continue
        queue = deque([start])
        seen.add(start)
        group = []
        while queue:
            mid = queue.popleft()
            group.append(mid)
            for target in sorted(adjacent[mid]):
                if target not in seen:
                    seen.add(target)
                    queue.append(target)
        groups.append(sorted(group))
    return sorted(groups, key=lambda x: (-len(x), x[0]))


def audit(root: Path = ROOT) -> dict:
    invalid = validate_catalog(root)
    if invalid:
        raise ValueError("Canonical Atlas validation failed:\n"+"\n".join(invalid))

    records, errors = load_catalog(root)
    if errors:
        raise ValueError("Atlas load failed:\n"+"\n".join(errors))
    by_kind = defaultdict(dict)
    for ident, record in records.items():
        by_kind[ident.split(".", 1)[0]][ident] = record
    methods = by_kind["method"]
    families = by_kind["family"]
    problems = by_kind["problem"]
    papers = by_kind["paper"]
    relations = list(by_kind["relation"].values())
    role_counts = Counter(r["type"] for r in relations)

    kinds = _load_proposal("method-kind-proposals.json", root)
    capabilities = _load_proposal("capability-layer-proposal.json", root)
    review = _load_proposal("relation-review-queue.json", root)
    if set(kinds["method_kinds"]) != set(methods):
        raise ValueError("Provisional method-kind roster does not match canonical method IDs")
    for ident, item in kinds["method_kinds"].items():
        if item["primary_kind"] not in kinds["vocabulary"]:
            raise ValueError(f"Unknown proposed kind: {ident} -> {item['primary_kind']}")
    cap_index = {x["id"]: x for x in capabilities["capabilities"]}
    if len(cap_index) != len(capabilities["capabilities"]):
        raise ValueError("Duplicate capability proposal IDs")
    if not all(x["phase"] in {"modeling", "inference", "twin"} for x in cap_index.values()):
        raise ValueError("A capability references an unknown research phase")
    for cap in cap_index.values():
        for mid in cap["illustrative_method_ids"]:
            if mid not in methods:
                raise ValueError(f"{cap['id']} references missing method {mid}")
    if set(capabilities["candidate_problem_capabilities"]) != set(problems):
        raise ValueError("The proposed capability mapping must cover all existing problems")
    for pid, cap_ids in capabilities["candidate_problem_capabilities"].items():
        for cap_id in cap_ids:
            if cap_id not in cap_index:
                raise ValueError(f"{pid} references missing proposal capability {cap_id}")
    for item in review["candidates"]:
        if item["id"] not in by_kind["relation"]:
            raise ValueError(f"Review queue references missing relation {item['id']}")

    family_memberships = defaultdict(list)
    parent_links = defaultdict(list)
    family_direct_members = defaultdict(list)
    problem_methods = defaultdict(list)
    method_problems = defaultdict(list)
    paper_contributions = defaultdict(list)
    book_coverage = defaultdict(list)
    method_stage_roles = defaultdict(list)
    for r in relations:
        typ = r["type"]
        source, target = r["source_id"], r["target_id"]
        if typ == "member_of_family":
            family_memberships[source].append(target)
            family_direct_members[target].append(source)
        elif typ == "subfamily_of":
            parent_links[source].append(target)
        elif typ == "addresses":
            problem_methods[target].append(source)
            method_problems[source].append(target)
        elif typ in PAPER_METHOD_ROLES:
            paper_contributions[target].append(source)
        elif typ == "covers" and target in methods:
            book_coverage[target].append(source)
        elif typ == "uses_method":
            method_stage_roles[source].append(target)

    components = _components(set(methods), relations)
    linked = {
        mid for r in relations if r["type"] in LINEAGE_ROLES
        for mid in (r["source_id"], r["target_id"])
    }
    roots = sorted(fid for fid in families if not parent_links[fid])
    no_direct = sorted(fid for fid in families if not family_direct_members[fid])
    high_review = [r["id"] for r in review["candidates"] if r["priority"]=="high"]
    method_kind_counts = Counter(
        p["primary_kind"] for p in kinds["method_kinds"].values()
    )

    report = {
        "report_version": "v0.9-readonly-audit",
        "based_on_repo": "TianminWang/physics-ai-methods-atlas",
        "source": "Existing canonical data files, no changes to scientific content",
        "ontology": {
            "status": "provisional",
            "method_kind_counts": dict(sorted(method_kind_counts.items())),
            "capabilities_proposed": len(cap_index),
            "capabilities_by_phase": dict(sorted(Counter(
                c["phase"] for c in cap_index.values()
            ).items())),
            "relation_review_candidates": len(review["candidates"]),
            "high_priority_relations": sorted(high_review),
        },
        "inventory": {
            "entities": {k: len(v) for k, v in sorted(by_kind.items())},
            "relation_types": dict(sorted(role_counts.items())),
            "total_relations": len(relations),
            "family_taxonomy_roots": roots,
            "family_taxonomy_edges": role_counts["subfamily_of"],
            "family_memberships": role_counts["member_of_family"],
            "families_without_direct_method_members": no_direct,
            "methods_with_multiple_families": {
                mid: sorted(fids) for mid, fids in sorted(family_memberships.items())
                if len(fids) >= 2
            },
            "methods_without_family": sorted(set(methods)-set(family_memberships)),
            "problem_method_links": role_counts["addresses"],
            "method_problem_coverage": {
                pid: len(problem_methods[pid]) for pid in sorted(problems)
            },
            "methods_without_direct_problem_link": sorted(
                set(methods)-set(method_problems)),
            "methods_without_paper_contribution_link": sorted(
                set(methods)-set(paper_contributions)),
            "methods_without_book_coverage_link": sorted(
                set(methods)-set(book_coverage)),
            "methods_without_start_here": sorted(
                mid for mid, m in methods.items() if not m.get("start_here")),
            "stage_functional_links": role_counts["uses_method"],
            "evolution_links": sum(role_counts[r] for r in LINEAGE_ROLES),
            "methods_in_evolution": len(linked),
            "methods_without_evolution": sorted(set(methods)-linked),
            "evolution_component_count_all_methods": len(components),
            "evolution_component_count_linked": sum(len(c)>1 for c in components),
            "evolution_component_sizes": [len(c) for c in components],
        },
        "diagnosis": [
            "Current method.* entities include mathematical problem formulations, broad method families, algorithms, neural model architectures, physical models, design/diagnostic techniques and software frameworks.",
            "An extends/combines DAG alone cannot serve as a complete methodology taxonomy; disconnected components can be scientifically correct.",
            "Current problem.* entries mix reusable mathematical tasks, hemodynamic application scenarios and longitudinal digital-twin cases. A reusable capability layer should remain distinct.",
            "The user-facing functional mapping may reference a method in the unlinked shelf. This must be navigable, not silently dim the canvas.",
            "A semantic family link does not amount to separately verified evidence of every family member.",
            "Provisional kind and capability mappings are proposals; no academic edge is retyped or fabricated in this audit."
        ],
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT/"build"/"audit-v09.json")
    args = parser.parse_args()
    result = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False)+"\n", encoding="utf-8"
    )
    inv=result["inventory"]
    print(
        "v0.9 audit OK: "
        f"{inv['entities']['method']} methods, "
        f"{inv['entities']['family']} families, "
        f"{inv['entities']['problem']} problems, "
        f"{inv['total_relations']} relations, "
        f"{inv['evolution_links']} evolution edges, "
        f"{inv['methods_in_evolution']} evolution-linked methods; "
        f"{result['ontology']['capabilities_proposed']} proposed capabilities "
        f"(DESIGN ONLY)"
    )
    print("Audit report:", args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
