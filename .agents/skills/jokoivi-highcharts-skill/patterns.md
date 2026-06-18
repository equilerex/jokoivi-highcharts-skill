# Highcharts Config Patterns — Reference

Verified patterns. All rendered successfully via MCP. TypeScript `Highcharts.Options` format.

## Contents

- [Donut / Pie](#donut--pie) — standard, center KPI label, rules
- [Bar (Horizontal)](#bar-horizontal) — standard, grouped, stacked, rules
- [Column (Vertical)](#column-vertical) — standard, grouped, stacked absolute, stacked 100%, drilldown
- [Line](#line) — standard, time-series, dual-axis, rules
- [Spline](#spline) — standard, actual vs target, spline vs line decision
- [Shared patterns](#shared-patterns) — tooltip, data labels, legend, axis formatting, responsive, credits/exporting, noData, accessible colors
- [Format string reference](#format-string-reference)
- [Dashboard patterns](#dashboard-patterns) — KPI row + chart, chart + DataGrid with shared data, rules

---

## Donut / Pie

### Standard donut

```typescript
const options: Highcharts.Options = {
  chart: { type: 'pie' },
  title: { text: 'Revenue by Segment' },
  series: [{
    type: 'pie',
    name: 'Revenue',
    innerSize: '60%',       // string % or number px — lives on series, not plotOptions
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
      showInLegend: true,   // must be here, not top-level legend
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
};
```

### Donut with center KPI label

Uses `subtitle` floating trick — no SVG renderer needed.

```typescript
{
  chart: { type: 'pie' },
  title: { text: 'Revenue by Segment' },
  subtitle: {
    text: '$95M<br/>Total ARR',       // <br/> works for line break
    floating: true,
    verticalAlign: 'middle',
    y: 15,                             // fine-tune per font size
    style: { fontSize: '16px', fontWeight: 'bold', textAlign: 'center' },
  },
  series: [{
    type: 'pie',
    innerSize: '60%',
    data: [ /* ... */ ],
  }],
  plotOptions: {
    pie: {
      dataLabels: { enabled: false },  // disable outer labels
      showInLegend: true,
    },
  },
}
```

### Pie rules
- `innerSize` on **series object** — not `plotOptions.pie`
- `showInLegend` under `plotOptions.pie`
- `colorByPoint` is `true` by default — don't set
- `startAngle: -90, endAngle: 270` for 12-o'clock start
- `sliced: true` on a data point pops it out
- `center: ['50%', '50%']` for explicit centering

---

## Bar (Horizontal)

### Standard bar

```typescript
{
  chart: { type: 'bar' },
  series: [{ name: 'Q4 Sales', data: [120, 95, 80, 60, 45] }],
  xAxis: {
    categories: ['North America', 'Europe', 'APAC', 'LATAM', 'MEA'],
  },
  yAxis: { title: { text: 'Revenue ($M)' } },
  plotOptions: {
    bar: {
      dataLabels: { enabled: true },
    },
  },
}
```

### Grouped bar

```typescript
{
  chart: { type: 'bar' },
  series: [
    { name: 'Q3', data: [40, 25, 15, 8] },
    { name: 'Q4', data: [55, 30, 18, 12] },
  ],
  xAxis: { categories: ['Prospect', 'Qualified', 'Proposal', 'Closed'] },
  plotOptions: {
    bar: {
      groupPadding: 0.1,    // space between category groups
      pointPadding: 0.05,   // space between bars within group
      dataLabels: { enabled: true, format: '${point.y}M' },
    },
  },
  tooltip: { shared: true },
}
```

### Stacked bar

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
    stackLabels: { enabled: true },   // total on top — lives on yAxis
  },
  plotOptions: {
    bar: { stacking: 'normal' },      // 'normal' | 'percent'
  },
}
```

### Bar rules
- `xAxis` = category (vertical). `yAxis` = value (horizontal). Opposite of column.
- `stackLabels` on `yAxis`, not `plotOptions`
- `tooltip.shared: true` recommended for grouped/stacked
- `colorByPoint: true` on single-series bar for per-bar colors

---

## Column (Vertical)

### Standard column

```typescript
{
  chart: { type: 'column' },
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

### Grouped column

```typescript
{
  chart: { type: 'column' },
  series: [
    { name: '2023', data: [48, 55, 62, 70] },
    { name: '2024', data: [61, 72, 80, 95] },
  ],
  xAxis: { categories: ['Q1', 'Q2', 'Q3', 'Q4'] },
  plotOptions: {
    column: {
      grouping: true,       // default true
      groupPadding: 0.1,
      pointPadding: 0.05,
    },
  },
  tooltip: { shared: true, crosshairs: true },
}
```

### Stacked column — absolute

```typescript
{
  plotOptions: {
    column: { stacking: 'normal' },
  },
  yAxis: {
    stackLabels: { enabled: true },
  },
}
```

### Stacked column — 100% percent

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

### Column with drilldown

```typescript
{
  chart: { type: 'column' },
  series: [{
    name: 'Revenue',
    colorByPoint: true,
    data: [
      { name: 'Americas', y: 180, drilldown: 'americas' },
      { name: 'EMEA',     y: 130, drilldown: 'emea' },
      { name: 'APAC',     y: 90,  drilldown: 'apac' },
    ],
  }],
  xAxis: { type: 'category' },    // REQUIRED for drilldown
  drilldown: {
    series: [
      { id: 'americas', name: 'Americas', data: [['North America', 140], ['LATAM', 40]] },
      { id: 'emea',     name: 'EMEA',     data: [['Europe', 90], ['MEA', 40]] },
      { id: 'apac',     name: 'APAC',     data: [['ANZ', 35], ['SE Asia', 30], ['India', 25]] },
    ],
  },
  tooltip: {
    headerFormat: '<b>{point.name}</b><br/>',
    pointFormat: 'Revenue: <b>${point.y}M</b>',
  },
}
```

---

## Line

### Standard line with markers

```typescript
{
  chart: { type: 'line' },
  series: [{
    name: 'Active Users',
    data: [1200, 1350, 1480, 1600, 1750, 1900, 2100, 2300],
  }],
  xAxis: { categories: [ /* ... */ ] },
  plotOptions: {
    line: {
      marker: {
        enabled: true,
        symbol: 'circle',   // 'circle' | 'square' | 'diamond' | 'triangle' | 'triangle-down'
        radius: 4,
      },
    },
  },
}
```

### Time-series line

```typescript
{
  chart: { type: 'line' },
  series: [{
    name: 'DAU',
    data: [
      [1704067200000, 4200],   // [ms_timestamp, value] — ISO strings won't work
      [1704153600000, 4350],
    ],
  }],
  xAxis: {
    type: 'datetime',
    labels: { format: '{value:%b %e}' },
    dateTimeLabelFormats: {
      day:   '%b %e',
      week:  '%b %e',
      month: '%b %Y',
      year:  '%Y',
    },
  },
  tooltip: {
    xDateFormat: '%A, %b %e, %Y',
    pointFormat: '<b>{point.y:,.0f}</b> users',
  },
}
```

### Dual-axis multi-series

```typescript
{
  chart: { type: 'line' },
  series: [
    { name: 'Revenue ($M)', data: [ /* ... */ ], yAxis: 0 },
    { name: 'Users (K)',    data: [ /* ... */ ], yAxis: 1 },
  ],
  yAxis: [
    { title: { text: 'Revenue ($M)' } },
    { title: { text: 'Users (K)' }, opposite: true },  // opposite on yAxis object
  ],
  tooltip: { shared: true },
  plotOptions: { line: { marker: { enabled: false } } },
}
```

### Line rules
- Datetime data must be `[ms_timestamp, value]` — convert ISO strings before passing
- `marker.enabled: false` preferred for dense time-series
- `tooltip.shared: true` required for meaningful multi-series comparison
- `opposite: true` on `yAxis` object, not on series

---

## Spline

### Standard spline (no markers)

```typescript
{
  chart: { type: 'spline' },
  series: [{ name: 'Avg Session (min)', data: [ /* ... */ ] }],
  plotOptions: {
    spline: { marker: { enabled: false } },
  },
}
```

### Spline: actual vs target

```typescript
{
  chart: { type: 'spline' },
  series: [
    {
      name: 'Actual',
      data: [ /* ... */ ],
      marker: { enabled: true, radius: 3 },
    },
    {
      name: 'Target',
      data: [ /* ... */ ],
      dashStyle: 'ShortDash',     // 'Dash' | 'ShortDash' | 'Dot' | 'DashDot' | 'LongDash'
      marker: { enabled: false },
    },
  ],
  tooltip: { shared: true, valueSuffix: 'M' },
}
```

### Spline vs line decision

| Situation | Use |
|---|---|
| Dense time-series, precise value reading | `line` |
| Gradual trends, aesthetic smoothness | `spline` |
| KPI trends, impression charts | `spline` |
| Abrupt step changes | `line` |
| Stock / financial | `render_stock_chart` |
| Very noisy data | `line` (spline flattens peaks) |

---

## Shared patterns

### Tooltip

```typescript
// Shared (all series at x)
tooltip: {
  shared: true,
  crosshairs: true,
  headerFormat: '<b>{point.key}</b><br/>',
  pointFormat: '{series.name}: <b>{point.y}</b><br/>',
  valueSuffix: 'M',
  valueDecimals: 1,
}

// Datetime
tooltip: {
  xDateFormat: '%A, %B %e, %Y',
  pointFormat: '<b>{point.y:,.0f}</b>',
}

// HTML (rich formatting)
tooltip: {
  useHTML: true,
  formatter(): string {
    return `<div style="padding:4px"><b>${this.x}</b>: ${this.y}M</div>`;
  },
}
```

### Data labels

```typescript
plotOptions: {
  series: {
    dataLabels: {
      enabled: true,
      format: '{point.y:.1f}M',
      style: {
        fontSize: '11px',
        fontWeight: 'normal',
        textOutline: 'none',    // remove default white halo
        color: '#333333',
      },
      crop: false,
      overflow: 'none',
    },
  },
}
```

### Legend

```typescript
legend: {
  enabled: true,
  layout: 'vertical',           // 'horizontal' | 'vertical' | 'proximate'
  align: 'right',
  verticalAlign: 'middle',
  itemStyle: {
    fontWeight: 'normal',
    fontSize: '13px',
  },
}
// Disable: legend: { enabled: false }
// 'proximate': renders each item next to series end (line charts)
```

### Axis label formatting

```typescript
// Value axis: prefix/suffix
yAxis: {
  labels: {
    format: '${value}M',
  },
}

// Value axis: formatter function (K/M abbreviation)
yAxis: {
  labels: {
    formatter(): string {
      return this.value >= 1000
        ? `${this.value / 1000}K`
        : String(this.value);
    },
  },
}

// Datetime axis
xAxis: {
  type: 'datetime',
  labels: { format: '{value:%b %e}' },
}
```

### Responsive rules

```typescript
// MCP auto-injects its own rules — do not rely on them in app code
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

### Credits / exporting

```typescript
credits: { enabled: false },    // remove Highcharts.com link
exporting: { enabled: false },  // remove hamburger export menu
```

### Empty / no-data state

```typescript
// Requires no-data-to-display.js module
noData: {
  style: { fontWeight: 'bold', fontSize: '15px', color: '#666666' },
  position: { align: 'center', verticalAlign: 'middle' },
},
lang: {
  noData: 'No data available for this period',
},
// Pass series: [{ data: [] }] to trigger
```

### Colors — safe accessible palette (3:1+ on white)

```typescript
colors: [
  '#1565C0',  // blue
  '#E65100',  // orange
  '#2E7D32',  // green
  '#6A1B9A',  // purple
  '#00695C',  // teal
  '#AD1457',  // pink
  '#37474F',  // grey-blue
  '#F57F17',  // amber
],
```

---

## Format string reference

| Token | Output |
|---|---|
| `{point.y}` | Raw value: `45` |
| `{point.y:.1f}` | 1 decimal: `45.0` |
| `{point.y:,.0f}` | Comma thousands: `4,200` |
| `{point.percentage:.1f}` | Percent: `38.5` |
| `{point.name}` | Point name |
| `{series.name}` | Series name |
| `{value:%b %e}` | Axis date: `Jan 5` |
| `{value:%b %Y}` | Month/year: `Jan 2024` |
| `%A, %b %e, %Y` | Full: `Monday, Jan 1, 2024` |

---

## Dashboard patterns

### KPI row + chart

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
        { cells: [{ id: 'chart-1' }] },   // no width = full row
      ],
    }],
  },
  components: [
    { type: 'KPI', renderTo: 'kpi-1', title: 'ARR', value: '$95M', subtitle: '+12% YoY' },
    { type: 'KPI', renderTo: 'kpi-2', title: 'Users', value: '3,200', subtitle: '+8% MoM' },
    { type: 'KPI', renderTo: 'kpi-3', title: 'NPS', value: '72', subtitle: 'Avg: 45' },
    {
      type: 'Highcharts',
      renderTo: 'chart-1',
      chartOptions: {
        chart: { type: 'column' },
        series: [{ name: 'Revenue', data: [ /* ... */ ] }],
        xAxis: { categories: [ /* ... */ ] },
      },
    },
  ],
}
```

### Chart + DataGrid with shared data

```typescript
{
  dataPool: {
    connectors: [{
      id: 'revenue-data',
      type: 'JSON',
      options: {
        data: {
          columns: {
            month:   ['Jan', 'Feb', 'Mar'],
            revenue: [42, 55, 48],
          },
        },
      },
    }],
  },
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
  components: [
    {
      type: 'Highcharts',
      renderTo: 'chart-1',
      connector: { id: 'revenue-data' },
      chartOptions: { chart: { type: 'column' }, /* ... */ },
    },
    {
      type: 'DataGrid',
      renderTo: 'grid-1',
      connector: { id: 'revenue-data' },
    },
  ],
}
```

### Dashboard rules
- `cells[].id` must exactly match `components[].renderTo` — mismatch = silent no-render
- Cell `width`: `'1/2'`, `'1/3'`, `'2/3'`, `'1/4'`, `'3/4'`. Omit = full row.
- KPI `value` accepts string or number
- Shared data: set `connector.id` on components; data auto-bound
