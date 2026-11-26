# 学术论文与专著质量准入政策 v1.0

> **状态：正式生效（2026-11-26）** · Physics AI Methods Atlas
>
> 本文由原《文献与专著质量准入标准 v1.0（待确认稿）》精简定稿。它是**学术来源质量门槛**，不是知识图谱本体设计规范、论文评分系统，也不是 v0.9-A/B/C 开发阶段的定义。

## 1. 核心原则：文献先行，知识体系随后生长

**先检索和审核研究与专著，筛掉低质量、不可靠或缺乏实际学术价值的来源；再从通过准入的来源中识别理论、方法、算法、模型、研究能力及其关系，逐步建设知识图谱。**

- 不先画出一个必须完整或连通的图谱，再为每个既定节点寻找文献“填空”。
- 不因为某个研究方向缺少文献就降低准入标准；暂时缺乏可靠依据的概念和关系可以保留为待核查线索，但不得作为已证实知识呈现。
- 学术来源、研究问题可以引导检索主题，但不应预先强制规定最终方法节点、家族数目和演化边。
- 期刊/会议的声誉用于**检索排序**，不代替对单篇研究的评价。不同学科遵循各自的发表传统：机器学习重视正式顶会；数学、数值分析、反问题重视经典专业期刊和专著；临床应用重视研究设计及外部/前瞻性验证。
- 学术可信性与教学易读性是不同问题。Landmark（方法学地位）和 Start Here（优先学习入口）由后续知识整理决定，**不是本政策的准入等级**。

本政策不实行 A/B/C 文献质量评分。**只判断“准入 / 待核查 / 不准入”**：通过准入者可作为正式知识体系的来源；待核查者仅用于探索，不能作为正式结论的唯一依据；不准入者不进入正式来源集合。

## 2. 单篇研究的最低准入要求

论文或正式研究报告需逐篇核查以下条件，不能以“发表在 V1”代替：

| 维度 | 准入要求 |
| --- | --- |
| 书目及版本真实 | 确认题名、作者、年份、来源、DOI/arXiv ID（适用时）、正式出版/录用类别及被审查的具体版本；不能验证身份则暂缓 |
| 学术审查可靠 | 原则上经过可信的同行评议；经典原始成果和极少数高影响预印本按第 4 节特别审核 |
| 主题有明确价值 | 与 Atlas 所研究的数学/物理/计算方法、反问题、数据驱动模型、推断、预测、控制、数字孪生或相关临床/物理验证存在可解释的连接 |
| 研究有实质内容 | 提供可辨认的理论、方法、算法、模型、严格比较、独立验证、可靠的否定结果或高质量系统综合；不收录明显浅层复用与缺乏知识增量的重复应用 |
| 结论可信且有边界 | 数学推理、物理假设、数值实验、统计设计、数据划分及比较设置没有明显重大缺陷；论文主张与实际证据相称 |
| 发表状态可接受 | 检查撤稿、重要更正、表达关切及关键争议；严重影响核心结论且未消除的问题不得通过 |

**“实质内容”不等同于必须发明新算法。** 严谨的误差分析、失败模式研究、经典理论证明、临床外部验证、方法比较和高水平综述也可能是重要学术来源。相反，引用很多、所在期刊著名，不代表文章自动合格。

对于超出当前评审能力的技术主张，记录“不确定、需专家或原文深入复核”；不以自信但未经核查的摘要代替通过准入。

## 3. 期刊、会议及专题来源：开放的优先检索清单

下面沿用原草案的 **V1 核心优先 / V2 高质量专题**，只表示检索顺序与专题相关性。**V2 不是低质量等级，未列出也不自动被拒绝；任何来源都必须逐篇审核。** 列表为维护起点，并非全面排名。

