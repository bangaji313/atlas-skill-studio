# Atlas visual direction

Brand source: the existing Atlas family SVGs. Paper `#F2EEE4`, ink `#132C3A`, muted `#506473`, and a darkened green accent `#166A58` for legible text/strokes. The original mint, lilac and blue marks identify the studios; they are decorative category cues, not the only source of meaning.

The README uses a 1600×720 editorial hero and a 1600×900 architecture diagram. The diagram has five conceptual nodes, six orthogonal connectors and no crossings. It shows source provenance, studio organization and host packaging; detailed skill lists belong in the catalog. The artwork is a product explanation, not a fabricated app screenshot.

Typography uses Georgia for display titles, Segoe UI/Arial for names and body copy, and a tracked sans-serif eyebrow. These are deliberate system-font fallbacks so the committed SVGs do not depend on a font CDN. The vectors include accessible titles/descriptions and explicit backgrounds for GitHub light/dark themes. PNG previews are supplied for export.

Method: Atlas Creative Production `diagram-design`, using the Architecture type, its connector/complexity rules, and the established Atlas brand rather than the shipped default palette. Regenerate vectors with `python tools/render_visuals.py`.
