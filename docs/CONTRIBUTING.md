# Contributing · 维护与更新规范

## 1. 先找节点，再看论文

每次增加论文前先搜索是否已有同一论文（DOI、arXiv、标题）；同一篇论文只建立一次权威记录。明确论文是提出、理论分析、应用、综述还是比较某个方法；Landmark 必须相对于具体方法关系给出理由。优先阅读建议（`start_here`）是可选的，没有固定数量限制。

## 2. 新方法与家族不应等同于新论文

- 新节点应该代表可独立理解、复用的数学或算法机制，而不是一篇论文、一个数据集或一种临床应用。
- 先选择是否属于现有方法家族（`member_of_family`）；同一方法可以属于多个家族，但只能保留一份 `method.*` 记录。
- 若真的存在可追溯的前驱或融合来源，才使用 `extends` / `combines`，提供具体创新、原先的技术瓶颈、证据论文和适用边界。
- 如果只是一般/特殊化，则使用 `specializes`；学习依赖使用 `depends_on`；不要把研究时间先后当作继承证据。
- 未完成系统检索的家族使用 `coverage_status=planned`，不填造假的代表论文。

## 3. 研究主轴与方法是多对多功能关系

新增家族或方法以后，检查它是否与当前六个环节有关。只有在能够解释具体功能时才加入 `stage.* → family.*` 或 `stage.* → method.*` 的 `uses_method`，用中英文 `role` 清楚说明。

例如“反演阶段使用 FNO 作为正向代理”不同于“FNO 本身直接输出参数后验”。避免笼统归类误导用户。

## 4. 演进边的文字和颜色

- `extends` / `combines` 记录 `innovation_detail`, `innovation_detail_zh`, `bottleneck`, `bottleneck_zh` 和 `evidence_paper_ids`。
- 可以用 `stage_ids` 标注多个确有关联的环节；明确主要研究动机时再设置 `primary_stage_id`，它必须属于 `stage_ids`。
- 配色由主轴环节的 `color` 派生，**不得在关系文件中随意设置另一个颜色**。
- `tradeoff` 记录复杂性、计算成本或适用边界；“改进”不表示所有指标都更好。
- `uses_method` 的 `evidence_scope` 指明它是概念可用、已有学术支持、特定应用验证还是暂时性的候选研究设想。

## 5. 中文/英文维护

统一科学事实只写入一份权威实体或关系 JSON。新的 `stage`、`family`、`concern` 节点具有 `name`/`name_zh` 与相应中英文说明。旧方法的中文名通过 `locales/zh-CN.json` 提供，后续可逐步迁到记录的双语字段。

GitHub 首页 `README.md` 为中文，`README.en.md` 为英文；统一架构说明为 `docs/zh/UNIFIED_GRAPH.md` 和 `docs/en/UNIFIED_GRAPH.md`。不维护两份互相独立的图谱数据。

## 6. 本地或 PR 自动检查

```bash
python -m pip install -r requirements-dev.txt
python -m scripts.validate
python -m pytest -q
python -m scripts.export_graph
python -m scripts.export_unified --lang zh --output build/unified-zh.json
python -m scripts.export_unified --lang en --output build/unified-en.json
```

所有数据源中引用的 ID 必须存在。家族分类 DAG 和方法演进 DAG 不允许循环；主轴反馈循环则合法。**校验工具能够保证结构一致，不代表自动验证了论文的科学结论。** 对新的历史前驱关系和临床应用有效性，必须人工依据原文判断。

完整架构：[中文版](zh/UNIFIED_GRAPH.md) · [English](en/UNIFIED_GRAPH.md)。
