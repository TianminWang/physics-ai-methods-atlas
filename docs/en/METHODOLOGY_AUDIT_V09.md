# v0.9 Methodology structure audit and ontology proposal

> **Audit first, evidence review second, visualization last.** No canonical scientific records or current v0.8 website behavior are changed in this phase.

Audit baseline: GitHub `main` commit `5591a85784cb526dfd6ce8044e4a409c0eff8621`. Rerun with `python -m scripts.audit_v09 --output build/audit-v09.json`.

## 1. Grounded inventory

| Scope | Count |
|---|---:|
| Canonical `method.*` | 61 |
| Method families `family.*` | 34 |
| Existing `problem.*` scenarios/tasks | 15 |
| Papers / books | 58 / 12 |
| Typed relationships | 530 |
| Family memberships / family hierarchy links | 67 / 29 |
| Direct method-to-problem `addresses` links | 93 |
| Stage-to-method/family `uses_method` links | 55 |
| Evidence-backed `extends` / `combines` | 12 / 4 |
| Methods participating in those genealogy links | 24 |
| Methods without a recorded genealogy link | 37 |
| Nontrivial genealogy components | 8 |

All 61 current methods have at least one family membership. Six methods have multiple direct family memberships. All 15 problems have a method-to-problem link. Seven upper family categories have no **direct** method members, which is not necessarily a defect: they can organize subfamilies.

Three methods lack a direct `addresses` link: Deep Galerkin, Deep Ritz and Physics-Informed DeepONet. This is a candidate coverage follow-up, not a verdict on their importance.

## 2. Main semantic findings

The existing `method.*` set mixes different epistemic levels:

- **Problem formulations:** Bayesian Inverse Problems, Nonlinear Least Squares, PDE-Constrained Optimization.
- **Broad method families:** MCMC, SBI, Neural Operator Learning, VI.
- **Concrete algorithms:** Gauss–Newton, LM, NUTS, EnKF, CQL.
- **Numerical schemes:** finite difference, finite volume, finite element, Runge–Kutta.
- **Model architectures and families:** DeepONet, FNO, PINO, VAE, GAN, diffusion models.
- **Training/inference strategies:** Flow Matching, learned-forward inversion, generative prior and physics-guided diffusion.
- **Mechanistic models:** Windkessel and structured-tree outflow.
- **Software infrastructure:** DiffTaichi.

These should not all be given identical taxonomy semantics. A **provisional, non-canonical** first classification of all 61 existing entities is stored in [method-kind-proposals.json](../../audits/v09/method-kind-proposals.json). A primary display kind can coexist with additional facets and multiple real scholarly family memberships.

The current `problem.*` collection mixes general inverse tasks with specific vascular/clinical scenarios. A reusable **Capability** layer should be distinct from both these scenarios and the methodological family taxonomy. The [draft capability catalog](../../audits/v09/capability-layer-proposal.json) proposes 19 cross-application capabilities: 6 for modeling, 8 for inference, 5 for personalized prediction/intervention/update. It maps all 15 existing problems to candidate capabilities **for design review, not as verified method efficacy**.

## 3. Four separate relationship meanings

1. **Scientific task/functional roles:** phase → capability → family/method, and existing `addresses` links from methods to problems. A family role never automatically proves every member's efficacy.
2. **Conceptual classification:** `member_of_family`, `subfamily_of`, `specializes`. These encode inclusion/specialization, not historical progress.
3. **Technical mechanism transfer:** prospective `uses_training_strategy`, `adapts_algorithm_from`, `uses_component`, `unifies_or_generalizes`. These are **design proposals only**, not yet schema predicates.
4. **Historical methodology evolution:** `extends` and `combines` require original-paper evidence, an explicit innovation mechanism, targeted bottleneck and trade-offs.

For example, Flow Matching is characterized in its ICLR paper as a training approach for continuous normalizing flows; Song et al. describe the score-SDE framework as encompassing earlier score-based and diffusion approaches. These are candidates for more precise link semantics, not proof that the current edges are categorically incorrect. Sources: [Lipman et al., ICLR 2023](https://mlanthology.org/iclr/2023/lipman2023iclr-flow/), [Song et al., ICLR 2021](https://mlanthology.org/iclr/2021/song2021iclr-scorebased/), [Kingma & Welling, ICLR 2014](https://mlanthology.org/iclr/2014/kingma2014iclr-auto/). A ten-item [relation-review queue](../../audits/v09/relation-review-queue.json) documents specific original relations and their scholarly questions. No edges were retyped in this phase.

## 4. Root cause of v0.8's empty highlight

The functional stage → family/method map covers **all 61 methods**, but the main v0.8 SVG renders only the **24 methods** involved in documented `extends` or `combines` edges. Thus a valid functional link to, e.g., Bayesian model discrepancy or SBI may focus a method in the collapsed shelf, leaving no visible highlighted SVG node. This is a **UI projection mismatch**, not evidence that the methods or links are missing.

A future viewer must guarantee navigable results for every valid functional link: select on canvas, expand and locate in the unlinked shelf, or show an explicit list of family-level candidate methods and evidence scopes.

## 5. Proposed architecture

Retain the **three-phase scientific axis** and existing six stage IDs as sub-capabilities. Add a reusable, **multi-to-multi Capability layer**. Keep one canonical method record per method, with concept type/facets and multiple family memberships. Keep problem/application scenarios separate, and render three perspectives from the same knowledge graph:

- **Problem/capability view:** what questions must be solved and which different approaches can help?
- **Method taxonomy view:** which families, algorithm types and cross-family memberships organize the methods?
- **Method genealogy view:** which *documented* advancements and fusions explain a method's predecessors and descendants?

Disconnected evolution components are scientifically acceptable. The goal is complete **problem → capability → method → evidence** traceability, not a forced single connected DAG.

## 6. Next actions

Phase A (this PR): audit, provisional types, proposed capability definitions, academic edge review queue and read-only automated validation.

Phase B: agree on the ontology and define backward-compatible schema migration.

Phase C: verify primary scholarly evidence and correct only relations that are substantiated.

Phase D: complete representative problem-to-capability-to-method routes, emphasizing inverse problems and coronary digital-twin use cases.

Phase E: update v0.8 visualization to reflect the verified ontology and fix functional-link navigation, before GitHub Pages.

See the full Chinese [audit](../zh/AUDIT_V09.md), [ontology](../zh/ONTOLOGY_V09.md) and [remediation plan](../zh/REMEDIATION_V09.md).
