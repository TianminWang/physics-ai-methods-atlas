"""Validate JSON Schemas, cross-references, reading policy, and graph semantics.

Run: python -m scripts.validate
Dependencies: python -m pip install -r requirements-dev.txt
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
COLLECTIONS = {
    "areas": "area",
    "methods": "method",
    "problems": "problem",
    "papers": "paper",
    "books": "book",
    "relations": "relation",
}
RELATION_PAIRS = {
    "belongs_to": {("method", "area")},
    "subarea_of": {("area", "area")},
    "specializes": {("method", "method")},
    "extends": {("method", "method")},
    "combines": {("method", "method")},
    "depends_on": {("method", "method")},
    "contrasts_with": {("method", "method")},
    "addresses": {("method", "problem")},
    "introduces": {("paper", "method")},
    "analyzes": {("paper", "method")},
    "applies": {("paper", "method")},
    "surveys": {("paper", "method")},
    "compares": {("paper", "method")},
    "covers": {("book", "method"), ("book", "area"), ("book", "problem")},
}
PAPER_RELATIONS = {"introduces", "analyzes", "applies", "surveys", "compares"}
DAG_GROUPS = {
    "area taxonomy": {"subarea_of"},
    "method taxonomy": {"specializes"},
    "method evolution": {"extends", "combines"},
    "learning prerequisites": {"depends_on"},
}


def _kind(entity_id: str) -> str:
    return entity_id.split(".", 1)[0]


def _cycles(edges: list[tuple[str, str]]) -> list[list[str]]:
    """Find one representative cycle from each DFS-discovered back edge."""
    graph: dict[str, list[str]] = defaultdict(list)
    for source, target in edges:
        graph[source].append(target)
    state: dict[str, int] = {}
    stack: list[str] = []
    found: list[list[str]] = []

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for neighbor in graph.get(node, []):
            if state.get(neighbor, 0) == 0:
                visit(neighbor)
            elif state.get(neighbor) == 1:
                found.append(stack[stack.index(neighbor):] + [neighbor])
        stack.pop()
        state[node] = 2

    for node in sorted(graph):
        if not state.get(node, 0):
            visit(node)
    return found


def load_catalog(root: Path = ROOT) -> tuple[dict[str, dict], list[str]]:
    """Load repository records; return {id: record} and human-readable errors."""
    errors: list[str] = []
    records: dict[str, dict] = {}
    schema_path = root / "schemas" / "atlas.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, ValueError, Exception) as exc:
        # A schema failure prevents every subsequent structural check.
        return {}, [f"{schema_path}: invalid schema: {exc}"]

    for collection, kind in COLLECTIONS.items():
        validator = Draft202012Validator(
            schema["$defs"][kind], format_checker=FormatChecker()
        )
        directory = root / "data" / collection
        if not directory.is_dir():
            errors.append(f"{directory}: missing collection directory")
            continue
        for path in sorted(directory.glob("*.json")):
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{path}: invalid JSON: {exc}")
                continue
            for err in sorted(validator.iter_errors(record), key=lambda e: str(e.path)):
                location = ".".join(map(str, err.absolute_path)) or "(root)"
                errors.append(f"{path}: {location}: {err.message}")
            if not isinstance(record, dict):
                continue
            entity_id = record.get("id")
            if not isinstance(entity_id, str):
                continue
            expected = f"{kind}.{path.stem}"
            if entity_id != expected:
                errors.append(f"{path}: id must be '{expected}', got '{entity_id}'")
            if entity_id in records:
                errors.append(f"{path}: duplicate id '{entity_id}'")
            else:
                records[entity_id] = record
    return records, errors


def validate_catalog(root: Path = ROOT) -> list[str]:
    """Run all validation rules, including typed relations and reading policy."""
    records, errors = load_catalog(root)
    if not records:
        return errors or ["No catalog data found."]
    relations = {
        k: r for k, r in records.items() if _kind(k) == "relation"
    }
    methods = {
        k: r for k, r in records.items() if _kind(k) == "method"
    }
    papers = {
        k: r for k, r in records.items() if _kind(k) == "paper"
    }
    edge_signatures: set[tuple[str, str, str]] = set()
    paper_method_links: set[tuple[str, str]] = set()
    method_areas: set[str] = set()

    for rel_id, rel in relations.items():
        source, target, predicate = (
            rel.get("source_id"), rel.get("target_id"), rel.get("type")
        )
        if not all(isinstance(v, str) for v in (source, target, predicate)):
            continue
        for name, endpoint in (("source", source), ("target", target)):
            if endpoint not in records:
                errors.append(f"{rel_id}: {name} endpoint '{endpoint}' does not exist")
        if source == target:
            errors.append(f"{rel_id}: self-relations are not allowed")
        if (_kind(source), _kind(target)) not in RELATION_PAIRS.get(predicate, set()):
            errors.append(
                f"{rel_id}: invalid source/target types for '{predicate}'"
            )
        signature = source, predicate, target
        if signature in edge_signatures:
            errors.append(f"{rel_id}: duplicated relation triple {signature}")
        edge_signatures.add(signature)
        if predicate in PAPER_RELATIONS:
            paper_method_links.add((source, target))
        if predicate == "belongs_to" and _kind(source) == "method":
            method_areas.add(source)
        evidence = rel.get("evidence_paper_ids", [])
        if isinstance(evidence, list):
            for paper_id in evidence:
                if paper_id not in papers:
                    errors.append(f"{rel_id}: missing evidence paper '{paper_id}'")
            if predicate in {"extends", "combines"} and not evidence:
                errors.append(
                    f"{rel_id}: method-lineage claim requires evidence_paper_ids"
                )

    for method_id, method in methods.items():
        if method_id not in method_areas:
            errors.append(f"{method_id}: missing 'belongs_to' area relation")
        core = method.get("core_reading", [])
        if not isinstance(core, list):
            continue
        if method.get("status") == "curated" and not 1 <= len(core) <= 2:
            errors.append(f"{method_id}: curated methods require 1–2 must-read papers")
        seen: set[str] = set()
        for entry in core:
            if not isinstance(entry, dict):
                continue
            paper_id = entry.get("paper_id")
            if not isinstance(paper_id, str):
                continue
            if paper_id in seen:
                errors.append(f"{method_id}: repeated must-read paper '{paper_id}'")
            seen.add(paper_id)
            paper = papers.get(paper_id)
            if paper is None:
                errors.append(f"{method_id}: must-read paper '{paper_id}' is missing")
                continue
            if (paper_id, method_id) not in paper_method_links:
                errors.append(
                    f"{method_id}: must-read '{paper_id}' needs a paper→method relation"
                )
            if method.get("status") == "curated":
                if paper.get("verification_status") != "verified":
                    errors.append(
                        f"{method_id}: must-read '{paper_id}' is not verified"
                    )
                if (
                    paper.get("publication_status") != "peer_reviewed"
                    and not entry.get("exception_reason")
                ):
                    errors.append(
                        f"{method_id}: must-read '{paper_id}' needs a documented "
                        "preprint/unknown-publication exception"
                    )

    for paper_id in papers:
        if not any(source == paper_id for source, _ in paper_method_links):
            errors.append(f"{paper_id}: paper must link to at least one method")
    for field in ("doi", "arxiv"):
        identifiers: dict[str, str] = {}
        for paper_id, paper in papers.items():
            value = paper.get("identifiers", {}).get(field)
            if not isinstance(value, str):
                continue
            normalized = value.lower().strip()
            if field == "doi":
                normalized = normalized.removeprefix("https://doi.org/")
            else:
                normalized = re.sub(r"v\d+$", "", normalized)
            if normalized in identifiers:
                errors.append(
                    f"{paper_id}: duplicate {field} '{value}' also used by "
                    f"{identifiers[normalized]}"
                )
            identifiers[normalized] = paper_id

    for group, predicates in DAG_GROUPS.items():
        directed_edges = [
            (rel["source_id"], rel["target_id"])
            for rel in relations.values()
            if rel.get("type") in predicates
            and isinstance(rel.get("source_id"), str)
            and isinstance(rel.get("target_id"), str)
        ]
        for cycle in _cycles(directed_edges):
            errors.append(f"{group}: cycle detected: {' -> '.join(cycle)}")
    return sorted(set(errors))


def main() -> int:
    problems = validate_catalog()
    if problems:
        print(f"Atlas validation FAILED ({len(problems)} issue(s)):")
        for error in problems:
            print(f"  - {error}")
        return 1
    records, _ = load_catalog()
    kinds = defaultdict(int)
    for key in records:
        kinds[_kind(key)] += 1
    print(
        "Atlas validation OK: "
        + ", ".join(f"{kind}={kinds[kind]}" for kind in sorted(kinds))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