| 领域 | V1 核心优先来源（示例） | V2 高质量专题来源（示例） |
| --- | --- | --- |
| 综合、交叉与权威综述 | Nature、Science、Nature Machine Intelligence、Nature Biomedical Engineering、Nature Computational Science、Nature Methods、Nature Medicine、Nature Physics、PRL、PRX、Science Translational Medicine、The Lancet Digital Health；Nature Reviews Methods Primers / Bioengineering / Cardiology / Physics | Nature Communications、Science Advances、PNAS、npj Digital Medicine、Communications Medicine / Physics；按具体论文内容和学科判断 |
| 机器学习、统计学习、世界模型、RL | NeurIPS、ICML、ICLR；COLT、AISTATS、UAI；JMLR、IEEE TPAMI、IJCV | TMLR、AAAI、IJCAI、L4DC、KDD、IEEE TNNLS 等；正式论文与非归档 Workshop 必须区别 |
| 计算机视觉、几何及可微图形学 | CVPR、ICCV、ECCV；**SIGGRAPH 正式研究论文及 ACM TOG（适用图形学/几何主题）** | MIDL、ISBI 以及与研究问题高度相关的专业期刊和会议 |
| 经典数值分析、PDE、优化、反问题 | SIAM Journal on Numerical Analysis、SIAM Journal on Scientific Computing、Numerische Mathematik、Mathematics of Computation、Foundations of Computational Mathematics、Acta Numerica、Inverse Problems、SIAM Journal on Imaging Sciences、SIAM Journal on Optimization、SIAM Journal on Control and Optimization、Mathematical Programming、SIAM Review | SIAM Journal on Mathematical Analysis / Applied Mathematics、Inverse Problems and Imaging、Journal of Scientific Computing、Journal of Inverse and Ill-Posed Problems、Optimization Methods and Software、Computational Optimization and Applications 等 |
| 统计、贝叶斯推断与 UQ | JASA、Biometrika、Annals of Statistics、Bayesian Analysis、SIAM/ASA Journal on Uncertainty Quantification | Statistics and Computing、Annals of Applied Statistics、Multiscale Modeling & Simulation、SIAM Journal on Applied Dynamical Systems 等 |
| 科学计算、流体与 Physics AI | Journal of Computational Physics（JCP）、Computer Methods in Applied Mechanics and Engineering（CMAME）、International Journal for Numerical Methods in Engineering、Journal of Fluid Mechanics | Physics of Fluids、Physical Review E、Computational Mechanics、Computer Physics Communications、Machine Learning: Science and Technology、Communications in Computational Physics 等 |
| 医学图像、医学 AI、生物医学工程 | IEEE TMI、Medical Image Analysis、MICCAI 正式论文、IPMI、IEEE TBME、Radiology、Nature Biomedical Engineering | Radiology: AI、MIDL、IEEE ISBI、Medical Physics、Physics in Medicine & Biology、JBHI、Computer Methods and Programs in Biomedicine、Computers in Biology and Medicine 等 |
| 冠脉血流动力学、FFR/QFR、PCI、临床证据 | JACC、Circulation、European Heart Journal、JACC: Cardiovascular Imaging / Interventions、Circulation: Cardiovascular Imaging / Interventions、European Heart Journal – Cardiovascular Imaging、EuroIntervention、Cardiovascular Research | Journal of Cardiovascular Computed Tomography、European Heart Journal – Digital Health、The International Journal of Cardiovascular Imaging、Journal of Biomechanics、Journal of Biomechanical Engineering、Biomechanics and Modeling in Mechanobiology、Annals of Biomedical Engineering 等 |

说明：

1. **不要跨学科比较影响因子。** SIAM、Numerische Mathematik、Inverse Problems、JCP、CMAME 等的专业价值，不应因指标规模不同而被低估。
2. 检查具体会议 **Track / Proceedings / 录用形式**。顶会 Workshop、poster 展示、PMLR 收录等标签，本身不保证与主会归档论文同等级的审稿。
3. 综述提供理论综合、源流与学习入口；不能因发表在权威综述期刊就自动视作某算法的原始提出论文。
4. **Nature Reviews Computing 计划于 2027 年 1 月创刊**；截至本版定稿时不作为已有成熟文献来源列入上述清单，未来根据实际发表情况增补。
5. V1/V2 随领域发展按需复核，建议至少每年检查一次；对清单外的可信研究实行开放提名，而非封闭白名单。

## 4. 特别准入：经典文献、预印本与会议版本

**经典原始成果：** 对公认的理论/方法源头，不以今天的刊物影响因子、发表年代或现代审稿标准否决。须通过原始文献、权威专著、历史研究或后续独立工作的交叉核查确认出处、贡献与适用范围。

**正式发表版本：** 如果 arXiv 工作已有正式期刊/主会版本，优先依据正式版本核验；保留可追溯的预印本关系，不把同一研究的版本当作多个独立成果。

**尚未同行评议的预印本：** 默认“待核查”，**不得仅凭新颖或热门进入正式学术依据**。只有在技术结论经深入检查、已有多个独立团队复用/验证/扩展且在领域内形成充分认可时，才允许特殊准入；必须注明非同行评议状态、独立支持来源、审核理由和复核条件。无引用数机械门槛，不因社交媒体热度破例。

