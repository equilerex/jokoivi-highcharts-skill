# jokoivi-highcharts-skill

LLM skill for working with the Highcharts Options API.

## Scope

- Generate typed `Highcharts.Options` configs from scratch
- Patch existing configs surgically (changed keys only, never full regeneration)
- Select appropriate chart type for a given data shape and objective
- Audit configs against WCAG 2.2 accessibility requirements
- Look up API options, format strings, and chart-type specifics via MCP
- Convert REST API JSON to Highcharts `series[]` format (via `data_to_series.py`)

## Out of scope

- Component/wrapper code — rendering is the app's concern
- Signal or state management wiring
- Build tooling, module imports, or bundler config

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Entry point — routing, gotchas, a11y baseline, MCP tool list |
| `patterns.md` | Verified `Highcharts.Options` configs by chart type (lazy-loaded) |
| `a11y.md` | WCAG 2.2 criteria, contrast table, audit checklist (lazy-loaded) |

## Companion tool

`.agents/tools/data_to_series.py` — CLI converter: REST JSON array → Highcharts `series[]`.

```
python data_to_series.py --input data.json --type column --x month --y revenue
python data_to_series.py --input data.json --type line --x date --y value --datetime
python data_to_series.py --input data.json --type pie --name segment --y revenue
python data_to_series.py --input data.json --type grouped-column --x quarter --y revenue --group region
```
