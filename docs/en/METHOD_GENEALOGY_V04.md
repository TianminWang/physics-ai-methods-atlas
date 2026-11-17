# v0.4 Method Genealogy: Scientific Computing, Inverse Problems, Generative Models and World Models

This is a **selective, evidence-linked expansion** of the v0.3 single-workflow-axis / independent-method-DAG architecture. New paper records are sourced from journals or peer-reviewed proceedings; historical significance is **contextual to each paper→method relation**, and `start_here` readings are optional.

## 1. Numerical foundations

New nodes [FDM](../../data/methods/finite-difference.json), [FVM](../../data/methods/finite-volume.json), [FEM](../../data/methods/finite-element.json), and [Runge–Kutta](../../data/methods/runge-kutta-integration.json) are **parallel discretization/integration families**, not an invented linear historical progression. They primarily link to focused textbooks by LeVeque, Brenner–Scott, and Hairer et al. [DiffTaichi](../../data/methods/difftaichi.json) provides differentiable simulation infrastructure but does not remove solver/model error.

## 2. Inverse inference and information

[Profile-likelihood identifiability](../../data/methods/profile-likelihood-identifiability.json) addresses whether observed data genuinely determine unknown parameters, which differs from whether an optimizer converges. Probability-focused methods now include [MCMC](../../data/methods/markov-chain-monte-carlo.json), [NUTS](../../data/methods/no-u-turn-sampler.json), [VI](../../data/methods/variational-inference.json), [simulation-based inference](../../data/methods/simulation-based-inference.json), and [sequential neural posterior estimation](../../data/methods/sequential-neural-posterior.json).

A complementary branch, [Bayesian model discrepancy](../../data/methods/bayesian-model-discrepancy.json), separates physical simulator inadequacy from calibration parameter uncertainty. [Bayesian experimental design](../../data/methods/bayesian-experimental-design.json) connects observations to expected information gain.

## 3. Operator architecture expansion

The Atlas retains DeepONet, FNO, PINO, Geo-FNO and DINO, and adds:

- [Multipole Graph Neural Operator](../../data/methods/multipole-graph-neural-operator.json), using multilevel graph interactions for long-range operator behavior;
- [Galerkin Transformer](../../data/methods/galerkin-transformer.json), adapting attention with function-space projection interpretations;
- [MeshGraphNets](../../data/methods/meshgraphnets.json), in a **separate learned-mesh-simulation family**. Learned graph rollout is not automatically a mesh-invariant neural operator.

## 4. Generative models and inverse problems

Parallel foundations now include [VAE](../../data/methods/variational-autoencoder.json), [GAN](../../data/methods/generative-adversarial-network.json), [normalizing flows](../../data/methods/normalizing-flow.json), [DDPM](../../data/methods/diffusion-probabilistic-model.json), [score-based SDE modeling](../../data/methods/score-based-sde.json), and [flow matching](../../data/methods/flow-matching.json).

Evidence-backed extensions now explain specific changes:

| Method direction | Improvement | Research stage |
|---|---|---|
| Score-based generation → [DPS](../../data/methods/diffusion-posterior-sampling.json) | Add measurement guidance for noisy inverse problems; approximate posterior, not an exact sampling guarantee | Inversion |
| DDPM → [Physics-informed diffusion](../../data/methods/physics-informed-diffusion.json) | Add first-principles residual penalties | Forward physics |
| Pretrained generator → [learned generative prior inversion](../../data/methods/generative-range-prior.json) | Restrict inverse solutions to learned generator range | Inversion |

**Physical residual losses are not exact physical enforcement**, and generating multiple samples is not equivalent to demonstrating reliable posterior calibration.

## 5. World models, control and offline decisions

[PlaNet](../../data/methods/planet-latent-planning.json) learns latent dynamics and online planning; [Dreamer](../../data/methods/dreamer-latent-imagination.json) trains behavior on imagined latent trajectories. [MPC](../../data/methods/model-predictive-control.json), [MBPO](../../data/methods/model-based-policy-optimization.json), and [CQL](../../data/methods/conservative-q-learning.json) use different assumptions: constrained online planning, short model rollouts for policy optimization, and conservative offline value estimates respectively. **None is claimed as clinically validated for virtual coronary PCI.**

## 6. Uncertainty and observation design

[Generalized polynomial chaos](../../data/methods/polynomial-chaos-expansion.json) propagates uncertain PDE inputs; model discrepancy and experimental design address the distinct questions of model bias and information quality. These techniques coexist with cross-cutting physical validity and generalization concerns.

## 7. Reduce reading rather than accumulate homework

Continue the existing [minimal reading guide](../READING_GUIDE.md). For a focused generative-inverse extension, start with Ho (DDPM) and Chung (DPS); for likelihood-free inference, Cranmer et al.; for world models, PlaNet before Dreamer; for model error, Kennedy–O'Hagan (2001). Select **one branch at a time**—there is no fixed paper quota.

## 8. Honest coverage limits

The corpus remains a structured **initial methods atlas**, not a complete account of all Physics AI. Coronary 0D/1D/3D model variants, measurement operators, robust clinical digital twins, multi-physics and rigorous virtual-PCI evidence require further curation. Visual validation (v0.5) and the full site (v1.0) remain future stages.
