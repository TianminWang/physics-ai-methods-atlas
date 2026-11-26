# 全域文献发现性扫描报告（2026-11-26）

> **状态：第一轮跨14个方向的“广度扫描”已完成；尚不满足“完整全域系统检索”的验收条件。**
>
> 基础：[Corpus-first v1 正式协议](../../docs/zh/CORPUS_FIRST_PROTOCOL_V1.md) · [质量准入政策](../../docs/zh/SOURCE_ADMISSION_POLICY.md) · [147条候选明细 JSON](discovery-leads-2026-11-26.json)
>
> **必须区分**：已经发现具有可核查来源页面的候选 ≠ 这些候选通过学术质量准入 ≠ 所有相关研究均被穷尽。本文不将本轮工作宣称为符合 PRISMA 等规范的已完成系统综述，也不将其宣称为 Scholarly Corpus v1 已冻结。

## 1. 边界与检索方式

- 研究时间截面：**2026-11-26（含）**，不设置历史起始日期；目前最早发现于1944年的经典论文，但不表示更早的相关研究不存在。
- 学术范围：M1 ODE/PDE/数值与降阶，M2 确定性反问题/优化，M3 概率反问题/UQ/SBI，M4 动力系统/数据同化，M5 Physics AI/神经算子，M6 生成模型/生成式反问题，M7 世界模型/控制/RL，M8 计算机视觉与几何；A1 医学影像，A2 医工血流模型，A3 FFR/QFR功能推断，A4 医学AI，A5 虚拟PCI与干预，A6 患者特异数字孪生。
- 方法：公开学术网页检索，使用专业关键词及 `site:` 限域，在SIAM、Cambridge、Springer、IEEE/MedIA、JMLR、NeurIPS、PMLR、ICLR/OpenReview、CVF、Nature、JACC、PubMed 等查找正式出版页面/会议记录，另以专著和综述辨认历史原论文，沿部分研究引文追踪。
- 来源清单只用于检索排序，非文献质量等级；不从旧 61 个方法/34 个家族进行配额式检索。
- 目前受限于检索接口与人工审查工作量，**并未**收集每种数据库搜索式的完整导出结果、命中/排除统计，没有跨数据库全量批量检索，也未逐篇完成全文技术审核与撤稿检查。

本次实际检索中有代表性的查询包括：

