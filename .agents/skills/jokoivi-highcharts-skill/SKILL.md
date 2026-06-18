---
name: jokoivi-highcharts-skill
description: >
  Use this skill whenever the user is working with Highcharts in any capacity — generating chart
  configs, patching existing ones, picking chart types, auditing for accessibility or WCAG 2.2,
  debugging options, asking about the API, or building dashboards. Covers Highcharts.Options
  TypeScript configs for Angular apps (custom wrapper, no official highcharts-angular package),
  data shaping from REST APIs, and enterprise best practices. Trigger on: highcharts, chart config,
  Highcharts.Options, series, xAxis, yAxis, plotOptions, tooltip, dataLabels, accessibility, wcag,
  visualization, drilldown, dashboard, pie, donut, bar, column, line, spline, chart type.
---

## Core contract

- Output typed `Highcharts.Options` only — no component code
- Patch intent → surgical edit only, never regenerate full config
- New config → always apply a11y baseline (below)
- Signal values slot into `series[].data`, `xAxis.categories` — never model signal wiring

## Intent → action

| Intent | Action |
|---|---|
| Generate new config | Load `patterns.md` → build typed config → apply a11y baseline |
| Patch existing config | Edit only changed keys. Return diff block, not full object |
| API question | `search_docs` MCP |
| Chart type selection | `recommend_chart` MCP |
| Find example | `search_snippets` MCP |
| Validate config | `validate_config` MCP — ignore known false-positives (see below) |
| A11y audit | Load `a11y.md` → run checklist |
| Data shaping from REST | Suggest `.agents/tools/data_to_series.py` |

## A11y baseline (always on new configs)

```typescript
accessibility: {
  enabled: true,
  description: '', // caller fills: what chart shows + key insight
  point: { valueDescriptionFormat: '{index}. {point.category}: {point.y}.' },
},
credits: { enabled: false },
```

For production/audited configs: load `a11y.md`.

## Known validate_config false-positives — ignore

- `Unknown option 'series.N.data'`
- `Unknown option 'series.N.innerSize'`
- `Unknown option 'plotOptions.*.stacking'`
- `Unknown option 'series.N.dashStyle'`

## Core gotchas

| Wrong | Correct |
|---|---|
| `plotOptions.pie.innerSize` | `series[0].innerSize` |
| `legend.showInLegend` | `plotOptions.pie.showInLegend: true` |
| Drilldown without category axis | `xAxis: { type: 'category' }` required |
| `stackLabels` on `plotOptions` | `yAxis.stackLabels.enabled: true` |
| Datetime data as ISO strings | Must be `[ms_timestamp, value]` pairs |
| `opposite: true` on series | Goes on `yAxis` object, not series |

## Reference files

Load on demand — do not load both upfront:

| File | Load when |
|---|---|
| `patterns.md` | Generating new config, need verified example, dashboard layout |
| `a11y.md` | A11y audit, WCAG question, production config review |

## MCP tools

| Tool | When |
|---|---|
| `mcp__81e48b56-8f89-4796-bd68-fd779008e422__recommend_chart` | Type selection |
| `mcp__81e48b56-8f89-4796-bd68-fd779008e422__get_chart_type_info` | Type-specific API detail |
| `mcp__81e48b56-8f89-4796-bd68-fd779008e422__search_docs` | Option lookup |
| `mcp__81e48b56-8f89-4796-bd68-fd779008e422__search_snippets` | Code examples |
| `mcp__81e48b56-8f89-4796-bd68-fd779008e422__validate_config` | Config validation (JSON string input) |

Do not call render tools — app renders.
