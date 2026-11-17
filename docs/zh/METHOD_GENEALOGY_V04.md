# v0.4 方法谱系：从传统反问题到生成式物理 AI 与世界模型

> 一张统一研究主轴上的方法演化索引：重点看**技术改进、目标瓶颈和证据文献**，而不是一次读完所有论文。

本轮保持 v0.3 的六个研究环节及方法家族独立原则。方法与研究环节通过有说明的功能边连接；方法谱系内部区分分类 (`specializes`)、扩展 (`extends`)、融合 (`combines`) 和对照 (`contrasts_with`)。**相邻出版年份并不能证明直接继承关系。**

## 1. 物理建模与数值计算：传统数值方法是基础基线

- [有限差分 FDM](../../data/methods/finite-difference.json)：差分近似 → 离散方程；适合学习离散误差与稳定性。
- [有限体积 FVM](../../data/methods/finite-volume.json)：控制体积分与界面通量 → 局部守恒；对血流动量/连续方程尤其重要。
- [有限元 FEM](../../data/methods/finite-element.json)：弱形式、试探/测试函数、几何网格；不是由 FDM “演进而来”的单线后继。
- [Runge–Kutta 时间积分](../../data/methods/runge-kutta-integration.json)：ODE 或半离散 PDE 的时间推进方法。

这四种方法不是一条直线的“前代→后代”；在 Atlas 中主要是**平行的方法分类和技术对照**。优先阅读的是 LeVeque、Brenner–Scott、Hairer 等经典书的相关章节，而不是强行找一篇所谓“发明 FVM 的 Landmark”。

[可微物理模拟 DiffTaichi](../../data/methods/difftaichi.json) 提供与数值模拟程序求导相关的独立方法路线；它不等于 PINN，也不能替代模型与离散误差检查。

## 2. 反问题及概率推断：把“会优化”与“能辨识”分开

**确定性反演：** Chavent/最小二乘 → Gauss–Newton/LM → 伴随梯度及 PDE 约束优化，原有方法全部保留。

新增 [剖面似然可辨识性分析](../../data/methods/profile-likelihood-identifiability.json)，用于检查在有限、含噪观测下究竟哪些参数能被确定。**优化器收敛并不证明参数可辨识。**

**概率反演和计算：**
- [MCMC](../../data/methods/markov-chain-monte-carlo.json) → [NUTS](../../data/methods/no-u-turn-sampler.json)，前者是广义采样方法，后者为可自动确定轨迹长度的 HMC 实现之一；这里只记录分类，不假装 NUTS 是直接改造每一种 MCMC。
- [变分推断 VI](../../data/methods/variational-inference.json)：通过优化近似后验分布，与 MCMC 属于替代性计算路线。
- [仿真驱动推断 SBI](../../data/methods/simulation-based-inference.json) → [序贯神经后验估计 APT](../../data/methods/sequential-neural-posterior.json)：当仿真器可生成数据、但似然不可直接计算时提供另一条推断路线。

补充 [贝叶斯模型失配校准](../../data/methods/bayesian-model-discrepancy.json)：将模拟器系统偏差与未知参数区分建模，防止参数“代偿”错误的正向模型。它与新加入的 [贝叶斯实验设计](../../data/methods/bayesian-experimental-design.json) 一起连接到**观测是否充分**的问题。

## 3. 神经算子：从双路线拓展到图与注意力

原有 [DeepONet](../../data/methods/deeponet.json)、[FNO](../../data/methods/fno.json) 及 PINO、Geo-FNO、DINO 保留。

新增两条有明确原始研究的架构：

- [Multipole Graph Neural Operator](../../data/methods/multipole-graph-neural-operator.json)：将多级图结构和长程相互作用引入 PDE 算子近似，对应的技术问题是全局图消息传递的复杂度。
- [Galerkin Transformer](../../data/methods/galerkin-transformer.json)：用注意力/投影解释学习 PDE 算子，并研究如何改变 softmax 注意力设计。

另收录 [MeshGraphNets](../../data/methods/meshgraphnets.json)，但**单独放在“网格图学习模拟”家族**，因为在物理网格上传播消息进行状态滚动，不能自动等同于具备离散化无关性结论的神经算子。

这三者的联系主要是**同类问题的不同表示策略**，不能因为都含 Graph/Transformer 就随意画成相互继承。

## 4. 生成式建模及生成式反问题：本次主要补足的缺口

基础生成方法包括：

- [VAE](../../data/methods/variational-autoencoder.json)、[GAN](../../data/methods/generative-adversarial-network.json)：潜变量生成与对抗生成是并行路线。
- [Normalizing Flow](../../data/methods/normalizing-flow.json) → [Flow Matching](../../data/methods/flow-matching.json)：Flow Matching 为连续归一化流提供基于条件概率路径的向量场回归训练；不是说所有离散可逆流都必须先转化为扩散模型。
- [DDPM](../../data/methods/diffusion-probabilistic-model.json) → [Score-SDE](../../data/methods/score-based-sde.json)：连续 SDE 框架统一理解得分生成与扩散过程（方法学概念扩展，非简单改名）。

