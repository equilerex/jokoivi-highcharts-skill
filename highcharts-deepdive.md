# Highcharts Enterprise Patterns — Deep-Dive Reference

All patterns in this document are verified unless explicitly marked `// UNVERIFIED`.
Verification = rendered successfully via `mcp__highcharts__render_chart` or noted tool.

---

## 1. Donut / Pie Charts

### Pattern
Donut: `pie` type with `innerSize`. Used for composition (parts-of-whole).
Pie: same without `innerSize`. Donuts preferred in enterprise dashboards — easier to read at small sizes, center space usable for KPI label.

### Verified configuration — Standard Donut

```typescript
{
  chart: { type: 'pie' },
  title: { text: 'Revenue by Segment' },
  series: [{
    name: 'Revenue',
    innerSize: '60%',          // string percent OR pixel number
    data: [
      { name: 'Enterprise', y: 45 },
      { name: 'Mid-Market', y: 30 },
      { name: 'SMB',        y: 15 },
      { name: 'Other',      y: 10 },
    ],
  }],
  plotOptions: {
    pie: {
      dataLabels: {
        enabled: true,
        format: '{point.name}: {point.percentage:.1f}%',
      },
      showInLegend: true,
      startAngle: -90,   // optional: rotate start position
      endAngle: 270,
      center: ['50%', '50%'],
    },
  },
  tooltip: {
    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>',
  },
  legend: {
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'middle',
  },
}
```

### Verified configuration — Donut with Center KPI Label

Uses `subtitle` with `floating: true` and `verticalAlign: 'middle'`. No SVG renderer needed.

```typescript
{
  chart: { type: 'pie' },
  title: { text: 'Revenue by Segment' },
  subtitle: {
    text: '$95M<br/>Total ARR',  // <br/> works for line break
    floating: true,
    verticalAlign: 'middle',
    y: 15,                        // fine-tune vertical centering
    style: { fontSize: '16px', fontWeight: 'bold', textAlign: 'center' },
  },
  series: [{
    name: 'Revenue',
    innerSize: '60%',
    data: [ /* ... */ ],
  }],
  plotOptions: {
    pie: {
      dataLabels: { enabled: false }, // disable outer labels to avoid clash
      showInLegend: true,
    },
  },
  legend: {
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'middle',
  },
}
```

### Verified configuration — Accessible Donut

```typescript
{
  accessibility: {
    enabled: true,
    description: 'Donut chart showing revenue split by segment.',
    point: { valueSuffix: '%' },
  },
  // ... rest of config
}
```

