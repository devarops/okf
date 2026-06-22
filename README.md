# LLM Wiki in the Open Knowledge Format

This is my personal [LLM Wiki][llm-wiki].
It conforms to the [Open Knowledge Format][okf-blog] (OKF) v0.1 [specification][okf-spec].

The content is entirely generated and maintained by LLM agents.
An LLM agent reads source documents, extracts key information, and builds this wiki.
I browse the results and ask questions, but I don't directly edit the wiki.

Concept pages live under `bundle/`.
Source documents go in `raw/`.

Run the validator to verify the wiki follows the format:

```shell
make validate
```

[llm-wiki]: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
[okf-blog]: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
[okf-spec]: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
