# Minimal Reading Guide · 面向反问题与神经算子的最小阅读主线

## Goal

Understand how traditional inverse methods and modern physical neural operators relate **without** reading every paper in the repository. You do **not** need to resume a full mathematics curriculum. Supplement Jacobians, optimization, Fourier transforms, probability, or numerical PDEs **when you need them** to understand a specific method.

This is a **path, not a course or a checklist**. The first paper/book recommended by a method is a *starting point*, never a mandatory reading assignment. A single source may cover several nodes. Detailed proofs can be revisited when relevant to actual research.

## Suggested route (about 7 readings spread over time)

| Order | Research question | One recommended reference | Nodes reached | Reason |
|---|---|---|---|---|
| 1 | How does a physics inverse problem become an optimization problem? | [Chavent — Nonlinear Least Squares for Inverse Problems](../data/books/chavent-nonlinear-least-squares.json), selected finite-dimensional parts | Nonlinear least squares, Gauss–Newton, regularization | Connect forward-map residuals, sensitivity and stability |
| 2 | How do we compute gradients through physics models? | [Giles & Pierce (2000), An Introduction to the Adjoint Approach to Design](../data/papers/giles-2000-adjoint.json) | Adjoint sensitivity, PDE-constrained optimization | Understand the Lagrangian/adjoint trick in an accessible way |
| 3 | What does a neural PDE solution with physical constraints look like? | [Raissi et al. (2019), Physics-informed neural networks](../data/papers/raissi-2019-pinn.json) | PINN, inverse PINN | Establish soft PDE residuals and inverse coefficient learning |
| 4 | What changes from a single solution to a map between functions? | [Boullé & Townsend (2024), A mathematical guide to operator learning](../data/papers/boulle-2024-math-guide.json) | Neural operator, function representation | Best conceptual bridge before architectural details |
| 5 | How is an operator parameterized? | **Choose one**: [Lu et al. DeepONet (2021)](../data/papers/lu-2021-deeponet.json) or [Li et al. FNO (2021)](../data/papers/li-2021-fno.json) | DeepONet **or** FNO | DeepONet gives branch/trunk intuition; FNO gives spectral operator layers |
| 6 | What does physics-informed operator learning add? | [Li et al. PINO (2024)](../data/papers/li-2024-pino.json) **or** [Wang et al. physics-informed DeepONet (2021)](../data/papers/wang-2021-physics-deeponet.json) | PINO / physics-informed DeepONet | Combine operator learning with residual physics |
| 7 | How does an operator actually help an inverse problem? | [Arridge et al. (2024), Inverse problems with learned forward operators](../data/papers/arridge-2024-learned-forward.json) | Learned-forward inversion | Understand surrogate bias, reconstruction stability and correction |

These are not a forced sequence in calendar weeks. If your current research already uses nonlinear least squares and adjoints, **start at step 3 or 4**. Step 5 explicitly chooses **one** of two main operator architectures initially.

## Only then open one relevant branch

| Research intention | Recommended one-step extension | Why |
|---|---|---|
| Direct mapping from sparse observation to unknown PDE parameter | [Cho & Son, PI-DION (ICLR 2025)](../data/papers/cho-2025-pidion.json) | Direct inverse operators vs iterative inversion through a forward surrogate |
| Gradient-sensitive neural surrogates | [O'Leary-Roseberry et al., DINO (JCP 2024)](../data/papers/oleary-roseberry-2024-dino.json) | Learned Jacobians and outer-loop optimization |
| Bayesian uncertainty and posterior approximation | [Stuart (2010), Bayesian perspective](../data/papers/stuart-2010-bayesian.json) | Priors, posteriors and well-posedness; selected sections first |
| Sequential patient-specific twin updates | [Asch et al., Data Assimilation](../data/books/asch-data-assimilation.json), selected Kalman/variational chapters | State estimation over time |
| Reduced-order forward modeling | [Sirovich (1987), Snapshot POD](../data/papers/sirovich-1987-pod.json), then [Operator Inference (2016)](../data/papers/peherstorfer-2016-opinf.json) | Compact state/trajectory representation |
| Geometry-changing vessels | [Geo-FNO (JMLR 2023)](../data/papers/li-2023-geofno.json) | Why standard Fourier operators need geometric adaptation |
| Vascular outflow parameters | [Westerhof et al., arterial Windkessel (2009)](../data/papers/westerhof-2009-windkessel.json) | Physical boundary-model assumptions and inversions |
| Systemic multi-vessel inverse inference | [Ryan et al. (2026)](../data/papers/ryan-2026-cardiovascular-pino.json) | Direct example of operator surrogates + Bayesian calibration in **systemic**, not coronary, vessels |
| Coronary FFR curve from angiography | [Xie et al., BVPINO (2025)](../data/papers/xie-2025-bvpino.json) | Direct coronary-specific physics-informed operator application |

## Minimal experiment that connects the whole map

1. Solve a one-dimensional ODE or Poisson PDE with an ordinary numerical solver.
2. Fit unknown coefficients with least squares and a suitable regularizer.
3. Train a simple data-driven solution surrogate, then DeepONet or FNO, using a *family* of parameter settings.
4. Re-run the **same inversion** by optimizing through the learned forward map.
5. Compare both forward and **inverse** error, noise sensitivity, out-of-distribution behavior, time cost, and whether the gradient of the surrogate agrees with the reference solver.

A well-predicted state field does **not** guarantee a correctly recovered physical parameter. The final comparison matters much more than architectural novelty.

## How to use each node

Read its `core_idea` → `innovation` → `limitations` → `start_here` reference **if one is suggested** → optional other papers. You can stop once you can state (a) what the model learns, (b) what assumptions/observations it needs, (c) what differentiates it from predecessors, and (d) why it may help or fail for your inverse problem.

Landmark status captures a paper's *scholarly role for a particular method*. It is **not** equivalent to “you must read this paper now”.