### Verified rules
- `innerSize` lives on the **series object**, not `plotOptions.pie`. String (`'60%'`) or number (pixels).
- `showInLegend: true` must be set under `plotOptions.pie` (not top-level `legend`).
- `startAngle` / `endAngle` control rotation; `-90` / `270` starts at top (12 o'clock).
- `sliced: true` on a data point pops it out visually.
- `colorByPoint` is `true` by default for pie — no need to set it.
- Center KPI label via `subtitle.floating + verticalAlign: 'middle'` works; adjust `y` offset per font size.
- `dataLabels.format` supports `{point.percentage:.1f}` — standard Highcharts format string.
- `tooltip.pointFormat` replaces entire tooltip body per point.

### Drilldown — Verified

```typescript
{
  chart: { type: 'column' },  // drilldown is not pie-native; use column for parent
  series: [{
    name: 'Revenue',
    colorByPoint: true,
    data: [
      { name: 'Americas', y: 180, drilldown: 'americas' },
      { name: 'EMEA',     y: 130, drilldown: 'emea' },
    ],
  }],
  xAxis: { type: 'category' },  // required for drilldown category axis
  drilldown: {
    series: [
      { id: 'americas', name: 'Americas', data: [['North America', 140], ['LATAM', 40]] },
      { id: 'emea',     name: 'EMEA',     data: [['Europe', 90], ['MEA', 40]] },
    ],
  },
}
```

- `xAxis.type: 'category'` is **required** for drilldown to render correctly.
- `drilldown` key on a data point must exactly match `drilldown.series[].id`.
- Drilldown on pie (parent = pie, drilldown = pie) is also supported but not verified here.
- Module: `drilldown.js` required in standalone Highcharts. **Not needed** in the MCP renderer.

### Not verified / avoid
- `// UNVERIFIED: pie-to-pie drilldown. Known to work in standalone; MCP not tested.`
- `// SAFE FALLBACK: column → column drilldown verified above.`
- Pattern fill (Highcharts `patternFill` module) — not tested. Requires `pattern-fill.js` module.

---

## 2. Bar Charts (Horizontal)

### Pattern
`type: 'bar'` — horizontal bars. Category axis is vertical (xAxis). Value axis is horizontal (yAxis).
Used for ranked comparisons (top N regions, pipeline stages, etc.).

### Verified configuration — Standard Bar

```typescript
{
  chart: { type: 'bar' },
  title: { text: 'Sales by Region' },
  series: [{ name: 'Q4 Sales', data: [120, 95, 80, 60, 45] }],
  xAxis: {
    categories: ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'MEA'],
  },
  yAxis: { title: { text: 'Revenue ($M)' } },
  plotOptions: {
    bar: {
      dataLabels: { enabled: true },
    },
  },
}
```

### Verified configuration — Grouped Bar

```typescript
{
  chart: { type: 'bar' },
  series: [
    { name: 'Q3', data: [40, 25, 15, 8] },
    { name: 'Q4', data: [55, 30, 18, 12] },
  ],
  xAxis: { categories: ['Prospect', 'Qualified', 'Proposal', 'Closed'] },
  yAxis: { title: { text: 'Deals ($M)' } },
  plotOptions: {
    bar: {
      dataLabels: { enabled: true, format: '${point.y}M' },
      groupPadding: 0.1,   // space between groups (0-0.5)
    },
  },
  tooltip: { shared: true },
}
```

### Verified configuration — Stacked Bar

```typescript
{
  chart: { type: 'bar' },
  series: [
    { name: 'Won',    data: [40, 30, 20] },
    { name: 'Active', data: [30, 25, 35] },
    { name: 'Lost',   data: [20, 15, 10] },
  ],
  xAxis: { categories: ['Enterprise', 'Mid-Market', 'SMB'] },
  yAxis: {
    title: { text: 'Deals' },
    stackLabels: { enabled: true },  // total label on top of stack
  },
  plotOptions: {
    bar: { stacking: 'normal' },     // 'normal' = absolute, 'percent' = 100%
  },
}
```

### Verified rules
- `xAxis` = category axis (vertical in bar). `yAxis` = value axis (horizontal).
- `groupPadding` controls space between groups; `pointPadding` controls space within group.
- `stacking: 'normal'` | `'percent'` on `plotOptions.bar`.
- `stackLabels.enabled: true` on `yAxis` shows totals — works with `stacking: 'normal'`.
- `tooltip: { shared: true }` shows all series at a hovered category — works in bar.
- `dataLabels.format` uses Highcharts format strings; `${point.y}M` works for currency prefix.
- `colorByPoint: true` on series gives each bar a different color.

### Not verified / avoid
- `// UNVERIFIED: waterfall bar chart. Different type ('waterfall') — not tested here.`
- Negative bars (diverging bar): untested. `plotOptions.bar.threshold: 0` expected to work.

---

## 3. Column Charts (Vertical)

### Pattern
`type: 'column'` — vertical bars. Standard for time-bucketed data (monthly, quarterly).

### Verified configuration — Standard Column

```typescript
{
  chart: { type: 'column' },
  title: { text: 'Monthly Revenue' },
  series: [{ name: '2024', data: [42, 55, 48, 61, 70, 65, 78, 82, 75, 88, 92, 99] }],
  xAxis: {
    categories: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
  },
  yAxis: {
    title: { text: 'Revenue ($M)' },
    gridLineWidth: 1,
  },
}
```

### Verified configuration — Grouped Column

```typescript
{
  chart: { type: 'column' },
  series: [
    { name: '2023', data: [48, 55, 62, 70] },
    { name: '2024', data: [61, 72, 80, 95] },
  ],
  xAxis: { categories: ['Q1', 'Q2', 'Q3', 'Q4'] },
  yAxis: { title: { text: 'Revenue ($M)' } },
  plotOptions: {
    column: {
      grouping: true,          // default true; explicit for clarity
      groupPadding: 0.1,       // space between category groups
      pointPadding: 0.05,      // space between bars within group
    },
  },
  tooltip: { shared: true, crosshairs: true },
}
```

### Verified configuration — Stacked Column (absolute)

```typescript
{
  chart: { type: 'column' },
  series: [
    { name: 'Product',  data: [60, 55, 50, 45] },
    { name: 'Services', data: [25, 30, 35, 38] },
    { name: 'Other',    data: [15, 15, 15, 17] },
  ],
  xAxis: { categories: ['Q1', 'Q2', 'Q3', 'Q4'] },
  yAxis: { title: { text: 'Revenue ($M)' }, stackLabels: { enabled: true } },
  plotOptions: {
    column: { stacking: 'normal' },
  },
}
```

### Verified configuration — 100% Stacked Column

```typescript
{
  plotOptions: {
    column: {
      stacking: 'percent',
      dataLabels: { enabled: true, format: '{point.percentage:.0f}%' },
    },
  },
  yAxis: { title: { text: 'Percent' }, max: 100 },
  tooltip: { pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>' },
}
```

### Verified rules
- `groupPadding` (between groups) and `pointPadding` (within group) both expressed as fraction of point width.
- `crosshairs: true` on tooltip adds a vertical crosshair line.
- `tooltip.shared: true` shows all series in one tooltip at hover position.
- `stackLabels.enabled: true` on `yAxis` for column stacks — shows sum at top.
- `stacking: 'percent'` automatically normalizes to 100%; set `yAxis.max: 100` for explicit cap.
- `colorByPoint: true` on a single-series column gives each column a distinct color (good for drilldown parent).

### Responsive behavior
- MCP auto-injects responsive rules at `maxWidth: 400` (hide legend, credits, yAxis title) and `maxWidth: 300` (smaller fonts). These are always present in MCP output.
- Override with your own `responsive.rules` array — it replaces the injected rules.

### Not verified / avoid
- `// UNVERIFIED: column with plotLine/plotBand on xAxis or yAxis. Known valid API; not tested.`

---

## 4. Line Charts

### Pattern
`type: 'line'` — connects points with straight segments. Best for trends and multi-series comparison.

### Verified configuration — Standard Line with Markers

```typescript
{
  chart: { type: 'line' },
  title: { text: 'User Growth' },
  series: [{
    name: 'Active Users',
    data: [1200, 1350, 1480, 1600, 1750, 1900, 2100, 2300, 2500, 2750, 3000, 3200],
  }],
  xAxis: { categories: ['Jan','Feb','Mar', /* ... */] },
  yAxis: { title: { text: 'Users' } },
  plotOptions: {
    line: {
      marker: {
        enabled: true,
        symbol: 'circle',  // 'circle' | 'square' | 'diamond' | 'triangle' | 'triangle-down'
        radius: 4,
      },
    },
  },
}
```

### Verified configuration — Time-Series Line

```typescript
{
  chart: { type: 'line' },
  series: [{
    name: 'DAU',
    data: [
      [1704067200000, 4200],  // [timestamp_ms, value]
      [1704153600000, 4350],
      // ...
    ],
  }],
  xAxis: {
    type: 'datetime',
    labels: { format: '{value:%b %e}' },  // Highcharts date format string
  },
  yAxis: { title: { text: 'Users' } },
  tooltip: {
    xDateFormat: '%A, %b %e',           // tooltip date format
    pointFormat: '<b>{point.y:,.0f}</b> users',
  },
}
```

### Verified configuration — Dual-Axis Multi-Series

```typescript
{
  chart: { type: 'line' },
  series: [
    { name: 'Revenue',    data: [/* ... */], yAxis: 0 },
    { name: 'Users (K)',  data: [/* ... */], yAxis: 1 },
  ],
  yAxis: [
    { title: { text: 'Revenue ($M)' } },
    { title: { text: 'Users (K)' }, opposite: true },
  ],
  tooltip: { shared: true },
  plotOptions: { line: { marker: { enabled: false } } },
}
```

### Verified rules
- `xAxis.type: 'datetime'` enables timestamp-based axis; data must be `[ms_timestamp, value]` pairs.
- `xAxis.labels.format` uses `{value:%b %e}` style — Highcharts date format, not moment.js.
- `tooltip.xDateFormat` overrides date display in tooltip header.
- `tooltip.pointFormat` uses `{point.y:,.0f}` for comma-formatted integers.
- `opposite: true` on `yAxis` places axis on right side.
- `marker.enabled: false` hides dots on line — preferred for dense time-series.
- `marker.symbol` options: `circle`, `square`, `diamond`, `triangle`, `triangle-down`.
- `tooltip.shared: true` required for meaningful multi-series hover comparison.

### Not verified / avoid
- `// UNVERIFIED: connectNulls option behavior when data has null gaps. API exists; not tested.`
- `// SAFE FALLBACK: omit nulls from data array entirely to avoid gaps.`

---

## 5. Spline Charts

### Pattern
`type: 'spline'` — same as line but with Bezier curve smoothing. Use when:
- Data has natural curves (heartbeat, gradual trends)
- You want smoother visual without hard angles
- NOT when precise value reading matters (smoothing shifts visual peak from actual data point)

### Verified configuration — Standard Spline, No Markers

```typescript
{
  chart: { type: 'spline' },
  title: { text: 'Session Duration Trend' },
  series: [{
    name: 'Avg Session (min)',
    data: [4.2, 4.8, 5.1, 4.9, 5.5, 6, 5.8, 6.3, 6.7, 7.1, 6.9, 7.4],
  }],
  xAxis: { categories: ['Jan','Feb', /* ... */] },
  yAxis: { title: { text: 'Minutes' } },
  plotOptions: {
    spline: { marker: { enabled: false } },
  },
}
```

### Verified configuration — Spline Actual vs Target

```typescript
{
  chart: { type: 'spline' },
  series: [
    {
      name: 'Actual',
      data: [42, 55, 48, 61, 70, 65, 78, 82, 75, 88, 92, 99],
      marker: { enabled: true, radius: 3 },
    },
    {
      name: 'Target',
      data: [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105],
      dashStyle: 'ShortDash',         // dashed line for reference/target
      marker: { enabled: false },
    },
  ],
  tooltip: { shared: true, valueSuffix: 'M' },
}
```

### Verified rules
- `dashStyle` valid values (verified via render): `'ShortDash'`, `'Dash'`, `'Dot'`, `'DashDot'`, `'LongDash'`, `'Solid'`.
- `marker` config per-series overrides `plotOptions.spline.marker`.
- `tooltip.valueSuffix` appends to every point value in tooltip.
- Spline and line share the same API surface — any line config works on spline.
- Spline smoothing is automatic Bezier — no tension parameter exposed in the public API.
- For very noisy data, spline can visually flatten peaks. Use line instead.

### When spline vs line
| Situation | Recommendation |
|---|---|
| Dense time-series, precise values matter | `line` |
| Moderate data, aesthetic smoothness matters | `spline` |
| KPI trends, impression charts | `spline` |
| Stock/financial data | `render_stock_chart` |
| Data has abrupt step changes | `line` or `step` type |

---

## 6. Shared Enterprise Patterns

### Accessibility

```typescript
accessibility: {
  enabled: true,
  description: 'Human-readable chart description for screen readers.',
  point: {
    valueDescriptionFormat: '{index}. {point.category}: {point.y} million dollars.',
    valueSuffix: '%',  // appended to announced values
  },
  series: {
    descriptionFormat: '{series.name}, bar chart with {series.points.length} bars.',
  },
  screenReaderSection: {
    beforeChartFormat:
      '<h5>{chartTitle}</h5><div>{typeDescription}</div>' +
      '<div>{chartSubtitle}</div><div>{chartLongdesc}</div>',
  },
}
```

- Accessibility module is built into modern Highcharts. No separate module needed in MCP.
- `accessibility.enabled: true` is sufficient minimal config. Add `description` for audits.
- `point.valueSuffix` announces the unit after each value (e.g. "45 percent").

### Responsive Rules

MCP auto-injects these rules — do not rely on them in application code. Set your own:

```typescript
responsive: {
  rules: [
    {
      condition: { maxWidth: 600 },
      chartOptions: {
        legend: { enabled: false },
        yAxis: { title: { text: null } },
        plotOptions: { series: { dataLabels: { enabled: false } } },
      },
    },
    {
      condition: { maxWidth: 400 },
      chartOptions: {
        title: { style: { fontSize: '12px' } },
        credits: { enabled: false },
      },
    },
  ],
}
```

- `responsive.rules` is an array; first matching `condition.maxWidth` wins.
- Target: chart container width, not viewport width.
- Safe to disable legend, yAxis title, dataLabels at small widths.

### Legend

```typescript
legend: {
  enabled: true,
  layout: 'vertical',           // 'horizontal' | 'vertical' | 'proximate'
  align: 'right',               // 'left' | 'center' | 'right'
  verticalAlign: 'middle',      // 'top' | 'middle' | 'bottom'
  itemStyle: {
    fontWeight: 'normal',
    fontSize: '13px',
  },
  symbolRadius: 2,              // rounded corners on legend symbol box
}
```

- `layout: 'proximate'` renders legend items next to each series' last point (line charts).
- Pie/donut: `showInLegend: true` on `plotOptions.pie` (not top-level `legend`).
- Disable legend: `legend: { enabled: false }` OR `legend: false`.

### Tooltip Patterns

```typescript
// Shared tooltip (all series at cursor x position)
tooltip: {
  shared: true,
  crosshairs: true,
  headerFormat: '<b>{point.key}</b><br/>',       // header line
  pointFormat: '{series.name}: <b>{point.y}</b><br/>',
  footerFormat: '',
  valueSuffix: 'M',
  valueDecimals: 1,
}

// DateTime tooltip
tooltip: {
  xDateFormat: '%A, %B %e, %Y',   // day of week, month, day, year
  pointFormat: '<b>{point.y:,.0f}</b>',
}

// HTML tooltip (richer formatting)
tooltip: {
  useHTML: true,
  formatter: function() {
    return `<div style="padding:4px"><b>${this.x}</b>: ${this.y}M</div>`;
  }
}
```

- `{point.y:,.0f}` = comma thousands separator, 0 decimals.
- `{point.percentage:.1f}` = one decimal percent (pie/stacked).
- `formatter` function overrides all format strings; `this` = point context.
- `useHTML: true` enables actual HTML in tooltip body.

### Data Labels

```typescript
plotOptions: {
  series: {
    dataLabels: {
      enabled: true,
      format: '{point.y:.1f}M',      // value format
      style: {
        fontSize: '11px',
        fontWeight: 'normal',
        textOutline: 'none',         // remove default white text outline
        color: '#333333',
      },
      crop: false,
      overflow: 'none',
    },
  },
}
```

- `textOutline: 'none'` removes the default white halo around data label text.
- `crop: false` + `overflow: 'none'` prevents clipping at chart edges.
- Per-series override: set `dataLabels` directly on the series object.

### Colors / Contrast

```typescript
colors: [
  '#2196F3', '#FF9800', '#4CAF50', '#F44336',
  '#9C27B0', '#00BCD4', '#FF5722', '#607D8B',
],

plotOptions: {
  series: {
    colorByPoint: false,  // one color per series (default for most types)
  },
}
```

- `colors` array at chart root sets the global color sequence for all series.
- For accessibility: ensure minimum 3:1 contrast against chart background.
- Pie/donut: `colorByPoint` is `true` by default — no need to set.
- Column single-series: set `colorByPoint: true` for per-bar color.

### Empty / No Data State

```typescript
// Requires no-data-to-display.js module in standalone.
// In MCP: accepted and rendered (empty chart area shown).
noData: {
  style: {
    fontWeight: 'bold',
    fontSize: '15px',
    color: '#666666',
  },
  position: {
    align: 'center',
    verticalAlign: 'middle',
  },
},
lang: {
  noData: 'No data available for this period',  // custom message
},
```

- Pass empty `data: []` in series to trigger noData display.
- `lang.noData` overrides the default "No data to display" text.
- Module requirement: `no-data-to-display.js` in standalone. MCP accepts config but module availability in rendering environment not confirmed — use with expectation of fallback to empty chart area.

### Loading State

```typescript
// Triggered programmatically, not via config:
// chart.showLoading('Loading data...');
// chart.hideLoading();

loading: {
  style: {
    backgroundColor: '#ffffff',
    opacity: 0.8,
  },
  labelStyle: {
    fontWeight: 'bold',
    fontSize: '14px',
    color: '#666666',
  },
}
```

- `// UNVERIFIED: showLoading() programmatic call via MCP. Config key accepted; runtime call requires chart instance.`
- `// SAFE FALLBACK: For static MCP renders, handle loading state outside Highcharts (skeleton screen, wrapper div).`

### Credits / Exporting

```typescript
credits: { enabled: false },   // remove "Highcharts.com" link
exporting: { enabled: false },  // remove hamburger export menu
```

- Both verified. Standard in enterprise deployments.
- Exporting options if needed:

```typescript
exporting: {
  enabled: true,
  buttons: {
    contextButton: {
      menuItems: ['downloadPNG', 'downloadSVG', 'downloadCSV'],
    },
  },
  filename: 'my-chart',
}
```

- `// UNVERIFIED: exporting.menuItems behavior in MCP render context. Likely no-op (no server-side export).`

### Axis Label Formatting

```typescript
// Category axis — no formatter needed
xAxis: { categories: ['Q1', 'Q2', 'Q3', 'Q4'] }

// Datetime axis
xAxis: {
  type: 'datetime',
  labels: { format: '{value:%b %e}' },          // Jan 1, Jan 2...
  dateTimeLabelFormats: {                         // format at each zoom level
    day:   '%b %e',
    week:  '%b %e',
    month: '%b %Y',
    year:  '%Y',
  },
}

// Value axis with prefix/suffix
yAxis: {
  title: { text: null },                          // hide yAxis title
  labels: {
    format: '${value}M',                          // prefix $, suffix M
    // OR formatter function:
    formatter: function() {
      return this.value >= 1000
        ? (this.value / 1000) + 'K'
        : this.value;
    },
  },
}
```

- `{value:%b %e}` in axis label format = Highcharts date format string (not strftime exactly).
- `formatter` function gives full control; `this.value` = axis tick value.

---

## 7. Dashboard / Integration Notes

### Verified — KPI Row + Full-Width Chart

```typescript
// render_dashboard input
{
  gui: {
    layouts: [{
      rows: [
        {
          cells: [
            { id: 'kpi-1', width: '1/3' },
            { id: 'kpi-2', width: '1/3' },
            { id: 'kpi-3', width: '1/3' },
          ],
        },
        {
          cells: [{ id: 'chart-1' }],  // no width = full row
        },
      ],
    }],
  },
  components: [
    { type: 'KPI', renderTo: 'kpi-1', title: 'Total ARR', value: '$95M', subtitle: '+12% YoY' },
    { type: 'KPI', renderTo: 'kpi-2', title: 'Active Users', value: '3,200', subtitle: '+8% MoM' },
    { type: 'KPI', renderTo: 'kpi-3', title: 'NPS Score', value: '72', subtitle: 'Industry avg: 45' },
    {
      type: 'Highcharts',
      renderTo: 'chart-1',
      chartOptions: {
        chart: { type: 'column' },
        title: { text: 'Monthly Revenue' },
        series: [{ name: 'Revenue', data: [42, 55, 48, 61, 70, 65, 78, 82, 75, 88, 92, 99] }],
        xAxis: { categories: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] },
      },
    },
  ],
}
```

### Verified — Chart + DataGrid with Shared DataPool

```typescript
{
  gui: {
    layouts: [{
      rows: [{
        cells: [
          { id: 'chart-1', width: '2/3' },
          { id: 'grid-1',  width: '1/3' },
        ],
      }],
    }],
  },
  dataPool: {
    connectors: [{
      id: 'revenue-data',
      type: 'JSON',
      options: {
        data: {
          columns: {
            month:   ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            revenue: [42, 55, 48, 61, 70, 65],
          },
        },
      },
    }],
  },
  components: [
    {
      type: 'Highcharts',
      renderTo: 'chart-1',
      connector: { id: 'revenue-data' },   // reference connector by id
      chartOptions: {
        chart: { type: 'column' },
        title: { text: 'Monthly Revenue' },
        xAxis: { categories: ['Jan','Feb','Mar','Apr','May','Jun'] },
      },
    },
    {
      type: 'DataGrid',
      renderTo: 'grid-1',
      connector: { id: 'revenue-data' },
    },
  ],
}
```

### Verified rules
- `gui.layouts[].rows[].cells[].id` must **exactly** match `components[].renderTo`. Mismatch = silent no-render.
- Cell `width` is a CSS fraction string: `'1/2'`, `'1/3'`, `'2/3'`, `'1/4'`. No width = full row.
- `dataPool.connectors[].type: 'JSON'` with `options.data.columns` = column-oriented data.
- `connector: { id: 'X' }` on component references dataPool by id — data shared across components.
- `DataGrid` component renders sortable table from connector data automatically.
- KPI `value` accepts string or number. `subtitle` is plain text below value.

### Not verified / avoid
- `// UNVERIFIED: cross-component cursor sync (hover on chart highlights row in grid). Known feature of @highcharts/dashboards; requires sync config. Not tested.`
- `// SAFE FALLBACK: use separate render_chart + render_grid calls if sync not needed.`
- `// UNVERIFIED: GoogleSheets connector. dataPool.connectors[].type: 'GoogleSheets'. API known; not tested.`
- `// UNVERIFIED: editMode. render_dashboard accepts editMode key but interactive drag-resize is runtime-only.`

---

## Validation Tool Notes

`validate_config` (`mcp__81e48b56__validate_config`) has an **incomplete schema**:

| Warning produced | Reality |
|---|---|
| `Unknown option 'series.0.innerSize'` | Valid — `innerSize` is real pie series API |
| `Unknown option 'series.0.data'` | False positive — `data` always valid |
| `Unknown option 'plotOptions.column.stacking'` | False positive — `stacking` is valid |

**Rule**: `validate_config` status `Valid` = no hard errors. Warnings on `series[].data`, `series[].innerSize`, `plotOptions.*.stacking` are **false positives** — ignore them.

Use `validate_config` for:
- Catching typos in option key names (e.g. `dataLabel` vs `dataLabels`)
- Catching type errors (string where number expected)
- Sanity check before large renders

Do not use as authoritative — test render is the final arbiter.

---

## Module Requirements Summary

| Feature | Module (standalone) | MCP |
|---|---|---|
| Accessibility | `accessibility.js` | Built-in |
| Drilldown | `drilldown.js` | Built-in |
| No-data display | `no-data-to-display.js` | Config accepted; display unconfirmed |
| Exporting | `exporting.js` | Config accepted; export likely no-op |
| Data module (CSV/HTML source) | `data.js` | Untested |
| Pattern fill | `pattern-fill.js` | Untested |
| Boost (WebGL) | `boost.js` | Config accepted; WebGL depends on renderer env |
| Stock tools | `stock-tools.js` | Use `render_stock_chart` |
| Dashboards | `@highcharts/dashboards` | Use `render_dashboard` |

---

## Format String Reference

| Token | Meaning | Example output |
|---|---|---|
| `{point.y}` | Raw Y value | `45` |
| `{point.y:.1f}` | 1 decimal | `45.0` |
| `{point.y:,.0f}` | Comma thousands, 0 dec | `4,200` |
| `{point.percentage:.1f}` | Percent of total, 1 dec | `38.5` |
| `{point.name}` | Point name | `Enterprise` |
| `{series.name}` | Series name | `Revenue` |
| `{value:%b %e}` | Date on axis | `Jan 5` |
| `{value:%b %Y}` | Month/year | `Jan 2024` |
| `%A, %b %e, %Y` | Full date (xDateFormat) | `Monday, Jan 1, 2024` |
