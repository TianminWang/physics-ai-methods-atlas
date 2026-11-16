# Physics AI Methods Atlas · 物理 AI 方法图谱

> A living, evidence-linked methodological knowledge graph for **ODE/PDE inverse problems, Physics AI, neural operators, coronary hemodynamics, and patient-specific digital twins**.

**目标是理解方法体系，而不是收藏尽可能多的论文。** 默认以**方法演化森林**组织知识，并将论文、书籍、研究问题及跨方法融合关系关联到相应节点。以后可以从同一份数据切换到冠脉/数字孪生研究任务视图。

## Current release — curated method backbone v0.2 · 2026-11-16

| Entity | Count | Purpose |
|---|---:|---|
| Research areas | 5 | Navigation, not method ancestry |
| Methods | 30 | Traditional + learned approaches, curated for this initial scope |
| Papers/peer-reviewed chapters | 32 | Verified bibliographic references, reusable across methods |
| Books / monographs | 8 | Many-to-many coverage, with chapters when known |
| Research problems | 10 | Inversion, vascular flow, FFR, dynamic twins and intervention |
| Typed relations | 210 | Taxonomy, lineage, bibliography, applicability and coverage |

**Start here (优先阅读) ≠ 必须完成的任务。** Each method *may* suggest a small starting set (usually about 1–2 papers or textbook chapters), but **there is no mandatory count**. Some methods need no starting recommendation, others benefit from more. Landmark significance is attached to a **paper's contribution to a particular method**, not a blanket global paper badge. See [reading policy](docs/READING_POLICY.md).

## Conceptual forest (illustrative overview)

The arrows below make the general families legible. They are **not** a substitute for the precisely typed, evidence-linked edges in `data/relations/`.

~~~mermaid
flowchart LR
  LS["Nonlinear least squares"] --> GN["Gauss–Newton"] --> LM["Levenberg–Marquardt"]
  NO["Neural operator learning"] --> DeepONet["DeepONet"] --> PIDO["Physics-informed DeepONet"]
  NO --> FNO["FNO"] --> PINO["PINO"] --> BVPINO["Bi-variational PINO / coronary FFR"]
  FNO --> GeoFNO["Geo-FNO"]
  NO --> DINO["Derivative-informed operator"]
  KF["Kalman filtering"] --> EnKF["EnKF"] --> EKI["Ensemble Kalman inversion"]
  POD["POD / reduced basis"] --> OpInf["Operator inference"]
~~~

The real graph also links PINNs, learned-forward inversion, direct inverse operators, Bayesian inference, adjoints, 4D-Var, vascular boundary models and research applications. The full **interactive website** is planned for Phase 3.

## Recommended starting research path

**For ODE/PDE inversion + neural operators**, avoid reading every method node. A manageable spine is:

1. **Nonlinear least squares / PDE adjoints:** selected Chavent book sections + [Giles & Pierce (2000)](data/papers/giles-2000-adjoint.json).
2. **PINN:** [Raissi et al. (2019)](data/papers/raissi-2019-pinn.json).
3. **Operator-learning overview:** [Boullé & Townsend (2024)](data/papers/boulle-2024-math-guide.json).
4. **One operator architecture first:** [DeepONet (2021)](data/papers/lu-2021-deeponet.json) **or** [FNO (ICLR 2021)](data/papers/li-2021-fno.json); read the second later as needed.
5. **Physics-informed operators:** [PINO (2024)](data/papers/li-2024-pino.json).
6. **Inverse-problem bridge:** [Inverse problems with learned forward operators](data/papers/arridge-2024-learned-forward.json).
7. **Choose your specialization:** [direct inverse operator, ICLR 2025](data/papers/cho-2025-pidion.json), or [DINO, JCP 2024](data/papers/oleary-roseberry-2024-dino.json), or [Bayesian perspective](data/papers/stuart-2010-bayesian.json).

No full prerequisite mathematics curriculum is assumed. See [Minimal reading route and expansion branches](docs/READING_GUIDE.md).

## Research-specific examples

- [Patient-specific coronary parameter inference](data/problems/coronary-parameter-inference.json): physical inverse calibration, boundary models, sensitivities, Bayesian uncertainty.
- [Coronary FFR curve estimation](data/problems/coronary-ffr-curve.json): bi-variational PINO and angiographic applications.
- [Multi-vessel systemic calibration](data/problems/systemic-arterial-calibration.json): vascular operator surrogates and Bayesian inference (**systemic, not proof of coronary validation**).
- [Virtual PCI counterfactual modeling](data/problems/virtual-pci-counterfactual.json): a **future research question**, not yet a validated method node.

## Canonical data and development

~~~text
data/{areas,methods,papers,books,problems,relations}/   one JSON file per record
schemas/atlas.schema.json                              schema version 2.0.0
scripts/validate.py                                    semantic + reference validation
scripts/export_graph.py                                derived normalized nodes/edges
tests/                                                regression tests
docs/                                                 architecture and curation guidance
~~~

A method's `start_here` list is **optional, ordered, uncapped** and may reference either `paper.*` or `book.*`. Other papers stay attached using typed relationships; they are **not** additional required reading. Method `status=curated` reflects reviewed content, **not how many papers were recommended**.

To check or export the source graph (Python 3.11+):

~~~bash
python -m pip install -r requirements-dev.txt
python -m scripts.validate
python -m pytest -q
python -m scripts.export_graph --output build/atlas-graph.json
~~~

The exported JSON is generated; edit the source records instead of hand-maintaining graph files.

**Documentation:** [Architecture](docs/ARCHITECTURE.md) · [Reading policy](docs/READING_POLICY.md) · [Reading guide](docs/READING_GUIDE.md) · [Contributing](docs/CONTRIBUTING.md) · [Roadmap](docs/ROADMAP.md).

**Scope:** Scientific modeling, physical inverse problems and model learning. Coronary hemodynamics is the primary application, but classical numerical methods and transferable learning techniques are first-class citizens. A newer paper is not automatically a superior method; linkage claims require semantic and scientific justification.
