# Must-read policy · 每个方法只推荐 1–2 篇必读论文

## Purpose

The atlas is designed to reduce reading burden. **Curated** method nodes contain **1–2 must-read papers** forming a *minimum viable understanding set*. Other associated publications are optional research references, not required homework. Reading two papers cannot guarantee full mastery; it should give an informed starting point.

## Selection criteria

1. **Conceptual coverage:** explain the task, central mechanism, main assumptions and limits.
2. **Scholarly credibility:** prefer original peer-reviewed work or authoritative synthesis; distinguish conceptual origin from later improvements.
3. **Pedagogical clarity:** clear problem formulation, meaningful examples, understandable math.
4. **Research relevance:** help understand connections to forward models and inverse problems, especially ODE/PDE and hemodynamics.
5. **Marginal value:** do not select two overlapping papers when one landmark paper already makes the main idea clear.

**Default:** one foundational paper. Add a second explanatory, critical or theoretical counterpart *only if it materially helps*. For mature broad families, a high-quality review plus a canonical original may be more effective than two dense original articles.

## Enforced rules

- `method.status == "curated"` means **1 or 2** entries in `core_reading`.
- Every selected paper must have a record in data/papers, its bibliographic verification must be `verified`, and a paper→method relation must exist.
- Peer-reviewed papers are the default. For a preprint or uncertain publication, a core-reading entry must include `exception_reason` explaining why an exception is warranted.
- Every selection includes `why` (reason for inclusion) and `focus` (what to read/understand).
- `method.status == "draft"` can have **0** must-reads because its literature curation is unfinished. Draft is shown as incomplete, *not* curated.
- All other linked papers appear as **further reading** and do not silently become required.

## Separate notions

**Editorial selection** is not **personal reading progress**:

- `core_reading` = the editor's prioritized 1–2 papers for the method.
- `landmark` = historical significance of a publication (can be core or non-core).
- `verification_status` = checked publication metadata, not an assessment of technical correctness.
- User read/unread/deep-read = future personal layer, independent of the public scientific catalog.

A paper can be relevant to multiple methods and core to more than one. A cross-method reading itinerary should show it **once**, annotated with all covered methods.

## Changing the selections

If a better tutorial, survey, or decisive primary reference appears, revise the selection with a brief explanation in the PR. Keep a displaced but valuable paper attached to its methods as further reading. Never delete provenance merely to make the required reading list shorter.

A good minimum reading set should let the user answer: **What problem? What assumptions? What model/algorithm? Why is it different? What does it improve, and where does it fail? How can it serve inverse problems?**

**Stage-1 example:** PINN, DeepONet and FNO each have one checked original core paper. Classical inverse methods remain explicitly draft until their must-reads are selected in Phase 2.
