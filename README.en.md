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

## v0.4 scope — first literature-backed expansion

| Component | Current records |
|---|---:|
| Workflow stages / cross-cutting concerns | 6 / 5 |
| Method families / methods | **34 / 61** |
| Scholarly papers / monographs | **58 / 12** |
| Research problems / typed links | **15 / 530** |

The expansion adds 31 distinct reusable method nodes across **finite differences/volumes/elements and ODE integrators**, identifiability and Bayesian computation (MCMC/NUTS, VI, SBI), **generative modeling and inverse diffusion**, graph/attention operator architectures, differentiable physical simulation, and latent world models and planning (PlaNet/Dreamer/MPC/MBPO/offline RL). Landmark roles are contextual and linked to source papers; starting reading references remain optional.

**Evidence scope:** virtual coronary intervention planning is a research application hypothesis, not clinically established by general world-model or offline-RL papers. The atlas is a curated foundation, not a completed scientific encyclopedia.

## v0.6 unified method graph prototype (new)

[How to review v0.6](viewer-v06/README.md) · [Viewer source](viewer-v06/index.html)

The new prototype removes v0.5's separate method genealogy tabs. **All 61 methods live on one shared graph**; workflow stages now explicitly map to families or specific methods through documented functional-role edges.

Selecting a workflow stage highlights directly linked methods and method-family derived candidates at different strengths, while other methods remain visible but muted. Six visual zones aid navigation without imposing a unique scholarly parent.

Download the **atlas-unified-v06** offline HTML from [GitHub Actions](https://github.com/TianminWang/physics-ai-methods-atlas/actions/workflows/validate.yml), unzip, and open `index.html`. This is a reviewable prototype, not yet the complete deployed GitHub Pages experience.

## v0.5 interactive layout prototype (historical)

A working three-branch layout is available for classical inversion, neural operators and generative inverse problems. The preview derives from the canonical Atlas and includes stage/family roles, evidence-backed method evolution, compact/full node disclosure, citation panels, bilingual switching, searching and mobile navigation.

[Prototype instructions](prototype/README.md) · [Offline HTML artifact from the latest successful validation](https://github.com/TianminWang/physics-ai-methods-atlas/actions/workflows/validate.yml) · [Browser screenshots](https://github.com/TianminWang/physics-ai-methods-atlas/actions/workflows/prototype-ui.yml).

This is a focused validation release, not the deployed full GitHub Pages experience. Full progressive-disclosure browsing follows prototype approval.

## Navigate

- [Unified graph architecture (English)](docs/en/UNIFIED_GRAPH.md)
- [中文架构说明](docs/zh/UNIFIED_GRAPH.md)
- [v0.4 method genealogy and verified reading tracks](docs/en/METHOD_GENEALOGY_V04.md)
- [Historical first-30-method index](docs/METHOD_CATALOG.md)
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
