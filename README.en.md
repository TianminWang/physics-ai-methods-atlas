# Physics AI Methods Atlas · 物理 AI 方法知识图谱

**[简体中文（default）](README.md) | [English](README.en.md)**

> A growing, evidence-linked knowledge graph of **ODE/PDE inverse problems, scientific ML, neural operators, coronary hemodynamics, personalized digital twins and world models**.

The current design is **one three-phase research axis plus one global method-evolution DAG**. The research axis describes scientific capabilities; the DAG describes documented technical development and its targeted bottlenecks.

## Three research phases

| Phase | Main question | Child capabilities |
|---|---|---|
| **I. Physical modeling & forward problems** | How do physical laws, parameters and conditions produce states and measurements? | Governing and forward models; observations and data acquisition |
| **II. Inverse problems & inference** | What unknown information can be recovered from sparse noisy observations? | Parameter inference, state estimation, regularization and identifiability |
| **III. Personalized prediction, intervention & updating** | How can individualized models forecast, evaluate interventions and update from new data? | Prediction, counterfactual decision-making, continual assimilation |

Digital twins and world models are relevant system-level directions, not synonyms for the entire third phase. Physical validity, uncertainty, model error and generalization are cross-cutting concerns. Feedback may revise both inference and forward models.

## A relationship-ranked global method graph

The viewer no longer forces methods into six category rectangles. **Graphviz ranks every indexed method from actual `extends`, `combines` and neutral `specializes` relations.** Disconnected components are legitimate; no artificial scholarly genealogy is added.

**Node color = technical paradigm:** classical numerics/optimization, statistical/probabilistic, machine/deep learning, or physics–data hybrid. The color is a primary visual tag, not a unique scholarly parent; nonexclusive method-family memberships remain intact.

**Directed edge color = target research phase:** I blue, II purple, III teal, or neutral when unresolved. Extensions and combinations have different line patterns. Taxonomic and comparison links cannot be mistaken for demonstrated improvements.

Nodes and SVG links are equally selectable. Their details show mechanisms, original method-family memberships, actual bottlenecks, trade-offs, source papers, contextual Landmark roles and optional Start Here readings. Stage-to-family relevance remains distinct from method-specific empirical evidence.

## v0.7 interactive prototype

[Design specification](docs/en/THREE_PHASE_DAG_V07.md) · [中文说明](docs/zh/THREE_PHASE_DAG_V07.md)

From [GitHub Actions → latest successful Validate atlas data → Artifacts](https://github.com/TianminWang/physics-ai-methods-atlas/actions/workflows/validate.yml), download `atlas-global-dag-v07`, unzip it and open `index.html`. You do not need Graphviz or a web server to view the generated artifact.

This is an **offline testable prototype**, not yet the final GitHub Pages deployment.

## Indexed academic content and reading strategy

Current Atlas: approximately **61 methods, 34 families, 58 paper records, 12 books and 15 scientific problems**, plus typed relationships. The method map is not claimed exhaustive.

- [Method genealogy v0.4 (English)](docs/en/METHOD_GENEALOGY_V04.md)
- [Minimal reading guide](docs/READING_GUIDE.md)
- [Project roadmap](docs/ROADMAP.md)

Landmark significance is contextual to a paper's contribution to a specific method. **Start Here is optional** and has no compulsory paper quota.

## Development

Canonical scholarship lives in `data/`; presentation metadata in `config/v07.json`, builder in `scripts/build_v07.py`, and viewer source in `viewer-v07/`.

```bash
python -m pip install -r requirements-dev.txt
python -m scripts.validate
python -m pytest -q
python -m scripts.build_v07 --site build/viewer-v07
```

Graphviz `dot` and a CJK font are needed to **build**, but not to open the generated offline viewer. Historical [v0.6](viewer-v06/README.md) and [v0.5](prototype/README.md) prototypes remain accessible.
