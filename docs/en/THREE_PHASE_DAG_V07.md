# v0.7 · Three research phases and one global methods DAG

The Atlas represents **two distinct things**: a scientific workflow describing the capabilities needed to solve inverse problems and build individual digital models, and a scholarly method genealogy describing actual changes between algorithms. Functional links connect them, but application relevance never implies historical ancestry.

## Three research phases

| Phase | Existing child capabilities | Meaning |
|---|---|---|
| I. Physical modeling & forward problems | `physics-forward`, `observation` | Physical equations, parameterization, boundary conditions, forward solvers and observation operators |
| II. Inverse problems & inference | `inverse-calibration` | Recover unknown parameters/states from limited noisy observations; regularization and identifiability |
| III. Personalized prediction, intervention & updates | `prediction-uq`, `intervention-planning`, `continual-update` | Forecast under new conditions, model counterfactuals, plan interventions and assimilate later observations |

These are not compulsory sequential execution steps: forward models are repeatedly reused, and updating can trigger new inference and even model revision. Digital twins and world models are relevant system capabilities, not synonyms for every forecasting method. Physical validity, identifiability, numerical/model error, uncertainty calibration and external validation are cross-cutting requirements.

## The global DAG

The layout derives exclusively from documented `extends`, `combines` and the supporting `specializes` classification links. Graphviz's layered `dot` algorithm computes method ranks and routed paths. **No fixed category rectangles.** Disconnected components and singleton methods are valid: no imaginary edges are added to improve aesthetics.

`extends` and `combines` record actual technical improvements or fusion, with evidence, trade-offs and bottlenecks. `specializes` is gray taxonomy, **not** historical progress. `contrasts_with` is opt-in and does not determine DAG ranking. The overall knowledge graph need not be acyclic, while the main structural projection is validated as a DAG.

**Node color = editorial primary display paradigm:** classical numerical/optimization; statistical/probabilistic; machine/deep learning; physics–data hybrid. A method can retain multiple genuine method-family memberships regardless of its primary node color.

**Evolution-edge color = primary affected research phase:** I blue, II purple, III teal, otherwise neutral. The color comes from the originally documented `primary_stage_id` grouped into its parent phase, not from the methods' display regions. Line style distinguishes extensions, fusions and taxonomy.

## Workflow connections

Selecting a phase aggregates child-stage `uses_method` links, with separate semantics for a direct method role (possibly literature-supported), a family-level research lead, and a broader ancestor-family relation. The latter must **not** be silently promoted to method-specific empirical validation. Unannotated methods fade but remain accessible.

Nodes and actual SVG edges are both selectable, keyboard-accessible and inspectable, with methodological innovation, bottleneck, supporting sources, multiple family tags, Landmark papers and advisory Start Here readings.

## Build and review

`config/v07.json` defines the three-phase view and visual taxonomy; `scripts/build_v07.py` consumes the existing canonical methods and edges and emits a Graphviz-ranked SVG plus bilingual data. Build-time requirements include Graphviz and a CJK font:

```bash
python -m pip install -r requirements-dev.txt
python -m scripts.build_v07 --site build/viewer-v07
```

The generated viewer can be opened offline by double-clicking `index.html` beside `app.js` and `style.css`. CI builds a portable artifact and runs data/Graphviz and real Chromium desktop/mobile tests.

This is a v0.7 interactive prototype, **not yet the final GitHub Pages release**.
