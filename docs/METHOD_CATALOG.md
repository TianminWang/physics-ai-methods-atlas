# Method Catalogue · v0.2 初始方法目录

This is an **editorial index of the first 30 methods**, grouped by the role they play in scientific inverse problems. It is **not** a unique-parent historical tree: a method may belong to multiple areas and have more than one methodological predecessor. The source of truth is in [data/methods](../data/methods) and [data/relations](../data/relations).

**阅读建议：** 从[最小阅读主线](READING_GUIDE.md)切入，不需要将本目录的30个节点全部读完。“优先阅读（Start Here）”不设数量限制，也不等于学术里程碑；里程碑由论文对具体方法的贡献关系给出。

## A · Classical optimization and inverse theory (6)

| Method | Core use in inversion |
|---|---|
| [Nonlinear least squares](../data/methods/nonlinear-least-squares.json) | Fit unknown parameters to data via a forward model |
| [Gauss–Newton](../data/methods/gauss-newton.json) | Linearized least-squares parameter corrections |
| [Levenberg–Marquardt](../data/methods/levenberg-marquardt.json) | Damped local parameter updates |
| [Tikhonov regularization](../data/methods/tikhonov-regularization.json) | Control instability and incorporate prior structure |
| [Adjoint sensitivity](../data/methods/adjoint-sensitivity.json) | Gradients with many model parameters |
| [PDE-constrained optimization](../data/methods/pde-constrained-optimization.json) | Optimization under governing-equation constraints |

## B · Bayesian inference and data assimilation (5)

| Method | Core use |
|---|---|
| [Bayesian inverse problems](../data/methods/bayesian-inverse-problems.json) | Prior-likelihood-posterior and uncertainty |
| [Kalman filter](../data/methods/kalman-filter.json) | Recursive linear-Gaussian state estimates |
| [Ensemble Kalman filter](../data/methods/ensemble-kalman-filter.json) | Sample-ensemble sequential state updates |
| [Ensemble Kalman inversion](../data/methods/ensemble-kalman-inversion.json) | Iterative parameter updates using ensemble covariance |
| [4D-Var](../data/methods/four-d-var.json) | Time-window variational state estimation |

## C · Reduced physical forward models and hemodynamic boundaries (4)

| Method | Core use |
|---|---|
| [Snapshot POD](../data/methods/proper-orthogonal-decomposition.json) | Construct reduced state bases |
| [Operator inference](../data/methods/operator-inference.json) | Nonintrusive data-driven reduced dynamics |
| [Windkessel](../data/methods/windkessel.json) | Lumped arterial resistance/compliance outflow |
| [Structured-tree outflow](../data/methods/structured-tree-outflow.json) | Frequency-dependent distal arterial impedance |

## D · Neural solvers for individual PDE problems (3)

| Method | What it minimizes |
|---|---|
| [PINN](../data/methods/pinn.json) | Differential-equation residuals + data/boundary errors |
| [Deep Ritz](../data/methods/deep-ritz.json) | Variational energy |
| [Deep Galerkin Method](../data/methods/deep-galerkin.json) | Sampled PDE residuals in a meshfree scheme |

## E · Neural operator learning and physics-constrained operators (8)

| Method | Main idea |
|---|---|
| [Neural operator](../data/methods/neural-operator.json) | Learn function-to-function mappings for PDE families |
| [DeepONet](../data/methods/deeponet.json) | Branch/trunk decomposition |
| [FNO](../data/methods/fno.json) | Fourier-domain operator layers |
| [Physics-informed DeepONet](../data/methods/physics-informed-deeponet.json) | DeepONet with physical constraints |
| [PINO](../data/methods/pino.json) | Operator learning combined with PDE residual losses |
| [Geo-FNO](../data/methods/geo-fno.json) | Adapt Fourier layers to nonrectangular geometries |
| [Derivative-informed neural operator](../data/methods/derivative-informed-operator.json) | Learn operator outputs **and derivatives** |
| [BVPINO](../data/methods/bi-variational-pino.json) | Variationally weighted physics-informed operator for coronary FFR curves |

## F · Learning approaches that explicitly target the inverse mapping (2)

| Method | Main idea |
|---|---|
| [Inverse with learned forward operators](../data/methods/learned-forward-inversion.json) | Repeated inverse optimization through a trained forward model |
| [Physics-informed direct inverse operator](../data/methods/direct-inverse-operator.json) | Learn observation-to-unknown map across inverse instances |

These two routes are **not interchangeable**: a forward surrogate may enable traditional optimization and Bayesian sampling, while a direct inverse operator amortizes inference by training a different mapping.

## G · Learnable / discovered time dynamics (2)

| Method | Main idea |
|---|---|
| [SINDy](../data/methods/sindy.json) | Sparse discovery of governing ODE terms |
| [Neural ODE](../data/methods/neural-ode.json) | Learned continuous-time neural state dynamics |

## Research-problem entry points

- [ODE parameter inference](../data/problems/ode-parameter-inference.json)
- [PDE coefficient inference](../data/problems/pde-coefficient-inference.json)
- [Coronary hemodynamic parameter inference](../data/problems/coronary-parameter-inference.json)
- [Systemic multi-vessel arterial calibration](../data/problems/systemic-arterial-calibration.json)
- [Bayesian vascular calibration](../data/problems/vascular-bayesian-inference.json)
- [Coronary FFR curve from angiography](../data/problems/coronary-ffr-curve.json)
- [Dynamic state assimilation](../data/problems/dynamic-state-assimilation.json)
- [Geometry-dependent forward surrogate](../data/problems/geometry-dependent-forward-surrogate.json)
- [Virtual PCI counterfactual modeling](../data/problems/virtual-pci-counterfactual.json)
- [Longitudinal digital-twin updates](../data/problems/online-digital-twin-update.json)

**Evidence boundary:** A validated *systemic* multi-vessel forward/inverse benchmark does not establish validated **coronary** performance. Similarly, connecting a technique to virtual PCI as a **potential method** does not claim it has been clinically proven for that scenario.

Future stages will add uncertainty-aware model updating, differentiable CFD, optimization/control, generative counterfactuals and planning methods **when supported by sufficient relevant literature**.
