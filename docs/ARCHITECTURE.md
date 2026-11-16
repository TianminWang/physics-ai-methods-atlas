# Architecture · Unified workflow axis and method DAG

**Current design specification:** [English](en/UNIFIED_GRAPH.md) · [中文版](zh/UNIFIED_GRAPH.md)

This document is a short entry point; the bilingual specification above is authoritative for v0.3.

## One knowledge graph, one workflow axis, reusable methods

- **Workflow stages** (`stage.*`) describe the scientific loop from physical/measurement models to inverse calibration, trustworthy prediction, intervention planning, and continual assimilation.
- **Method families** (`family.*`) exist independently of the workflow axis and can form a classification DAG. Each method (`method.*`) is stored **once**, though it can connect to several families and serve several workflow stages.
- **Functional links** (`stage → family/method`, `uses_method`) state what a technique does in that scientific stage; they do **not** claim historical descent.
- **Method genealogy** uses distinct `specializes`, `extends`, `combines`, `contrasts_with`, `depends_on` relations; only evidence-backed `extends/combines` describe methodological changes.
- **Evolution link annotations** explain innovation, targeted bottleneck, tradeoffs, evidence, affected stages, and optional primary-stage coloring.
- **Concerns** (`concern.*`) apply across stages, for physical validity, identifiability, numerical/model error, uncertainty calibration and external generalization.

The scientific workflow may have feedback loops; method-genealogy and family taxonomic DAGs are checked for cycles. This is essential to avoid treating stage-to-method application relationships as methodological ancestry.

## Source data and projections

Canonical JSON records live in `data/`. Backward-compatible schema versions `2.0.0` and `2.1.0` coexist, without duplicating or re-ID-ing the original bibliographic resources. Chinese display names are provided through bilingual fields and a translation-only locale overlay for legacy method labels. Scientific facts and method evidence remain one source of truth.

- `python -m scripts.validate` — schema, cross-reference, DAG and metadata validation.
- `python -m scripts.export_graph` — full canonical node/edge data, including papers/books/problems.
- `python -m scripts.export_unified --lang zh` — render-ready bilingual workflow + family + method projection with styling semantics.

The interactive visual frontend belongs to a later release. No historical/cross-domain link automatically establishes method superiority or coronary-specific clinical effectiveness.
