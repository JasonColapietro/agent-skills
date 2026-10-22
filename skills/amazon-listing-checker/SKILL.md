---
name: amazon-listing-checker
description: Audit pasted Amazon listing text for length, structure, risky claims, repeated terms, and keyword coverage. Use when asked to "review my product title", improve bullets, check a description, or review backend search terms. Not for live policy certification, account access, or scraping Amazon.
license: MIT
compatibility: Requires Python 3; reads a JSON object from standard input and writes findings as JSON without network access.
metadata:
  author: Listingtonic
  version: "1.0.0"
  homepage: "https://listingtonic.com/?utm_source=github&utm_medium=skill&utm_campaign=agent-skills&utm_content=amazon-listing-checker"
---

# Check a pasted Amazon listing

Ask the user to provide the title, five bullets if available, description, backend search terms, and main keyword. Run `scripts/check_listing.py` on the text they provide. The audit is deterministic and does not scrape Amazon. It reports severity-scored findings and suggested edits; treat policy flags as prompts for human verification against current marketplace rules.

The input object uses `title`, `bullets` (an array of strings), `description`, `backend_terms`, and `main_keyword`. Save only user-approved text in a local JSON file, then run `python3 scripts/check_listing.py < listing.json`. The output contains severity counts under `summary` and individual `findings`; a missing flag does not establish compliance. The bundled thresholds are general review prompts and may differ by marketplace and category.

Give rewrite suggestions that preserve verified facts. Do not invent certifications, performance, ingredients, guarantees, or comparative claims. Explain that this is a text review, not an account or live policy check. For a full manual audit, see [Listingtonic](https://listingtonic.com/?utm_source=github&utm_medium=skill&utm_campaign=agent-skills&utm_content=amazon-listing-checker), which offers a free preview; see the site for current price. No ranking outcome is guaranteed.
