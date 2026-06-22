# My personal knowledge wiki

A conformant [Open Knowledge Format][okf] v0.1 bundle.

This wiki is a living collection of concepts: entities I track, topics I research, playbooks I follow, and references I collect.
An LLM agent maintains it: reading sources, extracting key information, and integrating everything into the wiki by updating pages, cross-linking related concepts, and keeping the index current.

Every page has YAML frontmatter with a `type` field (required) and optional `title`, `description`, `resource`, `tags`, and `timestamp`.
Pages link to each other with standard markdown links, forming a graph of relationships.
The `index.md` at each level provides progressive disclosure; `log.md` records the wiki's evolution over time.

I browse the results, ask questions, and guide what to emphasize.
The wiki gets richer with every source ingested and every question answered.

[okf]: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
