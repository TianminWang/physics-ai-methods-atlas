# Scholarly Corpus v1 — 全域检索记录与覆盖审计（启动记录）

> **状态：启动 / 发现性扫描，非完整检索** · **检索截止日期：2026-11-26** · **实际扫描日期：2026-11-26**
>
> [正式协议](../../docs/zh/CORPUS_FIRST_PROTOCOL_V1.md) | [47 条独立发现线索](discovery-leads-2026-11-26.json)
>
> **本记录仅证明“部分候选已在可核查的来源页面被发现”，不证明领域完成、论文已通过质量审查、重要文献已穷尽或方法知识体系已建立。**

## 1. 检索实施方式

本次首轮使用具备域名/关键词过滤的公开网页学术检索，重点限定在**可信出版社与正式会议论文集页面**（SIAM、Springer、Cambridge、JMLR、PMLR、ICML/NeurIPS/ICLR、Nature、Elsevier/MedIA、PubMed 索引等）。检索结果返回了官方来源的书目/摘要信息，并记录这些页面的永久链接与可见 DOI；未进行逐篇正式全文核验。

尚**没有**开展下列完整步骤：在各出版社/数据库的可复现搜索 API 执行完整布尔检索；记录每个数据库的全量命中数、逐步排除数；全文阅读与学术质量终审；所有文献的正向/反向引文链检索；Crossref/PubMed/出版方更正撤稿全量核查；正式主会与预印本版本统一；书籍版次/作者全面核对。不得称为已完成“系统综述”或 Corpus v1。

本次**未以旧61个方法/34家族为清单导向**，也未从旧 `research/b1/` 直接迁移26条探索记录。

## 2. 搜索式样例（本次实际使用，代表性而非全部）

