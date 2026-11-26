# v0.9 现有方法学知识结构审计

> **状态：第一轮结构审计已完成；本报告不是方法关系的学术终审。**
>
> 审计基准：`main` commit `5591a85784cb526dfd6ce8044e4a409c0eff8621`（2026-11-26 检查）。源数据不修改。数据计数可由 `python -m scripts.audit_v09 --output build/audit-v09.json` 重新计算。

## 1. 本次审计回答什么

v0.8 的不足不仅是 Graphviz 或交互细节，而是：整个方法体系同时包含**知识包含/分类关系**、**研究任务的功能关联**、**真实历史演化关系**，但我们曾主要依据最后一种关系来排列所有方法。

本轮要明确：

1. `method.*` 是否处于同一抽象层级？哪些其实是问题表述、宽泛方法族、算法、训练策略、模型架构、物理模型或软件框架？
2. `family.*` 是否表达稳定的分类逻辑？是否需要把主要功能角色与学术分类解耦？
3. `problem.*` 是否为研究任务/应用场景？它与“研究能力”（Capability）有何区别？
4. 现有边哪些是历史改进、分类、技术借用、学习依赖或应用功能关系？
5. 为什么点击一条有效的阶段→方法/家族映射后，有时主 DAG 没有目标节点高亮？

**审计不以“图谱必须连通”为目标，也不把无直接继承关系视为学术缺陷。**

## 2. 权威数据基线

| 项目 | 已检查数量 | 说明 |
|---|---:|---|
| 方法节点 `method.*` | 61 | 包括不同抽象层级 |
| 方法家族 `family.*` | 34 | 形成 6 个根家族的分类森林 |
| 具体研究问题 `problem.*` | 15 | 一般数学任务及领域应用混合 |
| 文献 `paper.*` / 专著 `book.*` | 58 / 12 | 原始数据继续沿用 |
| 全部有类型关系 | 530 | 18种关系类型 |
| 方法家族的成员关系 | 67 | 所有61个方法至少属于1个家族，6个方法有2个家族 |
| 家族→上层家族关系 | 29 | 多父类合法 |
| 方法→研究问题关系 | 93 | 所有15个研究问题至少有1条关联 |
| 研究阶段→方法/家族功能关系 | 55 | 部分是家族级而非方法级证据 |
| 真正的 `extends` + `combines` | **12 + 4 = 16** | 24个方法参与，37个方法尚未记录演进/融合边 |
| 方法分类 `specializes` | 16 | 不应与创新/演化混淆 |
| 由演进/融合边形成的非单节点连通分量 | 8 | 是现阶段文献整理与关系稀疏的结果 |

### 已经做对的部分

- 每个方法只有一个权威实体，实际允许多重家族归属。
- 不将 `start_here` 强制为1–2篇；Landmark 对应论文→方法贡献关系。
- 原始六项能力、三阶段投影、横向可信性关注点都有基础。
- 目前的所有问题节点都有 `addresses` 类型关系，并不是“数据全部未建”。

### 数量之外的质量问题

七个家族尚无直接方法成员，它们是用于容纳子家族的上层分类，因此**不能简单判断为七个错误或空白领域**。只有3个现有方法尚无直接 `addresses` 研究问题关系：Deep Galerkin、Deep Ritz、Physics-Informed DeepONet。这可能是映射补充工作，不必由此质疑其方法或文献地位。

## 3. 主要结构发现

### A. `method.*` 混合了不同本体层级

| 现有节点 | 暂定角色 | 为何不能简单并列 |
|---|---|---|
| Nonlinear Least Squares / Bayesian Inverse Problems | 数学问题表述 | 定义需要解的优化或推断问题，不等于具体求解器 |
| MCMC / Variational Inference / SBI | 宽泛方法家族 | 内部可以再分多个采样、密度估计或推断算法 |
| Gauss–Newton / LM / NUTS / CQL | 算法 | 有相对具体的更新规则和假设 |
| FNO / DeepONet / PINO / Galerkin Transformer | 神经架构或变体 | 强调模型表示与训练的结构 |
| Flow Matching / Physics-Informed Diffusion | 学习策略 | 主要贡献是训练路径或物理残差约束 |
| Windkessel / Structured-Tree Outflow | 物理模型 | 是机理表示或边界模型，不是优化器 |
| DiffTaichi | 软件/可微模拟基础设施 | 实现与程序求导机制需要分开理解 |

