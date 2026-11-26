# B1 首轮检索记录 · 2026-11-26 · 批次 01

> **性质：初步学术发现 / metadata seed。不是完成的系统综述、正式入选文献库或完整的学术质量审核。**
>
> 结构化候选数据见 [candidates-2026-11-26-01.json](candidates-2026-11-26-01.json)。每条来源均标注 `admission_status=pending`、`review_level=bibliographic_discovery_only`。只有完成 B2 准入才允许转入正式 Corpus。

## 1. 本轮目的与范围

首次验证[已确认的双轴检索方案](../../docs/zh/EXECUTION_PLAN_V09.md)是否能够检索到：

- 传统数学/数值反问题的原始研究或权威专著；
- 现代 Physics AI、生成模型、world model、视觉方法的正式论文；
- 医学影像、血流模型、FFR/QFR、虚拟支架与循环系统数字孪生的可信生医工/临床研究；
- 交叉来源，例如神经算子 + 血流动力学 + 贝叶斯参数反演。

本轮未限制所有历史年代，也未要求旧 61 个方法各自获得一篇候选。期刊/顶会 V1/V2 只引导搜索；旧数据库样本只有少量可在本轮中与新发现重合。

## 2. 检索来源与实际检索示例

| 通道 | 实际使用的部分检索表达式（节选） | 结果 |
| --- | --- | --- |
| 经典数理 | `site:cambridge.org/core/journals/acta-numerica "Inverse problems: A Bayesian perspective" Stuart 2010` | Acta Numerica 2010 官方书目与摘要 |
| 理论及数值专著 | `site:cambridge.org/core/books "Finite Volume Methods for Hyperbolic Problems" LeVeque` | Cambridge 图书页及版次 |
| 最小二乘/统计反问题专著 | `site:link.springer.com/book "Nonlinear Least Squares for Inverse Problems" Chavent`; `site:link.springer.com/book "Statistical and Computational Inverse Problems" Kaipio Somersalo` | Springer 书目、章节与版本 |
| 数据同化专著 | `site:epubs.siam.org "Data Assimilation" Asch Bocquet Nodet` | SIAM 书籍简介与章节（检索词的精确拼写可在后续搜索协议规范化） |
| 现代方法 | `site:jmlr.org neural operator learning maps between function spaces survey Kovachki 2023`; `site:openreview.net "Flow Matching for Generative Modeling" Lipman` | JMLR 论文和 ICLR 正式论文 |
| 生成/物理模拟 | `site:papers.nips.cc "Denoising Diffusion Probabilistic Models" Ho Jain Abbeel`; `site:proceedings.mlr.press "Learning to Simulate Complex Physics with Graph Networks"` | NeurIPS / ICML 正式记录 |
| 医学 AI | `site:nature.com "nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation"`; `site:link.springer.com "U-Net: Convolutional Networks for Biomedical Image Segmentation"` | Nature Methods / MICCAI 官方记录 |
| 冠脉诊断/治疗 | `site:pubmed.ncbi.nlm.nih.gov fractional flow reserve versus angiography guiding percutaneous coronary intervention Tonino 2009`; `site:pubmed.ncbi.nlm.nih.gov virtual stenting computational coronary FFR planning` | FFR 临床证据、virtual stenting 验证 |
| QFR 临床来源 | `site:pubmed.ncbi.nlm.nih.gov coronary quantitative flow ratio diagnostic accuracy FAVOR II China 2018 Xu` | 找到 Xu 等 JACC 2017；**实际书目年份按正式来源纠正，而不是直接采用查询年份** |
| 交叉领域 | `"Physics-Informed Neural Operators for Parameter Inference in Multi-vessel Cardiovascular Networks" "Annals of Biomedical Engineering"`; `"A new method to compute the blood flow equations using the physics-informed neural operator" "Journal of Computational Physics"` | 2026 / 2024 方法 × 血流模型与参数推断工作 |

**检索日期：2026-11-26。** 主要依赖出版社/会议官方页面、PMLR、ICLR 站点、Nature、Cambridge、SIAM、JACC 及 PubMed 书目信息。本轮没有自动抓取所有搜索结果、检索结果总数或逐条排除日志；不能据此宣称 PRISMA 式系统性文献综述或领域覆盖完整。

## 3. 可追溯的主要外部入口（书目证据）

