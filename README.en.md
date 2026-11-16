# Physics AI Methods Atlas · 物理 AI 方法知识图谱

**[简体中文（default）](README.md) | [English](README.en.md)**

> A research-workflow-centered, evidence-linked **method genealogy knowledge graph** for ODE/PDE inverse problems, scientific ML, coronary hemodynamics, patient-specific digital twins and intervention planning.

The goal is to understand **which capabilities the research workflow needs, what each method contributes, how successors differ from predecessors, and which sources are worth reading first**, not to consume every paper.

## One research axis, reusable method families

The shared research workflow contains six stages:

1. Physical representation and forward modeling
2. Observation and measurement modeling
3. Individualized inversion and state estimation
4. Trustworthy prediction and uncertainty propagation
5. Counterfactual intervention and decision planning
6. Continual assimilation and model updating

Physical and observation models both feed inversion. New measurements can update modeling, inference, and prediction. The axis represents **functional dependencies**, not a rigid temporal recipe.

Research stages point to **method families or methods** through directed links explaining the functional role. An operator-learning family can support forward solutions, inversion as a surrogate, and prediction without being duplicated under three stages.

Method families contain taxonomic and method-evolution DAGs: `specializes` means classification, `extends` an evidence-backed modification, `combines` a documented fusion, and `depends_on` a learning prerequisite. Evolution links record the **technical change, target bottleneck, tradeoffs, supporting paper, and affected research stages**. The primary affected stage supplies the link color; secondary stages remain recorded.

Physical consistency, identifiability, numerical/model error, uncertainty calibration, and generalization are explicit cross-cutting concerns.

## v0.3 scope

- **6 workflow stages**, **20 method families/subfamilies**, **5 cross-cutting concerns**.
- Preserves **30 existing methods**, **32 paper/chapter records**, **8 books**, and **10 research problems** without duplicating source records.
- All **10 previously recorded extends/combines links** now explain their targeted bottlenecks and stage-color mappings.
- Unpopulated major branches — generative modeling, classical numerical schemes, differentiable simulation and decision/control — are marked **planned**, not presented as already verified literature.

## Navigate

- [Unified graph architecture (English)](docs/en/UNIFIED_GRAPH.md)
- [中文架构说明](docs/zh/UNIFIED_GRAPH.md)
- [Method catalogue](docs/METHOD_CATALOG.md)
- [Minimal reading guide](docs/READING_GUIDE.md)
- [Project roadmap](docs/ROADMAP.md)

**Landmark** is contextual to a publication's contribution to a method. **Start Here** is optional reading guidance with no mandatory paper quota. Scientific facts have one canonical source; translations are display layers, not separate databases.

## Validate and export (Python 3.11+)

```bash
python -m pip install -r requirements-dev.txt
python -m scripts.validate
python -m pytest -q
python -m scripts.export_unified --lang zh --output build/unified-zh.json
python -m scripts.export_unified --lang en --output build/unified-en.json
```

Canonical records live in `data/{stages,families,methods,relations,concerns,papers,books,problems,areas}/`. The bilingual, graph-ready projection is produced by `scripts/export_unified.py`. Full interactive GitHub Pages visualization is planned after the method genealogy and literature are curated.
