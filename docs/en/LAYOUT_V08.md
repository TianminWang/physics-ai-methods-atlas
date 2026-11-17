# v0.8 · Full-width, evidence-first method DAG navigation

The three-phase research axis and canonical scholarly records remain unchanged. This release is a visual/interaction upgrade, **not a new taxonomy or an attempt to connect unrelated methods**.

## Why some methods are in a separate shelf

The atlas currently contains more methods than documented `extends` / `combines` evolution relationships. The main canvas shows **only methods participating in at least one documented evolution/fusion link**, with Graphviz optimizing their layered layout and component packing.

All other methods remain **in the same database**, searchable and available in the collapsible **lineage-awaiting-curation shelf**. Those methods can have other taxonomy links, landmark papers and suggested readings. This does not imply that they lack scholarly importance.

Taxonomic `specializes` and contrasting links can be overlaid but do not determine evolution ranks. Disconnected components remain legitimate, with explicit navigation rather than fabricated links.

## Visual language

- **Node color:** traditional numerical/optimization, statistical/probabilistic, machine/deep learning, or physics–data hybrid display paradigm; multiple actual family memberships are preserved.
- **Evolution-edge color:** the documented primary affected phase—I blue (modeling), II purple (inference), III teal (prediction/intervention/update), or neutral when unspecified.
- **Edge style:** solid = extends, dashed = combines, neutral dotted = classification, not historical improvement.

## Interactive features

The DAG uses **the full page width** and a viewport-height-adaptive canvas. A side drawer opens on method/edge selection and can be closed or pinned/docked. Fullscreen viewing, a navigable minimap, clickable component navigation, upstream/downstream lineage focus, search across **all** canonical methods, stage-based highlighting, and bilingual presentation are available.

Functional family-level relevance is still carefully distinguished from method-specific empirical evidence. Edge details retain innovation, bottleneck, tradeoffs and supporting papers. Landmark and Start Here citations remain contextual and advisory.

## Build / review

From the latest successful **Validate atlas data** GitHub Actions run, download `atlas-fullwidth-dag-v08` and open the extracted `index.html` offline.

Developers can build with:

```bash
python -m pip install -r requirements-dev.txt
python -m scripts.build_v08 --site build/viewer-v08
```

Graphviz and Chinese font support are needed only at **build time**. The portable result embeds all source-derived data.

v0.8 is an interactive layout prototype, not yet the final GitHub Pages site. Its semantic graph and original publication records remain in the authoritative Atlas.
