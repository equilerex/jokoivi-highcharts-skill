# Evaluate Design Feasibility (Rat Rod Detector)

Before writing any configuration, you must verify if a user's design request is natively supported by Highcharts or if it requires brittle hacks.

## The Core Philosophy: Why We Avoid Hacks

Highcharts is not a blank canvas; it is a highly optimized, accessible design system. Designers often mock up visual ideas that inadvertently require:

- Custom SVG rendered directly over the chart (`renderer`)
- Absolute positioned HTML overlays synced to chart redraw events
- Complex DOM manipulation post-render

**Why we NEVER do this:**

1. **Accessibility is Destroyed:** Highcharts natively maps data to screen readers and keyboard navigation. Custom DOM nodes and overlaid SVG shapes completely bypass the `a11y` module, breaking compliance instantly.
2. **Maintenance Debt:** Highcharts upgrades frequently break custom DOM hacks. If a chart requires a "Goblin contract" to function, it will shatter within 12 months.
3. **Performance/Exporting:** Custom HTML overlays do not export cleanly to PDF/PNG via the exporting module and they destroy rendering speed on mobile.

## The Feasibility Triage

When presented with a complex visual layout, classify it into one of these categories:

### 1. Native Supported Options

Things like colors, padding, gridline styles, border radiuses, or standard tooltip formatting.

- **Action:** Proceed to generation. Use `python .agents/skills/jokoivi-highcharts-skill/scripts/map_design_intent.py <keyword>` to find the specific options.

### 2. Supported Extensibility (Use Judiciously)

Using official formatters (`formatter`, `pointFormatter`) to return HTML, or using the official `annotations` module.

- **Action:** Proceed cautiously. Ensure `useHTML: true` is allowed by the project's export constraints. Do not put interactive elements (buttons, inputs) inside tooltips.

### 3. "Rat Rod" Hacks (Flag Immediately)

The designer wants something structurally impossible, like floating labels inside bars with curved custom connector lines, or a legend that acts like a complex external multi-select dropdown widget.

- **Action:** Stop. Explain _why_ it is dangerous (A11y, performance, maintenance).
- **The Pivot:** Offer "less fancy" native alternatives.

## How to Suggest Native Alternatives

If you must talk down a dangerous design, use this framework:

| Fancy Designer Ask                      | Safer Native Alternative                                                        |
| --------------------------------------- | ------------------------------------------------------------------------------- |
| Floating labels inside bars             | Standard `dataLabels` inside/outside with `overflow` rules                      |
| Custom curved connector lines           | Standard tooltip interaction or `series.label`                                  |
| Fully custom center widget in Donut     | Native `title`/`subtitle` vertically aligned, plus standard legend              |
| Clickable label chips overlaid on chart | Use the native `legend` or external form controls driving `series.setVisible()` |
| Complex multi-layer axis grouping       | Shorter axis labels combined with a robust tooltip                              |

### A Note on Terminology

Keep an open mind. Designers do not speak the Highcharts API language.
If they ask for a "tag" or a "chip," they might just need a styled `dataLabel` or a native `legend` item. Do not focus rigidly on the exact word they used; focus on the _intent_ of the layout.

## Design Feasibility Checklist

Before approving any layout or generating options, you must verify the following constraints:

1. **DOM Container Density:** Does the design place more than 4 charts on a single viewport row? If yes, reject and demand a `@highcharts/dashboards` grid layout.
2. **Axis Reciprocity:** Does a horizontal bar chart (`type: 'bar'`) attempt to use an X-axis for time-series? If yes, flag as an axis inversion error (Highcharts maps categories to the Y-axis on horizontal bar charts; the numerical/time scale is mapped to the X-axis in standard charts, but the Y-axis in bar charts).
3. **Overlapping Labels:** If data density is high, ensure `allowOverlap: false` is configured for data labels, or default to a tooltips-only interaction model.
4. **HTML Overlays:** Never suggest absolute-positioned HTML overlays overlaid on top of a chart container; instead, use native subtitles, custom legends, or styled SVG annotations.
