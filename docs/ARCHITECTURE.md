# Architecture · 数据与知识图谱架构

## 1. Three layers, one source of truth

1. **Canonical data:** individual JSON documents in data/{areas,methods,papers,books,problems,relations}.
2. **Validation and projections:** JSON Schema + semantic checks; a reconstructable, normalized graph snapshot.
3. **Views (not authoritative):** GitHub README overview, future default method-evolution forest, research-task/digital-twin workflow, and optional learning-dependency view.

Do **not** keep a separate hand-curated graph for each view. Do **not** duplicate a paper's metadata within every method record. The overall knowledge graph may contain cycles; only designated taxonomic / learning subgraphs must be acyclic.

## 2. Entity types

| Kind | Stable ID example | Purpose |
|---|---|---|
| area | area.inverse-problems | A broad navigation category, **not** method ancestry |
| method | method.fno | A distinct reusable method, family or methodological framework |
| paper | paper.li-2021-fno | Bibliographic evidence, reusable across multiple methods |
| book | book.physics-based-deep-learning | Textbook/monograph, covering multiple nodes or areas |
| problem | problem.coronary-parameter-inference | An inverse, inference or digital-twin research task |
| relation | relation.fno--belongs-to--physics-ai | A directed, semantically typed graph link |

Every record is a **separate file** under data/<plural>/<id suffix>.json. IDs, not labels or filenames, are the stable references. Rename display labels freely; avoid changing stable IDs after references exist. v0.1 uses schema_version "1.0.0".

Method records hold the central idea, innovation, limitations, required background and an ordered **core_reading** with at most two papers. Other papers are attached by relations. Books use `covers` relations with a chapter/section locator when known.

## 3. Typed relations (direction is significant)

| Type | Allowed direction | Meaning |
|---|---|---|
| belongs_to | method → area | Navigation membership; multiple areas allowed |
| subarea_of | area → area | Area hierarchy |
| specializes | specific method → general method | Conceptual specialization, not temporal improvement |
| extends | successor → predecessor | Evidence-backed methodological extension, **not** universal superiority |
| combines | composite method → constituent method | Evidence-backed method fusion |
| depends_on | method → prerequisite method | Learning prerequisite, **not** a historical influence claim |
| contrasts_with | method → method | Meaningful comparison; viewer may draw as undirected |
| addresses | method → problem | Can contribute to the task given suitable assumptions |
| introduces | paper → method | Introduces or establishes the named method |
| analyzes | paper → method | Theoretical, error, limitation or failure analysis |
| applies | paper → method | Application / empirical test |
| surveys | paper → method | Survey / tutorial |
| compares | paper → method | Comparative study |
| covers | book → method/area/problem | Educational coverage; optional `locator` for section |

Every relation stores a human-readable `claim`; `evidence_paper_ids` may cite supporting papers. `extends` and `combines` require at least one evidence paper. Bibliographic dates alone do not establish causal inheritance.

**Example:** method.fno → area.physics-ai is `belongs_to`; paper.li-2021-fno → method.fno is `introduces`. Cross-domain membership is never silently reinterpreted as method ancestry.

## 4. Directed acyclic projections

The validator separately checks:
- area taxonomy (`subarea_of`);
- method taxonomy (`specializes`);
- method evolution (`extends` + `combines`, together);
- learning prerequisites (`depends_on`).

Other edge types can create legitimate loops in the overall graph. A method may have multiple ancestors, components or applications. Every relationship has its own explicit semantics.

## 5. Reading rules and metadata normalization

~~~json
{
  "id": "method.fno",
  "status": "curated",
  "core_reading": [
    {
      "paper_id": "paper.li-2021-fno",
      "why": "Original definition of the Fourier neural-operator mechanism",
      "focus": "Fourier layers and PDE experiments"
    }
  ]
}
~~~

This is only an excerpt; the complete source is data/methods/fno.json. `status=curated` requires **1–2** verified, linked papers, while draft records can have none. Additional related papers use paper→method relationships and do not add to the must-read count.

User-specific reading status ("read", "to-read") is **independent** of editorial must-read status. If a paper is core to more than one method, the viewer should deduplicate it in an aggregated reading route.

## 6. Technical boundary

- JSON Schema validates fields, required types, enums, identifier shape and the two-paper cap.
- scripts/validate.py checks **cross-file** reference integrity, relation endpoint pairs, duplicate IDs/DOIs, paper-method links, evidence, area membership, curated selection and DAG cycles.
- scripts/export_graph.py produces deterministic graph JSON and refuses invalid data. Exported files live in ignored build/.
- The future UI will consume this JSON export and must never turn into another independently maintained source of truth.

Schema-breaking changes require versioned migration. Adding papers and ordinary method nodes should not require code changes.

## 7. Future interactive views

**Default A — method-evolution forest:** select areas and distinguish taxonomy, evidence-backed lineage and cross-links. Click nodes for core papers, further reading, book coverage and limitations.

**Switchable B — research-problem view:** start from coronary parameter inference / model calibration / state assimilation / counterfactual PCI tasks, and follow `addresses` links to available methods.

**Optional C — learning dependencies:** follow `depends_on` edges plus basic `background_topics` to determine what to learn next without a prerequisite of completing a whole mathematics curriculum.

The viewer should visibly distinguish curated vs draft nodes, verified vs provisional bibliography, and descriptive method links vs performance rankings.