与物理及反问题交叉的关键分叉：

| 方法边 | 技术变化 | 针对的瓶颈 | 主轴配色 |
|---|---|---|---|
| Score-SDE → [DPS](../../data/methods/diffusion-posterior-sampling.json) | 加入近似观测似然梯度 | 无条件生成不满足稀疏观测 | **反演**（紫） |
| DDPM → [Physics-Informed Diffusion](../../data/methods/physics-informed-diffusion.json) | 训练中加入控制方程残差 | 生成样本可能不满足物理规律 | **物理建模**（蓝） |
| 学习型生成器 → [生成式先验反演](../../data/methods/generative-range-prior.json) | 在生成器输出范围内做欠定反演 | 仅靠稀疏观测求解不稳定 | **反演**（紫） |

注意，**DPS 是近似后验采样而非精确贝叶斯求解保证**；物理信息扩散通常借助软损失，也不等于严格保证所有生成结果满足 PDE。上述关键边的技术瓶颈和原论文证据已存入关系数据。

## 5. 世界模型与干预决策：独立于“生成式图像预测”

- [PlaNet](../../data/methods/planet-latent-planning.json)：由高维观测学习潜在状态空间动态，并在线规划。
- PlaNet → [Dreamer](../../data/methods/dreamer-latent-imagination.json)：在模型生成的潜在想象轨迹上训练行为策略，以学习型策略替代单纯在线搜索。
- [MPC](../../data/methods/model-predictive-control.json)：基于预测模型进行滚动时域控制优化。
- [MBPO](../../data/methods/model-based-policy-optimization.json)：利用短模型生成轨迹减轻模型误差对 RL 策略更新的影响。
- [CQL](../../data/methods/conservative-q-learning.json)：针对离线数据分布外动作的 Q 值高估，用保守价值正则化学习策略。

MPC、MBPO 和 CQL 主要是**相邻、不同假设的决策技术路线**，不能画成单一替代链。冠脉虚拟 PCI 目前仅标注潜在迁移，不声称上述方法已经获得冠脉临床有效性验证。

## 6. 可信性、误差与观测设计

- [广义多项式混沌展开 gPCE](../../data/methods/polynomial-chaos-expansion.json)：传播低维不确定输入到解场的分布或统计量。
- [贝叶斯模型失配](../../data/methods/bayesian-model-discrepancy.json)：区分物理模型偏差与个体参数不确定性。
- [贝叶斯实验设计](../../data/methods/bayesian-experimental-design.json)：针对参数可辨识性和信息增益选择更有价值的观测。

这些是服务多个研究环节的**技术方法**。横向的“物理一致性/可辨识性/外部验证”等 concern 节点仍然保留为**评价要求**，不与具体算法混为同一种对象。

## 7. 读什么，才能减小学习负担？

**不建议逐个读完新增31个方法节点。** 如果当前目标是神经算子 + 反问题，建议沿已有 [最小阅读指南](../READING_GUIDE.md) 前进，在需要时只展开一条专题：

- 生成式反演入门：先读 [Ho 2020（DDPM）](../../data/papers/ho-2020-ddpm.json)，再读 [Chung 2023（DPS）](../../data/papers/chung-2023-dps.json)；物理约束生成再看 Bastek 2025。
- 仿真驱动反演：先读 [Cranmer 等，PNAS 2020](../../data/papers/cranmer-2020-sbi.json)，仅在有实际似然自由推断需求时精读 APT。
- 神经算子补充架构：基础 FNO/DeepONet 学完后，从 MGNO 和 Galerkin Transformer 中**先选一个**。
- 世界模型与规划：先读 [PlaNet（ICML 2019）](../../data/papers/hafner-2019-planet.json)，需要策略学习时再看 Dreamer。
- 模型不可信与参数代偿：读 [Kennedy–O'Hagan（2001）](../../data/papers/kennedy-2001-model-discrepancy.json)，并与传统反问题可辨识性分析联系起来。

以上均为**非强制的学习入口**；Landmark 是学术地位，不等于必须现在阅读。

## 8. 仍明确留待后续建设

这仍不是完备百科：0D/1D/3D 冠脉模型及其多物理耦合、医学生理观测模型、严谨的逆问题不适定性谱系、系统 UQ 基准、真实临床介入决策验证、多模态患者特异数字孪生等仍需要持续核对与扩展。

**下一步：** 通过 v0.5 的小型真实图验证总体布局和语义连线，再建设完整交互式图谱。
