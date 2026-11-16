# Architecture · 知识图谱数据与演化关系

## Three layers from one source of truth

1. **Canonical records:** individual JSON files in `data/areas`, `methods`, `papers`, `books`, `problems`, `relations`.
2. **Validation/projections:** JSON Schema draft 2020-12 and cross-file semantic validator; `scripts/export_graph.py` produces a normalized graph JSON.
3. **Views:** simplified README, future default **method-evolution forest A**, switchable coronary/digital-twin **research-problem view B**, optional **learning dependencies C**.

All views use the **same authoritative records**. Never maintain three independent knowledge maps.

## Entity types and identifiers

| Entity | Identifier | What it represents |
|---|---|---|
| area | `area.inverse-problems` | Scope/navigation category, **not** a historical ancestor |
| method | `method.fno` | Reusable method, algorithm or distinct framework |
| paper | `paper.li-2024-pino` | One verified scholarly reference; reuse across nodes |
| book | `book.chavent-nonlinear-least-squares` | Monograph or textbook with broad chapter coverage |
| problem | `problem.coronary-parameter-inference` | Concrete scientific/research task with unknowns and measurements |
| relation | `relation.pino--extends--fno` | Directed, typed and optionally evidence-backed link |

v0.2 uses `schema_version: "2.0.0"` on all records; a major-version bump was required to replace the first-stage `core_reading` field with `start_here` and to **remove the global paper Landmark flag**. The ID suffix must match the JSON filename, and stable IDs must be reused, not duplicated.

Methods contain `summary`, `core_idea`, `innovation`, optional `limitations`, `background_topics`, editorial `status`, optional `curation_note`, and optional ordered `start_here`. Bibliographic metadata lives only in paper/book records.

## Edge semantics (direction matters)

| Relation | Allowed direction | Meaning |
|---|---|---|
| `belongs_to` | method→area | Navigation membership, many allowed |
| `subarea_of` | area→area | Scope category hierarchy |
| `specializes` | specific method→general method | Method taxonomy; **not necessarily newer** |
| `extends` | later/new approach→method predecessor | Evidence-backed modification to a method |
| `combines` | composite method→component method | Evidence-backed methodological fusion |
| `depends_on` | method→method | Pedagogical prerequisite, **not** historical influence |
| `contrasts_with` | method→method | Important alternative with a different trade-off |
| `addresses` | method→problem | Can support an application under stated conditions |
| `introduces`, `analyzes`, `applies`, `surveys`, `compares` | paper→method | Role of a paper **relative to that method** |
| `covers` | book→method/area/problem | Educational coverage, optionally localized to chapter |

All relation records have a human-readable `claim`. `extends` and `combines` require `evidence_paper_ids`, allowing a reviewer to inspect an actual claimed methodological lineage. A paper→method role may also record `significance` and must give `significance_reason` for `landmark`.

**Important:** The entire graph may have cycles; the semantic projections `subarea_of`, `specializes`, (`extends` + `combines`), and `depends_on` must each be acyclic. Multiple parents are natural. The viewer must distinguish taxonomy and historical evolution from pedagogical prerequisites and clinical applicability.

## Start-here references are intentionally non-normative

~~~json
{
  "id": "method.fno",
  "start_here": [
    {
      "reference_id": "paper.li-2021-fno",
      "why": "Original Fourier neural-operator architecture",
      "focus": "Fourier layers and parametric PDE examples"
    }
  ]
}
~~~

The excerpt is illustrative, not a complete method record. `start_here` may be absent or have any number of entries. Most curated nodes suggest around 1–2 sources for convenience, not because a numerical requirement exists.

Books can appear directly in `start_here` and do **not** count as landmark papers. A new journal study can attach to several methods without creating a method node or expanding every reading list.

## Engineering and scientific responsibilities

- JSON Schema: field validity and `schema_version`.
- Semantic validator: ID uniqueness, typed relation endpoints, bibliographic identifier duplicates, reference and evidence integrity, contextual landmark requirements, recommended paper/book verification, acyclic views.
- Exporter: deterministic nodes+edges, refusing invalid input. `build/` is derived and ignored.
- Reader/frontend (Phase 3): displays methods in a forest by default, with cross-links, scholarly role, Landmark significance, optional `start_here`, and contrasting problem-oriented view.
- Scholar/curator: verifies publications against authoritative sources and checks whether a paper **really** proposes, extends, tests, or merely discusses a method.

**No arbitrary rule that newer = better; no inference that 1D systemic vascular validation proves 1D coronary clinical validation.** Problem examples describe applicability subject to evidence, not clinical guarantees.

## Near-term research scope

Traditional nonlinear least squares and adjoint optimization, stability/regularization, Bayesian inverse inference and ensemble/state assimilation belong on the **same** methodological map as PINNs, neural operators, derivative-informed surrogates and direct inverse networks. Vascular Windkessel and structured trees are physical boundary-model methods. Coronary FFR and virtual PCI are **problems/application slots**, not generic mathematical ancestor nodes.
