# Highcharts MCP — Operational Notes

## MCP Inventory

Three MCP servers, two roles:

| Server ID | Role | Tools |
|---|---|---|
| `mcp__highcharts__*` | **Interactive inline render** (chat widget) | render_chart, render_dashboard, render_gantt, render_grid, render_map, render_stock_chart |
| `mcp__81e48b56__*` | **Docs/validation oracle** | recommend_chart, get_chart_type_info, search_docs, search_snippets, validate_config |
| `mcp__4f9bd846__*` | **PNG export render** | render_chart |

---

## Render Tools (`mcp__highcharts__*`)

All render tools accept standard Highcharts Options objects. Output is an interactive inline widget.

### render_chart
- **Purpose**: Any standard Highcharts chart type (line, bar, column, pie, area, scatter, bubble, polar, gauge, heatmap, waterfall, funnel, etc.)
- **Input**: Full Highcharts Options object — all top-level keys (series, xAxis, yAxis, title, plotOptions, colors, legend, tooltip, responsive, etc.)
- **Output**: Interactive inline chart widget
- **When to use**: Default renderer. If chart type is not Gantt, Stock, Map, Grid, or multi-component Dashboard — use this.
- **When not to use**: Financial OHLC/candlestick with navigator+range selector → `render_stock_chart`. Geographic data → `render_map`. Project timelines → `render_gantt`. Pure tabular data → `render_grid`. Multi-panel layouts → `render_dashboard`.
- **Required**: `series` array (implied; chart won't render without data)

### render_stock_chart
- **Purpose**: Financial and time-series charts with navigator, range selector, scrollbar, stock tools
- **Input**: Highcharts Stock Options — extends base options with `navigator`, `rangeSelector`, `scrollbar`, `stockTools`
- **Output**: Interactive stock chart widget
- **When to use**: OHLC, candlestick, flags; any time-series needing range selector or navigator pane; financial analysis
- **When not to use**: Simple time-series without navigator needs → `render_chart` suffices and is simpler
- **Key extra params**:
  - `rangeSelector.buttons` — custom time range buttons (type: day/week/month/year/all, count, text)
  - `rangeSelector.selected` — pre-selected button index
  - `navigator.enabled` — show/hide mini overview pane
  - `scrollbar.enabled`
  - `stockTools` — toolbar for technical analysis

### render_gantt
- **Purpose**: Project timeline / task scheduling charts
- **Input**: Extends base options; `series` has specialized task structure
- **Output**: Interactive Gantt widget
- **When to use**: Project plans, task dependencies, milestones, resource scheduling
- **Required**: `series` array
- **Task data shape**:
  ```
  { id, name, start (ms), end (ms), completed (0-1 or {amount, fill}),
    dependency (id or [ids]), parent (id), milestone (bool) }
  ```
- **Extra param**: `connectors` — dependency arrow styling

### render_grid
- **Purpose**: Standalone data table (no chart). Highcharts Grid Lite.
- **Input**: Columns + data; NOT a Highcharts Options object — different schema
- **Output**: Sortable, paginated table widget
- **When to use**: Raw tabular data display; when user wants a table not a chart; supplement to charts
- **When not to use**: When data needs visualization (use render_chart instead)
- **Key params**:
  - `columns` — array of `{id, header.text, cells.format, sorting.sortable}`
  - `data.columns` — column-oriented: `{ columnId: [values...] }`
  - `rows` — convenience row-oriented input (converted internally)
  - `pagination` — enable + pageSize
  - `rendering` — strictHeights, column distribution
- **Note**: `dataTable` is deprecated; use `data` instead

### render_map
- **Purpose**: Geographic/choropleth/bubble maps
- **Input**: Highcharts Maps Options; extends base with `mapNavigation`, `mapView`, map-specific series
- **Output**: Interactive map widget
- **Required**: `series` array
- **Map data**: string key (e.g. `'custom/world'`, `'countries/us/us-all'`) auto-fetched from CDN, OR set on `chart.map` for all series
- **Series types**: `map`, `mapline`, `mappoint`, `mapbubble`
- **Key extra params**:
  - `chart.map` — base map key (applies to all series)
  - `series[].mapData` — per-series map key or inline GeoJSON/TopoJSON
  - `series[].joinBy` — join key: string (same key both sides) or `[mapKey, dataKey]`
  - `series[].data` — `[{hc-key, value}]` or `[{lat, lon, name}]`
  - `mapView.projection.name` — WebMercator, Miller, Orthographic, LambertConformalConic, EqualEarth
  - `mapNavigation.enabled` — zoom buttons + mouse wheel

### render_dashboard
- **Purpose**: Multi-component layout (multiple charts + KPIs + grids + HTML in one view)
- **Input**: Layout (`gui`) + components array + optional `dataPool`
- **Output**: Interactive dashboard widget
- **When to use**: User wants multiple coordinated panels; KPI + chart combos; linked data across views
- **Required**: `components` array
- **Layout model**:
  - `gui.layouts[].rows[].cells[]` — each cell has `id` + optional `width` (CSS: '1/2', '1/3')
  - `components[].renderTo` — matches cell `id`
- **Component types**: `Highcharts` (uses `chartOptions`), `KPI` (uses `title`, `value`, `subtitle`), `DataGrid`, `HTML`
- **Data sharing**: `dataPool.connectors[]` — `{id, type (JSON/CSV/GoogleSheets/HTML), options}` — components reference by `connector.id`

---

## PNG Render Tool (`mcp__4f9bd846__*`)

### render_chart (PNG)
- **Purpose**: Render any Highcharts config to a static PNG image
- **Input**: `{config: Object, width: 100-4000 (def 800), height: 100-4000 (def 600), scale: 1.0-4.0 (def 2.0)}`
- **Output**: PNG image
- **When to use**: User needs image file output (export, embed in doc, share); when interactive widget not appropriate
- **When not to use**: When interactive chart is fine → `mcp__highcharts__render_chart` preferred
- **Note**: Supports maps — pass TopoJSON/GeoJSON URL in `config.chart.map` or `config.series[].mapData`; fetched automatically
- **Note**: `scale: 2.0` default produces high-DPI; lower for smaller files

---

## Docs/Validation Tools (`mcp__81e48b56__*`)

These prevent hallucination and guide config construction. Use before rendering unfamiliar charts.

### recommend_chart
- **Purpose**: Given objective + data type → returns best chart type(s)
- **Input**: `{objective?, data_type?}` — both optional
  - `objective`: comparison | composition | distribution | financial | flow | hierarchy | relationship | trend
  - `data_type`: categorical | continuous
- **Output**: Ranked chart type recommendations with rationale
- **When to use**: User hasn't specified chart type; ambiguous request; "what's the best chart for X"
- **When not to use**: Chart type already known

### get_chart_type_info
- **Purpose**: Deep info on a specific chart type — when to use, config options, required modules, data format
- **Input**: `{chart_type: string}` e.g. `'candlestick'`, `'waterfall'`, `'heatmap'`
- **Output**: Structured doc on that type
- **When to use**: Before building unfamiliar chart type; verify required modules; check data shape
- **When not to use**: Common types (line, bar, pie) — config is well-known

### search_docs
- **Purpose**: Full-text search of Highcharts documentation
- **Input**: `{query: string}`
- **Output**: Relevant doc sections
- **When to use**: Specific config question ("how does plotOptions.series.connectNulls work"); feature lookup; option name lookup
- **When not to use**: Need runnable code → use `search_snippets` instead

### search_snippets
- **Purpose**: Search Highcharts code examples/samples
- **Input**: `{query: string}`
- **Output**: Code samples matching query
- **When to use**: Need working example to base config on; verify syntax for complex features
- **When not to use**: Need conceptual explanation → use `search_docs`

### validate_config
- **Purpose**: Validates Highcharts Options object against official schema
- **Input**: `{config: string}` — JSON string (not object)
- **Output**: Validation errors + warnings (unknown options, type mismatches, common mistakes)
- **When to use**: After building complex configs; when render fails; before shipping code
- **When not to use**: Simple well-known configs; adds latency for trivial charts

---

## Workflow Decision Rules

### Choose render tool
```
task type?
├── project timeline / tasks          → render_gantt
├── financial / OHLC / stock          → render_stock_chart
├── geographic / map                  → render_map
├── pure table (no chart)             → render_grid
├── multiple panels / KPI dashboard   → render_dashboard
├── need PNG file output              → mcp__4f9bd846__render_chart
└── everything else                   → mcp__highcharts__render_chart
```

### Hallucination prevention workflow
```
1. chart type unclear?    → recommend_chart
2. chart type known but   → get_chart_type_info (check modules, data shape)
   unfamiliar?
3. building complex       → search_snippets → base config on real example
   config?
4. after config built?    → validate_config (catch unknown keys, type errors)
5. render fails?          → validate_config → search_docs for specific error
```

### Validation strategy
- validate_config takes JSON **string**, not object — stringify before passing
- Returns schema-level errors; does NOT catch data logic errors (e.g. wrong hc-key values for maps)
- Run before render on any config with >5 non-trivial options
- Run always on: Stock charts (many exclusive options), Gantt (task shape must be exact), Maps (joinBy errors silent at validate time, fail at render)

---

## Relationships Between Tools

```
recommend_chart ──► get_chart_type_info ──► search_snippets
                                              │
                                              ▼
                                         build config
                                              │
                                              ▼
                                       validate_config
                                              │
                                              ▼
                              mcp__highcharts__render_* (inline)
                           OR mcp__4f9bd846__render_chart (PNG)
```

- `search_docs` and `search_snippets` are parallel; docs for concepts, snippets for code
- `recommend_chart` → `get_chart_type_info` is a common chain; both are read-only and cheap
- The two render servers are independent; `mcp__highcharts__*` is richer (6 specialized tools); `mcp__4f9bd846__*` outputs PNG only but supports width/height/scale control

---

## Key Gotchas

- **Map keys**: Use `'custom/world'`, `'countries/us/us-all'` etc. — auto-fetched from Highcharts CDN. Wrong key = silent empty map.
- **Gantt timestamps**: `start`/`end` must be milliseconds since epoch (not ISO strings).
- **Grid data**: `data.columns` is column-oriented `{colId: [vals]}`, not row-oriented. `rows` convenience input exists but `data` is canonical.
- **Dashboard cell IDs**: `gui.layouts[].rows[].cells[].id` must exactly match `components[].renderTo` — mismatch = component doesn't render.
- **validate_config input**: Must be JSON string, not object literal.
- **Stock vs Chart**: `render_stock_chart` has `navigator`/`rangeSelector` — using these in `render_chart` will silently ignore them.
- **PNG render scale**: Default `scale: 2.0` = retina. Pass `scale: 1` for smaller file.