| 检索方向 | 公开检索表达式（从本次操作选取） | 官方来源样例 |
| --- | --- | --- |
| M1/M2 数值反问题 | `site:epubs.siam.org inverse problems Tikhonov regularization adjoint nonlinear least squares parameter identification SIAM Review landmark` | [SIAM 反问题相关研究](https://epubs.siam.org/doi/10.1137/S0036144500358232) |
| M2 经典逆问题书 | `site:link.springer.com/book inverse problems theory regularization Engl Hanke Neubauer Chavent Kaipio Somersalo` | [Regularization of Inverse Problems](https://link.springer.com/book/9780792341574) |
| M3 SBI | `site:proceedings.mlr.press simulation-based inference neural posterior estimation likelihood-free 2019 2024` | [ICML 2024 Sequential Neural Score Estimation](https://proceedings.mlr.press/v235/sharrock24a.html) |
| M5 神经算子 | `site:jmlr.org papers neural operators inverse problems scientific machine learning uncertainty 2024 2025` | [JMLR Neural Operator](https://www.jmlr.org/papers/v24/21-1524.html) |
| M6 生成逆问题 | `site:openreview.net ICLR 2024 2025 2026 diffusion posterior sampling inverse problems generative priors flow matching` | [ICLR 2024 diffusion inverse problems](https://openreview.net/pdf?id=1YO4EE3SPB) |
| M7 决策 | `site:proceedings.mlr.press world models model based reinforcement learning planning MPC PlaNet Dreamer 2020 2024` | [ICML 2025 online world model](https://proceedings.mlr.press/v267/liu25p.html) |
| M8/A1 医学影像 | `site:sciencedirect.com/science/article "Medical Image Analysis" 2025 coronary artery segmentation deep learning coronary CTA` | [MedIA 2025 Topology-oriented coronary segmentation](https://www.sciencedirect.com/science/article/pii/S1361841525000131) |
| M8/A1 造影 | `site:pubmed.ncbi.nlm.nih.gov "IEEE Trans Med Imaging" coronary angiography reconstruction 2024 2025` | [IEEE TMI 2025 centerline reconstruction](https://pubmed.ncbi.nlm.nih.gov/40540370/) |
| A3/A5 QFR 临床 | `site:pubmed.ncbi.nlm.nih.gov quantitative flow ratio randomized trial FAVOR III China Lancet 2021 JACC 2022` | [Lancet FAVOR III China RCT](https://pubmed.ncbi.nlm.nih.gov/34742368/) |
| A3/A5 FFRct | `site:pubmed.ncbi.nlm.nih.gov CT derived fractional flow reserve trial multicenter diagnostic accuracy DISCOVER-FLOW NXT PLATFORM HeartFlow` | [JACC FUSION RCT 2026](https://pubmed.ncbi.nlm.nih.gov/42670732/) |
| A2/A6 医学数字孪生 | `site:nature.com/articles biomedical digital twin cardiovascular personalized hemodynamic physics-informed AI 2024 2025 2026` | [npj Digital Medicine 2026 patient-specific peripheral hemodynamics](https://www.nature.com/articles/s41746-026-03431-6) |
| 经典专著 | `site:link.springer.com/book "Numerical Optimization" Nocedal Wright second edition` | [Numerical Optimization 2e](https://link.springer.com/book/10.1007/978-0-387-40065-5) |

**限制：** 此处是“实际查询示例”，不是检索数据库导出的完整搜索历史；检索引擎对同一查询可能随时间变更排序/结果集合。继续完整检索前，应将各数据库搜索式版本化，并保存命中数、下载的可核验元数据/日期和筛选轨迹。

## 3. 首批跨领域发现的来源类型

本次 `discovery-leads-2026-11-26.json` 记录 **47 条来源页面线索，其中 38 篇论文与综述、9 本书**。每项均包含可访问来源 URL 和最初的 M/A 检索主题标签；共31条带 DOI（其他需要在全面书目校验中补齐）。

**所有47条均为 `academic_admission=pending`，且 `scientific_quality_review=not_performed`。** 标签分布只是观察到的代表性线索，不得将“每个方向有条目”理解成完成领域检索。

此次扫描横跨：
- 数值反问题、正则化、SIAM 数学与统计反问题教材；
- 统计推断/SBI、神经算子/Physics AI、生成式反问题；
- 世界模型与离线 RL；连续时间动力学模型；
- 冠脉 CCTA/DSA/IVUS 成像、几何重建、医学 AI 研究；
- FFR/QFR/虚拟规划相关的临床对照研究及患者特异数字孪生。

## 4. 覆盖审计初始矩阵（截至本次，仅“发现线索”，不作完成声明）

| 检索轴 | 初始覆盖现象 | 明显缺口及后续跨源检索重点 | 完成状态 |
| --- | --- | --- | --- |
| M1 ODE/PDE数值 | FVM与正向方法/数值相关来源 | FEM基础、数值ODE、ROM、稳定性误差、复杂耦合与血流边界 | **未完成** |
| M2 确定性反问题 | 正则化、优化、all-at-once、经典专著 | 适定性、可辨识性、adjoint、GN/LM、PDE约束优化、方法对照 | **未完成** |
| M3 统计反问题 | Bayesian 书、SBI/benchmark、变分生成反问题 | MCMC/HMC/NUTS/VI理论、先验/失配、UQ收敛、可信度 | **未完成** |
| M4 动力学/同化 | 变分/序贯同化教材、CDE、online world model | KF/EnKF/4DVar/系统辨识及原始理论源流 | **未完成** |
| M5 Physics AI | DeepONet、JMLR Neural Operator、物理代理 | PINN原始谱系与批评、FNO/PINO、可微模拟、算子泛化 | **未完成** |
| M6 生成式反问题 | DDPM、DDRM、RED-Diff、条件分布 | VAE/Flow/GAN的源流、score SDE、posterior correctness、拓展 | **未完成** |
| M7 world model/control | online world model、offline RL、continuous-time counterfactual | 最优控制/MPC经典、PlaNet/Dreamer谱系、安全约束RL、真实干预 | **未完成** |
| M8 视觉几何 | CCTA/DSA/IVUS重建分割及 MedIA/TMI | 传统几何、多视角、3D/4D、通用视觉基础模型、OCT | **未完成** |
| A1 医学影像 | CCTA/DSA/IVUS等线索 | OCT、跨设备/外部验证、定量几何误差、冠脉细分任务 | **未完成** |
| A2 医工物理模型 | 外周/脑血流数字孪生、血流边界相关 | 冠脉0D/1D/3D及多尺度、模型边界/生理参数、实验验证 | **未完成** |
| A3 FFR/QFR | QFR/FFRct临床RCT与诊断研究 | 功能学数学模型、具体观测算子、边界与导管测量误差 | **未完成** |
| A4 医学AI | 分割/患者代理数篇 | 外部验证、失效模式、可解释性、部署与公平性 | **未完成** |
| A5 虚拟干预 | QFR引导PCI / 临床治疗比较 | 真正虚拟支架/PCI规划仿真、干预反事实模型与前瞻性验证 | **未完成** |
| A6 医学数字孪生 | 循环系统综述、外周/脑血流患者特异模型 | 长期闭环同化、冠脉个体化更新、UQ及干预结局反馈 | **未完成** |

每项主题后续要完成：**至少两种独立发现途径、重要经典与现代代表研究、领域权威综述/专著（如适用）、去重与质量准入、引文补查及收敛性检查**，然后才可将状态改为“达到首版基线验收”。

## 5. 下一段真正的全域检索任务

按[协议](../../docs/zh/CORPUS_FIRST_PROTOCOL_V1.md)开展完整的跨数据库查询与版本化记录：为每个方法与应用大方向进一步细化子主题和布尔检索式；官方来源检索 + 权威综述/专著源流回溯；初步去重→全文/科学质量检查→引文补查与覆盖审计。旧数据不作为“已覆盖”证据。

**此时没有冻结 Corpus v1，更未开展正式知识归纳、节点迁移、关系纠偏或新版交互界面。**