| 轴 | 查询表达式示例 | 发现的官方来源 |
|---|---|---|
| M1/M2 | `site:epubs.siam.org inverse problems Tikhonov regularization adjoint nonlinear least squares parameter identification SIAM Review landmark` | [SIAM Review：Statistical Regularization](https://epubs.siam.org/doi/10.1137/S0036144500358232) |
| M2/M3 | `site:epubs.siam.org inverse problems ill posedness identifiability Bayesian design 2023 2024 SIAM` | [SIAM Review：Bayesian inverse well-posedness](https://epubs.siam.org/doi/10.1137/23M1556435) |
| M3 | `site:proceedings.mlr.press simulation-based inference neural posterior estimation likelihood-free 2019 2024` | [PMLR：Sequential neural score](https://proceedings.mlr.press/v235/sharrock24a.html) |
| M4/M7 | `Qin Badgwell survey of industrial model predictive control technology Control Engineering Practice 2003 doi` | [Elsevier：MPC Survey](https://www.sciencedirect.com/science/article/pii/S0967066102001867) |
| M5 | `site:jmlr.org papers neural operators inverse problems scientific machine learning uncertainty 2024 2025` | [JMLR：Neural Operator](https://www.jmlr.org/papers/v24/21-1524.html) |
| M6 | `site:openreview.net ICLR 2024 2025 2026 diffusion posterior sampling inverse problems generative priors flow matching` | [ICLR：diffusion inverse](https://openreview.net/pdf?id=1YO4EE3SPB) |
| M7 | `site:proceedings.mlr.press world models model based reinforcement learning planning MPC PlaNet Dreamer 2020 2024` | [ICML：world models](https://proceedings.mlr.press/v267/liu25p.html) |
| M8/A1 | `site:sciencedirect.com/science/article "Medical Image Analysis" 2025 coronary artery segmentation deep learning coronary CTA` | [MedIA：coronary segmentation](https://www.sciencedirect.com/science/article/pii/S1361841525000131) |
| A1 | `site:pubmed.ncbi.nlm.nih.gov "IEEE Trans Med Imaging" coronary angiography reconstruction 2024 2025` | [IEEE TMI：3D centerline](https://pubmed.ncbi.nlm.nih.gov/40540370/) |
| A2 | `site:pubmed.ncbi.nlm.nih.gov structured tree arterial 1d blood flow model wave propagation Olufsen 1999 2000` | [AJP：structure-tree outlet](https://pubmed.ncbi.nlm.nih.gov/9887040/) |
| A3/A5 | `site:pubmed.ncbi.nlm.nih.gov quantitative flow ratio randomized trial FAVOR III China Lancet 2021 JACC 2022` | [Lancet：FAVOR III](https://pubmed.ncbi.nlm.nih.gov/34742368/) |
| A3/A5 | `site:pubmed.ncbi.nlm.nih.gov virtual stenting fractional flow reserve coronary intervention FAVOR virtual PCI computed FFR 2014 2023` | [JACC Imaging：virtual planner 2022](https://pubmed.ncbi.nlm.nih.gov/35798401/) |
| A6 | `site:nature.com/articles biomedical digital twin cardiovascular personalized hemodynamic physics-informed AI 2024 2025 2026` | [npj Digital Medicine：peripheral hemodynamic twin](https://www.nature.com/articles/s41746-026-03431-6) |
| 经典源流 | `Levenberg 1944 A Method for the Solution of Certain Non-Linear Problems in Least Squares Quarterly of Applied Mathematics DOI` | [AMS 原刊：Levenberg 1944](https://doi.org/10.1090/qam/10666) |

这些仅是代表查询；并非可供系统综述复跑的完整数据库导出检索式。不能把搜索引擎结果数量视为数据库完整命中数。

## 2. 发现性候选统计（仅候选，不是已准入）

| 指标 | 数值 |
|---|---:|
| 候选作品总数 | **147** |
| 论文与综述 | 121 |
| 学术专著/教材 | 26 |
| 附 DOI 候选 | 94 |
| 仍未获取/归一 DOI 候选 | 53 |
| 待质量审核 | **147/147** |
| 完成原文实质审核 | **0/147** |
| 完成撤稿/更正全面核验 | **0/147** |
| 唯一候选 ID | 147 |
| 重复标准化题名（当前精确匹配） | 0 |
| 重复已记录 DOI | 0 |

说明：单一文章可能同时具有多种 M/A 标签，下表按关联统计而非互斥分类；没有A标签的纯方法研究并非遗漏。

| 方法学标签 | 被标记的候选数 | 应用标签 | 被标记的候选数 |
|---|---:|---|---:|
| M1 数值与正向计算 | 49 | A1 医学影像 | 26 |
| M2 确定性反问题/优化 | 34 | A2 医工物理模型 | 19 |
| M3 统计反问题/UQ | 29 | A3 冠脉功能推断 | 27 |
| M4 动力系统/同化 | 27 | A4 医学 AI | 16 |
| M5 Physics AI | 21 | A5 虚拟干预 | 21 |
| M6 生成模型/反问题 | 14 | A6 医学数字孪生 | 6 |
| M7 世界模型/控制 | 17 | | |
| M8 视觉/几何 | 23 | | |

| 年代 | 发现候选数 |
|---|---:|
| 1940s–1980s 合计 | 6 |
| 1990s | 7 |
| 2000s | 21 |
| 2010s | 35 |
| 2020s（截至2026-11-26） | 78 |

**明显的时间与主题偏斜**：现代文献远多于早期经典，A6 医学数字孪生的高质量候选仍偏少；这些是下一步全文质量审核及引文溯源前必须修正的抽样不足，不能用“14个标签皆非空”充当覆盖已完整的证据。

## 3. 质量判断严格保持未准入

每个候选均留有 `academic_admission=pending`、`scientific_quality_review=not_performed`、`retraction_and_correction_check=not_performed`，还未独立核查所有会议 Track、期刊最终版、预印本与正式版本关系、图书 ISBN/版次、临床结果外推限制。因此：

- 同一研究可能在原论文/期刊扩展/预印本存在版本重复；当前只做 DOI 与题名规范化的**初步库内去重**，不能宣称跨库完整去重。
- 高质量综述用于知识结构追溯、经典书籍用于定理/理论覆盖；尚未据此确定任何方法节点、原始贡献或历史谱系。
- 某些来源涉及初步试验、回顾性患者数据或多中心RCT，其**证据成熟度尚待正式审核**，不能混成统一“临床已验证”标签。
- 当前正式可发布的合格 Corpus 规模是 **0（尚未完成准入）**，不是147。

## 4. 未达到 Corpus v1 冻结的原因

与 [正式协议第6节](../../docs/zh/CORPUS_FIRST_PROTOCOL_V1.md) 逐项核对：

| 正式验收条件 | 目前证据与缺口 | 结果 |
|---|---|---|
| M1–M8、A1–A6 各主题均有充分检索覆盖 | 仅完成各轴的首次定向网页发现，部分子学科与年代不足 | **未通过** |
| 各主题至少两种独立发现渠道、可复现检索 | 有官方来源、综述/专著和部分引用，但未按全部子方向规范化记录数据库检索式及全量命中 | **未通过** |
| 全部候选统一去重、论文出版与质量准入 | 仅库内 DOI/题名去重、部分书目复核；无全体审核 | **未通过** |
| 分主题、年代、研究类型、证据类型完整覆盖矩阵 | 已建立粗粒度标签/年代表，没有全量排除与来源类型质控 | **未通过** |
| 多轮独立引文补查趋于饱和 | 尚未进行足以评估遗漏率的多轮前后向引用追踪 | **未通过** |
| 版本化冻结 `Scholarly Corpus v1` | 不满足任何正式冻结条件 | **未通过** |

因此，不得把本轮文件命名或介绍成“完整文献库”或“已完成全域系统检索”，不得据此启动正式本体建设。

## 5. 后续必须补齐的检索与质量工作

要完成用户要求的“在全域内先完整检索，再建立知识体系”，还须在可访问的全文/专业索引环境里进行：

1. 对各子主题设计**可重跑**的关键词与布尔式；至少跨官方出版数据库和独立引文/书目索引查询，保存筛选条件、命中/去重/排除数量。
2. 从权威综述/经典专著继续向前追原始工作，向后追重要理论、算法改进和独立证据；修正1970–1990及成熟数学方法覆盖不足。
3. 结合医学工程特征补足：冠脉CFD/患者特异0D–3D多尺度、OCT/IVUS/DSA、多中心影像验证、虚拟支架反事实预测与随机临床决策证据；同样覆盖一般医学AI的原创工程方法。
4. 统一 DOI/arXiv/ISBN 和版本，逐篇检查科学内容、同行评议类型、撤稿/更正，并依据[质量准入政策](../../docs/zh/SOURCE_ADMISSION_POLICY.md)形成正式 **准入/待核查/不准入** 记录。
5. 开展覆盖矩阵审计与独立重复检索；如果仍频繁找到关键缺失研究，不能宣布搜索趋于饱和。

**只有全域来源检索和质量审核达标、冻结 Corpus v1 后才开始统一知识体系与交互界面。** 现阶段没有对 `data/`、Schema、旧方法关系或 viewer 进行学术迁移。
