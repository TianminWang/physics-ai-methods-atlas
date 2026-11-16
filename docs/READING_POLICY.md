# Reading and landmark policy · 里程碑文献与优先阅读建议

## The user's research goal

**The full Atlas should be comprehensive; the user's reading burden should not be.** A method node can cite many papers, including original contributions, reviews, significant extensions, theory and applications. A reader should be able to grasp the main mechanism by prioritizing a small, carefully selected starting set rather than reading the entire bibliography.

**Default editorial aim: around 1–2 particularly useful sources per method, not an enforced limit.** A node may have zero, one, two or more starting references. A textbook chapter can be a better starting point for classical methods than an obscure original historical article.

## Separate two distinct judgments

### 1. Landmark — contextual methodological contribution

A paper's role and historical importance are captured **on its paper→method relationship**:

- `type`: `introduces`, `analyzes`, `applies`, `surveys`, or `compares`;
- optional `significance`: `landmark`, `representative`, or `supporting`;
- a `landmark` relationship must give a nonempty `significance_reason`.

There is **no global `paper.landmark: true/false`**. The same paper can be foundational for one method and simply a useful application for another. Not every method has a single literal origin paper, especially historical tools such as Gauss–Newton, adjoints or the Windkessel model. **Do not infer originality merely from publication date.**

### 2. Start here — a personalized reading-efficiency recommendation

A method may have ordered `start_here` entries with:
- `reference_id` — a unique `paper.*` or `book.*` identifier;
- `why` — why this source efficiently communicates the method;
- `focus` — the technical parts worth prioritizing;
- optional `locator` — book chapter or paper section, when checked;
- optional `exception_reason` — why a non-peer-reviewed paper deserves special priority.

Unlike academic Landmark status, a highly readable tutorial may be recommended **before** an original landmark. This is deliberately a guide, not homework.

## Integrity checks, not reading quotas

The validator enforces only matters that would damage the reliability of an actual recommendation:
- a source reference must exist and not be duplicated within the same method;
- a starting **paper** must have checked bibliographic metadata and a paper→method relationship;
- a starting **book** must have a book→method `covers` relationship;
- non-peer-reviewed starting papers require a documented exception;
- landmark contribution roles must be correctly typed and justified.

It **does not** require any recommended starting source for `curated` nodes, and **does not limit recommendations to 1–2 items**. `curated` means method definition, major claims and sources have received editorial attention, independently of reading recommendations.

## What makes a good recommendation?

For a specific method, ask:

1. Does the source establish the **problem, assumptions and mechanism**?
2. Does it explain what is *new relative to prior approaches*?
3. Can the user understand the main mathematics and limitations from selected sections?
4. Is it authoritative and bibliographically verified?
5. Is a second paper substantially complementary, or merely repetitive?

A well-chosen first paper, occasionally accompanied by a synthesis or critical analysis, is often enough to orient further research. For textbook-based classic methods, choose **relevant chapters rather than the whole monograph**.

## Personal progress and scholarly facts are different

Reading status (unread, skimmed, studied, reproduced), editorial start-order and Landmark significance are three separate concepts. Do not mutate a paper's Landmark role simply because the user has read it, and do not force complete reading of every landmark in a method family.

A paper can appear under multiple nodes; a future personalized reading view should **deduplicate that paper** and show all the topics it covers. The graph should make learning more efficient, not create extra work.