- [Cambridge · Stuart (2010), *Acta Numerica*](https://doi.org/10.1017/S0962492910000061)
- [SIAM · Cotter et al. (2010), Bayesian inverse PDE approximation](https://doi.org/10.1137/090770734)
- [JMLR · Kovachki et al. (2023), Neural Operator](https://www.jmlr.org/papers/v24/21-1524.html)
- [Nature Machine Intelligence · Lu et al. (2021), DeepONet](https://doi.org/10.1038/s42256-021-00302-5)
- [NeurIPS · Ho et al. (2020), DDPM](https://papers.nips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html)
- [ICLR · Lipman et al. (2023), Flow Matching](https://openreview.net/pdf?id=PqvMRDCJT9t)
- [PMLR · Sanchez-Gonzalez et al. (2020), graph-based physics simulation](https://proceedings.mlr.press/v119/sanchez-gonzalez20a.html)
- [MICCAI · Ronneberger et al. (2015), U-Net](https://doi.org/10.1007/978-3-319-24574-4_28)
- [Nature Methods · Isensee et al. (2021), nnU-Net](https://doi.org/10.1038/s41592-020-01008-z)
- [PubMed · Olufsen (1999), structured-tree outlets](https://pubmed.ncbi.nlm.nih.gov/9887040/)
- [JACC · Xu et al. (2017), online QFR diagnostic accuracy](https://doi.org/10.1016/j.jacc.2017.10.035)
- [JACC Interventions · Kim et al. (2014), virtual stenting](https://pubmed.ncbi.nlm.nih.gov/24332418/)
- [JCP · Li et al. (2024), physics-informed neural operator blood flow](https://doi.org/10.1016/j.jcp.2024.113380)
- [Annals of Biomedical Engineering · Ryan et al. (2026), PINO + Bayesian haemodynamics](https://doi.org/10.1007/s10439-026-04219-1)
- [Nature Reviews Bioengineering · Wu et al. (2026), circulatory digital twins](https://doi.org/10.1038/s44222-026-00427-5)
- [Cambridge · LeVeque, *Finite Volume Methods for Hyperbolic Problems*](https://doi.org/10.1017/CBO9780511791253)
- [Springer · Chavent, *Nonlinear Least Squares for Inverse Problems*](https://doi.org/10.1007/978-90-481-2785-6)
- [Springer · Kaipio & Somersalo, *Statistical and Computational Inverse Problems*](https://doi.org/10.1007/b138659)
- [SIAM · Asch et al., *Data Assimilation*](https://doi.org/10.1137/1.9781611974546)

## 4. 本批数据统计与局限

- **26 条候选：22 篇论文、4 本专著**。这些条目是小批人工选取的书目发现结果，不代表入选质量级别。
- 方法学检索标签 **M1–M8 均至少有候选**；应用标签 **A1–A6 也均有候选**；但各子领域明显不均衡。
- 跨轴示例：`P022` (M2/M3/M5 + A2/A3/A4)；`P021` (M1/M5 + A2/A4)。示例仅表示**研究主题**交叉，不等于图谱里已证明历史方法继承。
- 当前仍缺乏充分覆盖：严谨最优化、系统辨识、经典 MCMC/非线性可辨识性谱系、SBI、最优控制/MPC、offline RL、更多扩散逆问题方法、冠脉 CCTA/DSA/OCT/IVUS 的图像几何/定量验证，以及外部临床验证。**这些是下次 B1 检索重点**。
- 部分记录没有 DOI，但包含会议官方永久页或 PubMed URL；B2 可进一步核对正式 DOI、Track、版本与更正记录。
- 书目层初查**不等于**全文数学/实验质量审查；没有批准任何论文或专著加入正式权威 `data/`，也没有新建方法学节点/演进边。

## 5. 下一小批推进建议

沿两个轴补齐上述未覆盖的类别，尤其深入检索 **严谨反问题/优化与不确定性** 和 **医学影像至冠脉功能/干预的闭环工作**。同时对已发现来源开始去重和正式版本校核，再启动 B2 的逐项质量审核。不得因为某类候选数量少而放宽准入政策。

旧的 58 篇论文/12 本专著目前未完成与本批26条的 ID/DOI 去重对照，也没有在本轮进行全库 B2 审核；这项工作应作为下一小批优先任务。
