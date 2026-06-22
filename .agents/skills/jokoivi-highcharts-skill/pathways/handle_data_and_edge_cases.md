# Handle Data and Edge Cases

A chart design might look perfect with four clean data points in Figma, but production data is messy. 
Before finalizing a configuration, you must anticipate and handle common data edge cases to prevent the chart from shattering.

## 1. Edge Case Stress Testing
Review the raw data requirements and ensure the configuration handles these scenarios robustly:

### Long Strings & Overlapping Labels
- **The Threat:** Category names like `"Aggregated tax-adjusted investment portfolio performance..."` will overflow the container or collide.
- **The Native Fix:** Use `xAxis.labels.staggerLines`, `xAxis.labels.step`, or `dataLabels.overflow: "justify"`. Highcharts handles collisions automatically if configured properly; do not truncate text manually via CSS/JS.

### Massive Spikes vs Tiny Values
- **The Threat:** One point is `1,000,000` and another is `2`, making the small point invisible or un-hoverable.
- **The Native Fix:** Consider setting a `yAxis.type: 'logarithmic'`, or ensuring `plotOptions.series.minPointLength` is set so tiny columns can still be clicked.

### Missing, Zero, or Negative Data
- **The Threat:** Missing time-series points cause awkward line gaps, or negative values break pie charts.
- **The Native Fix:** For line charts with gaps, set `plotOptions.series.connectNulls: true` (or `false` based on user intent).

## 2. Data Mapping (REST to Highcharts Series)
You must convert flattened JSON arrays from REST APIs into Highcharts-compatible `series` arrays.

### Key Formatting Rules
1. **Never use ISO strings for datetime.** Time-series data must be formatted as `[ms_timestamp, value]`.
2. **Category data** requires an array of strings for `xAxis.categories` and a corresponding numerical `data` array for the series.
3. **Pie/Donut series** require an array of objects `{name: string, y: number}`.

### Using `data_to_series.py`
Suggest using the companion CLI tool located in `.agents/skills/jokoivi-highcharts-skill/scripts/data_to_series.py` for standard transformations.

*Examples:*
- **Column Chart (Category x Value):**
  `python .agents/skills/jokoivi-highcharts-skill/scripts/data_to_series.py --input data.json --type column --x month --y revenue`
- **Line Chart (Datetime x Value):**
  `python .agents/skills/jokoivi-highcharts-skill/scripts/data_to_series.py --input data.json --type line --x date --y value --datetime`
- **Pie Chart (Name x Value):**
  `python .agents/skills/jokoivi-highcharts-skill/scripts/data_to_series.py --input data.json --type pie --name segment --y revenue`
- **Grouped Column:**
  `python .agents/skills/jokoivi-highcharts-skill/scripts/data_to_series.py --input data.json --type grouped-column --x quarter --y revenue --group region`
