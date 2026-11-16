# Unified research workflow and method-genealogy DAG · v0.3

## 1. Primary organizing principle

The project maintains **one canonical knowledge graph**, not two independent research databases. It must answer:

1. What capabilities do physical modeling, observations, inverse estimation, prediction, intervention and continual updating require?
2. What reusable method families and individual algorithms serve those capabilities?
3. Which technical mechanism changed between a predecessor and a successor; what bottleneck motivated it; what is the evidence and tradeoff?

**Workflow stages are not methodological parents.** They point to methods/families by functional links. A method may be useful in multiple stages without duplicating its underlying record.

## 2. Six workflow stages

| ID | Capability | Color |
|---|---|---|
| `stage.physics-forward` | Physical representation and forward simulation | blue `#2563EB` |
| `stage.observation` | Observation and measurement modeling | cyan `#0891B2` |
| `stage.inverse-calibration` | Individualized inversion and state estimation | purple `#7C3AED` |
| `stage.prediction-uq` | Trustworthy prediction and UQ | amber `#B45309` |
| `stage.intervention-planning` | Counterfactual intervention and decisions | rose `#BE185D` |
| `stage.continual-update` | New observations, assimilation, updating | green `#15803D` |

`feeds_into` connects compatible information flows: forward modeling and observations jointly feed inversion. `feeds_back_to` captures continual updates to previous calibration, modeling or prediction. The workflow **may contain loops**. Its order is explanatory, not a requirement that each independent research project implement all stages.

Cross-cutting concerns (`concern.*`) cover physical conservation, identifiability, model/discretization error, uncertainty calibration and out-of-distribution validation.

## 3. Method families are independent and reusable

A family (`family.*`) represents a conceptual methodological branch; `subfamily_of` constructs a classification DAG. Specific methods (`method.*`) connect by `member_of_family` and may have more than one membership, but **each method has exactly one canonical record**.

`stage.* → family.*` or `stage.* → method.*` is a `uses_method` functional link. It explains **how** that method is relevant to that stage, in English and Chinese. For example, neural operators can be a forward surrogate in Stage 1, an inner-loop model in Stage 3, or a fast predictive operator in Stage 4. This does **not** imply the family was historically invented for those applications.

Family `coverage_status=planned` flags incomplete **Atlas coverage**, never the maturity of the external scientific field. Current gap scaffolds include classical numerical discretization, differentiable simulation, generative models and control/planning.

## 4. Distinguish taxonomy, genealogy and learning

| Relation | Direction | Interpretation |
|---|---|---|
| `specializes` | specific method → general method | Taxonomic/specialized form, not necessarily an improvement |
| `extends` | successor → predecessor | Evidence-backed methodological extension |
| `combines` | hybrid → component | Evidence-backed technical fusion |
| `depends_on` | method → prerequisite | Learning prerequisite, not historical influence |
| `contrasts_with` | method ↔ method | Alternative assumptions or computational tradeoffs |
| paper→method roles | paper → method | Introduces, analyzes, applies, surveys or compares |

`extends` and `combines` must have:

- `innovation_detail` / `innovation_detail_zh`: **what changed**;
- `bottleneck` / `bottleneck_zh`: **the targeted problem**;
- `evidence_paper_ids`: primary scholarly support.

Additional `tradeoff` and `stage_ids` describe costs and scope. `primary_stage_id` is optional; if provided, it must belong to `stage_ids`. The primary stage color is for **research motivation**, not a claim that a method cannot apply elsewhere.

Physical source records point from successor to predecessor; the future viewer may visually orient arrows from predecessor to successor to make evolution easier to read.

## 5. Semantic visual language

- Workflow `feeds_into`: stage-colored solid link.
- Workflow `feeds_back_to`: stage-colored dashed feedback.
- Functional `uses_method`: stage-colored dashed link with an explanatory role.
- Method `extends`: solid, colored by primary linked stage if one is supported.
- Method `combines`: distinct fusion/double edge, same conditional color logic.
- `member_of_family`, `subfamily_of`, `specializes`: neutral taxonomy connectors.
- `concern_applies_to`: neutral dotted links for pervasive quality conditions.

Line style communicates **relationship type**; color communicates **affected research capability**. Always preserve text labels to remain readable without color perception.

**Example: FNO → Geo-FNO**: a learned geometric deformation extends spectral operator layers to irregular domains. The direct bottleneck is geometric/mesh representation (Stage 1 blue); potential prediction uses are recorded as secondary Stage 4, without asserting general coronary clinical validation.

## 6. Records and bilingual projections

Canonical sources:

- `data/{stages,families,concerns,methods,relations,papers,books,problems,areas}/`
- `schemas/atlas.schema.json`
- `locales/zh-CN.json` (translation-only labels for legacy methods)
- `scripts/validate.py`, `scripts/export_graph.py`, `scripts/export_unified.py`

Schema v2.1.0 is **additive and backward-compatible with existing v2.0.0 records**. There is no mass rewriting of paper/monograph metadata or stable IDs. Chinese and English are display projections over the same scientific graph.

`python -m scripts.export_unified --lang zh` produces a render-ready view with `workflow_axis`, localized `nodes`, semantically typed and colored `edges`, `views.overview` for workflow+families, and `views.expanded` for later detailed interaction. Paper/book records are kept in the full authoritative graph and should be loaded on demand rather than added as thousands of nodes to the overview.

## 7. Explicit limits and next steps

The present stage **does not** fill entire generative, numerical or RL literature branches; nor does it deploy GitHub Pages. The main goal is to make future evidence-based expansion unambiguous and nonduplicative.

Order: **v0.3 unified structure → v0.4 verified literature and method family expansion → v0.5 small-graph visualization QA → v1.0 interactive browsing**. Landmark status remains contextual to paper→method roles; Start Here remains advisory with no fixed paper count.
