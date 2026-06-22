# jokoivi-highcharts-skill

A standalone, local devtooling skill for working with the [Highcharts](https://www.highcharts.com/) Options API in environments without MCP (Model Context Protocol) access.

## Pain Principles (Why We Built This)

- **Eradicate API Hallucination**: LLMs frequently hallucinate deprecated StackOverflow configurations. We rely on a deterministic local ground truth (AST JSON dictionary) before drafting code.
- **Context Window Efficiency**: The Highcharts TS repository is massive (7MB+). We condense this into a flat, scannable JSON schema to save token usage while maintaining perfect accuracy.
- **Enforce Enterprise & A11y Guardrails**: Ensure all generated charts comply with corporate standards and WCAG 2.2 accessibility rules by default.
- **Complete Local Autonomy**: Operate reliably in restricted corporate environments without requiring external cloud MCP server validation or network calls.

## Architecture Overview

We replaced external dependencies and brittle markdown files with an autonomous AST parser ecosystem:

1. **AST Dictionary (`highcharts_api_map.json`)**: A highly flattened, scannable map of 3,800+ Highcharts interfaces containing types and optionality. **All deprecated properties and empty interfaces have been aggressively pruned** from this dictionary to physically prevent LLM hallucination. Generated locally from the official `.d.ts` file.
2. **Local Helper Tools (`.agents/skills/jokoivi-highcharts-skill/scripts/`)**:
   - `generate_api_map.js`: Uses the TS Compiler API to parse `highcharts.d.ts` into the flat JSON map.
   - `grep_ts_definitions.py`: Fast JSON retrieval of exact interface schemas.
   - `deprecation_checker.py`: Validates drafts recursively against the AST dictionary to flag deprecated keys.
   - `extract_sample_config.py`: Pulls verified examples directly from the official `samples/` directory.
   - `search_local_docs.py`: Greps the official markdown documentation (`docs/`) for specific features or concepts.
3. **Modular Pathways (`.agents/skills/jokoivi-highcharts-skill/pathways/`)**:
   Segmented guidelines loaded on-demand for A11y baselines, data shapers, and dashboard layouts to save context.

*(For detailed tool testing and usage commands, see [`test-commands.md`](test-commands.md)).*

## Usage

When assigned a Highcharts task:
1. **Never guess API properties**. Always query `grep_ts_definitions.py` to get the strict types.
2. **Draft the configuration** based on the strict interface definitions.
3. **Apply the A11y Baseline** loaded from `pathways/a11y_baseline.md`.
4. **Validate the draft** using `deprecation_checker.py`.
5. Output the surgical patch or full typed `Highcharts.Options` object.

*(Note: During skill development only, MCPs like `highcharts-developer` and `highcharts-export` are enabled to assist with validation and knowledge gaps, but these will not be available in the final deployed environment.)*

## Backlog / Improvements

- [ ] **Future API Updates**: Create an automated script to download the latest `highcharts.d.ts` via npm/CDN, rebuild the `highcharts_api_map.json`, and immediately delete the source files to maintain the lightweight footprint.
- [ ] Write additional `data_shaper` helpers for specialized chart types (e.g., Gantt or Network graphs).
- [ ] Incorporate unit tests for the AST dictionary parser to detect breaking changes in major Highcharts version bumps.
- [ ] Improve `extract_sample_config.py` to cleanly handle complex, multi-file demo structures.
- [ ] Add support for validating specific `@highcharts/dashboards` layouts within the deprecation checker.
