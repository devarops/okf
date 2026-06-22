# LLM Wiki in the Open Knowledge Format

This is my personal LLM Wiki.
It conforms to the Open Knowledge Format (OKF) v0.1 specification.

The content is entirely generated and maintained by LLM agents.
An LLM agent reads source documents, extracts key information, and builds this wiki.
I browse the results and ask questions, but I don't directly edit the wiki.

Concept pages live under `bundle/`.
Source documents go in `raw/`.

Run the validator to verify the wiki follows the format:

```shell
make validate
```
