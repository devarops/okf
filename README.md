# okf

My personal knowledge wiki — a conformant Open Knowledge Format v0.1 bundle.

An LLM agent reads source documents, extracts key information, and
builds this wiki.  I browse the results, ask questions, and guide
what to emphasize.

Concept pages live under `bundle/`.  Source documents go in `raw/`.

Run the conformance checker to verify the wiki follows the format:

    python check_okf.py

Coming soon:
- Auto-generated `index.md` from frontmatter
- Enrichment agent for new sources
- Static HTML visualizer for the wiki graph