已针对全部61个方法提出**暂定的主语义类型**，见 [`audits/v09/method-kind-proposals.json`](../../audits/v09/method-kind-proposals.json)。这只是审计视图；**不能直接将宽泛方法节点删除或迁移成 family**，否则现有论文、边、书籍关联和稳定 ID 都可能受到影响。

### B. 方法家族的分类轴并不完全一致

34个家族中，有些按计算范式分类（如 Neural Operator、Bayesian Computation），有些按所解决任务分类（如 Learned Inverse），有些按物理领域分类（如 Hemodynamic Models）。它们自然会交叉。

**建议用多标签/多父类的分类 DAG，而不是强制做一棵严格互斥树。** 但更重要的是：方法家族不等于研究能力。方法家族回答“这是什么技术”，研究能力回答“它承担什么科学功能”。

### C. `problem.*` 与通用研究能力不应混在一起

当前15个问题中既有“ODE Parameter Inference、PDE Coefficient Inference”这类一般任务，也有“Coronary FFR Curve、Virtual PCI”这类特定应用，还包含长期数字孪生更新。

这些应当保留为**问题实例/场景（Problem / Scenario）**，并新设可复用的研究能力层（Capability）。例如：

- “后验推断”是通用研究能力，MCMC、VI、SBI 等可为其服务；
- “冠脉血流参数贝叶斯反演”是应用问题，可能需要观测建模、后验推断、参数化、辨识性与模型失配等多种能力。

目前草案列出19个研究能力：**Ⅰ建模6、Ⅱ反演8、Ⅲ预测干预更新5**。参见 [`audits/v09/capability-layer-proposal.json`](../../audits/v09/capability-layer-proposal.json)。

### D. 方法学的“包含、使用、融合、演进”不能用一种箭头代替

例如：
- `method.neural-operator` 是较广泛方法族；`method.fno` 可以是其中一个具体架构；
- `method.markov-chain-monte-carlo` 是较宽泛计算家族，`method.no-u-turn-sampler` 是经 HMC 路线形成的具体算法；
- Flow Matching 主要为**连续归一化流**提供一种训练方法，不一定应表示“所有 Normalizing Flow → Flow Matching”的历史继承。见 Lipman 等 ICLR 2023 原文；
- Song 等 ICLR 2021 以 SDE 框架统一了早期得分模型和扩散模型，简单的单线“DDPM → Score-SDE”可能掩盖其**概念统一**贡献；
- VAE 使用摊销式变分推断，`combines` 是否最精确需要对照原文的具体机制。

已列出10项待核验关系（包含优先级、原始 relation ID 和核查问题），见 [`audits/v09/relation-review-queue.json`](../../audits/v09/relation-review-queue.json)。**只是人工复核队列，不是关系错误的最终裁定。**

参考原文：Song et al. [ICLR 2021](https://mlanthology.org/iclr/2021/song2021iclr-scorebased/)、Lipman et al. [ICLR 2023](https://mlanthology.org/iclr/2023/lipman2023iclr-flow/)、Kingma & Welling [ICLR 2014](https://mlanthology.org/iclr/2014/kingma2014iclr-auto/)。

### E. v0.8 的“点击功能映射但无高亮”有明确的实现原因

v0.8 主 SVG **只渲染至少参与一个 `extends` 或 `combines` 的方法**（24个），但阶段映射投影覆盖**全部61个方法及其家族**。如贝叶斯模型失配校准和 SBI 有有效的反演功能记录，却可能不在主 SVG 上。

因此某些映射点击后会导致其他方法变暗，但没有任何可见目标节点被选中。这是**前端投影范围和功能索引之间的契约不一致**，而不是用户误操作，也不代表方法记录缺失。

建议未来规定：点击映射后必须返回至少一种显式结果：

- SVG 内的可见节点高亮与定位；
- 自动展开谱系待完善区并定位节点；
- 临时聚焦视图中呈现这些方法；
- 如果只存在家族级关联，则明确列出方法清单和证据级别，不能假装全部已直接验证。

## 4. 首轮结论

**不能将“完全连通的一张有向演化图”作为学术完整性的目标。** 稀疏继承关系可能是真实事实；本项目需要完整的是**科学问题→能力→方法组织及功能→方法演进→文献证据的可追溯链条**。

建议优先补齐理论和能力分类、节点类型、方法机制及关系证据，然后再推进可视化。**没有源论文支持的关系一律不主动添加。**

完整设计见 [《v0.9 本体与关系规范》](ONTOLOGY_V09.md)。后续整改顺序见 [《v0.9 后续工作队列》](REMEDIATION_V09.md)。