**Workshop、技术报告、代码仓库：** 可作为线索、复现材料或技术补充；若没有相当于正式学术审查的证据，不能独立充当重要方法起源或理论正确性的权威来源。历史经典的特殊情况单独审查。

## 5. 专著、教材与综述性参考书

专著与论文采用同样的**准入 / 待核查 / 不准入**原则，但按以下维度逐本判断：

- **作者专业性与准确性：** 作者的研究经历、理论论证、引文和技术内容可靠。
- **编辑/评审与学术认可：** 优先 SIAM、AMS、Cambridge、Oxford、Princeton、MIT Press、Springer 权威数学系列、CRC/Chapman & Hall、Wiley、Academic Press 等经专业审查的学术书籍；不是出版社白名单。
- **系统性与独立价值：** 能系统阐明理论、推导、算法、假设、局限或重要方法谱系；对已有书籍提供有意义的互补。
- **教学与可检索性：** 适合用作方法解释或学习入口；尽量记录具体章节/版本，而非要求通读整本书。
- **独立核验：** 可参考 MathSciNet、zbMATH、权威大学课程、领域综述和独立学术采用情况。

**开放在线教材/持续更新的学术书籍不自动排除。** 若作者专业性、技术可靠性和独立认可充分，可以通过准入；引用时必须记录所参考的版本、章节或访问日期，不能把在线教材自动等同于已经完成外部同行评议的定版专著。

## 6. 医学/物理应用的证据边界

在冠脉 FFR/QFR、虚拟 PCI、患者特异数字孪生等场景，特别区分：

1. **方法可行性：** 理想化模型、合成数据、体外实验；
2. **患者数据验证：** 回顾性影像/生理观测及其适当比较；
3. **外部验证：** 独立中心、设备或群体；
4. **临床决策或结局证据：** 前瞻性研究、随机试验或实际决策影响评价。

上述是**证据类型**，不是以期刊声誉换算的质量分数。高质量数值方法论文能够证明算法价值，但不能仅由模拟推断临床有效性；高水平临床论文也不因此自动被认定为一种新算法的源头。区分研究范围与结论范围。

## 7. 最小审核记录与长期维护

每份候选来源至少保留：可核查的书目身份与版本、来源/审稿类型、与 Atlas 的关联、核心学术贡献、明显局限或争议、**准入决定及理由**、审核日期；特殊准入附独立证据和复核理由。可先用可读的 Markdown 审核表或侧表实现，不要求立即把所有字段塞入现有论文 JSON。

在由来源提炼知识时，另行核实“论文到底支持哪一个概念或关系”：

- 方法节点必须具有可追溯的真实学术依据；
- **重要方法演进边**需回到原始研究核对机制、方向、技术改变及原文位置；
- 单纯更晚发表、使用相同技术关键词或有类似应用，不能推出学术继承；
- 可靠的综述、专著可以提供解释与交叉核证，但不能凭综述本身虚构方法发明史。

至少在正式版本替换、撤稿或重大更正出现时复核；可借助 Crossmark、出版社状态页面和独立研究进行确认。

## 8. 旧数据库的地位

截至 v0.9-A，现有 **58 篇论文、12 本专著、61 个方法、34 个方法家族**主要来自早期数据结构和可视化原型探索。**现有的 `verification_status: verified` 只表示此前的书目核验状态，不表示通过本版学术质量准入。**

- 保留旧数据与稳定 ID，避免破坏历史原型；**不自动“祖父条款”准入**。
- 新一轮先独立筛选高质量原始来源，再依据证据重建或修订概念和关系。
- 合格的旧来源可以复用；不合格/未核查者不应自动成为新正式知识体系的证据。
- 不承诺保留旧的节点数量、家族边界、19 项 Capability 或原有 530 条关系。
- 正式知识数据与历史示例数据的区分、迁移和 UI 标记，依后续[证据驱动重建路线](EVIDENCE_FIRST_REBUILD.md)实施；**本政策落地本身不修改学术数据或浏览器代码**。

## 参考准则与官方说明

- [DORA：San Francisco Declaration on Research Assessment](https://sfdora.org/read/) — 不以期刊层级指标替代单篇研究评价。
- [TMLR Editorial Policies](https://www.jmlr.org/tmlr/editorial-policies.html) — 区分技术正确性、证据强度与主观影响力。
- [Nature Reviews Computing — Journal Information](https://www.nature.com/nrcomput/journal-information) — 2027 年 1 月创刊信息。
- [COPE：Publication ethics guidance](https://publicationethics.org/guidance) — 更正、撤稿与出版伦理问题的参考。
