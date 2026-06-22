## user:
describe the classic developer and designer interaction with highcharts api when building new features




The classic developer/designer interaction with the Highcharts API is basically a polite hostage negotiation between **visual intent** and **configuration reality**.

Designer says:

> “Can we just make this chart look like the design?”

Developer opens Highcharts config and enters the option labyrinth.

```ts
Highcharts.chart('container', {
  chart: {
    type: 'column',
    spacing: [16, 16, 16, 16],
  },
  title: {
    text: undefined,
  },
  xAxis: {
    labels: {
      style: {
        fontSize: '12px',
      },
    },
  },
  yAxis: {
    gridLineDashStyle: 'Dash',
    title: {
      text: undefined,
    },
  },
  plotOptions: {
    series: {
      borderRadius: 4,
      pointPadding: 0.1,
      groupPadding: 0.2,
    },
  },
  series: [...]
});
```

Designer then says:

> “Almost. The bars should feel softer, the labels less noisy, and the tooltip more Nordea-ish.”

Developer asks:

> “Do you mean border radius, opacity, font weight, spacing, formatter logic, or the existential tone of the hover state?”

Designer points at Figma.

Developer points at the Highcharts docs.

The docs point at eleven different APIs, three deprecated examples, and one property that only works if `styledMode` is false and the moon is in `plotOptions.series.states.hover`.

Then comes the ritual:

### 1. Designer wants visual polish

Usually things like:

* chart should match Figma
* axes should be quieter
* grid lines should be subtle
* legend should align with surrounding layout
* tooltip should look custom
* labels should not overlap
* donut center text should look like the mockup
* colors should follow design tokens
* empty/loading/error states should feel designed, not “library default goblin mode” 🧌

### 2. Developer translates design into Highcharts concepts

The developer mentally maps design words into API caves:

| Designer says                            | Developer hears                                          |
| ---------------------------------------- | -------------------------------------------------------- |
| “Make it cleaner”                        | remove axis title, reduce ticks, soften grid             |
| “Less heavy”                             | lighter label color, thinner lines, lower opacity        |
| “More breathing room”                    | spacing, margin, label padding                           |
| “Can the tooltip be custom?”             | `tooltip.formatter`, HTML, CSS, accessibility concern    |
| “Can the donut have text in the middle?” | custom renderer, annotation, or HTML overlay             |
| “Can labels avoid overlapping?”          | dataLabels settings, crop, overflow, rotation, formatter |
| “Can this animate nicely?”               | hope, caffeine, and `animation`                          |

### 3. Highcharts is powerful, but not always obvious

Highcharts is not hard because it lacks options.

It is hard because it has **many correct-looking places to put the wrong option**.

For example:

```ts
plotOptions: {
  column: {
    dataLabels: { enabled: true }
  },
  series: {
    dataLabels: { style: { fontWeight: 'normal' } }
  }
}
```

Then someone asks:

> “Why does this work on column charts but not line charts?”

And now the developer has to explain inheritance, chart-type-specific options, series-level overrides, and why the same visual concept may live in four different neighborhoods of the API.

Tiny config gremlins everywhere.

### 4. Designer iterates visually, developer iterates structurally

Designer feedback is often visual:

> “This feels too cramped.”

Developer has to find the exact technical lever:

```ts
chart: {
  spacingTop: 8,
  spacingRight: 12,
  spacingBottom: 8,
  spacingLeft: 12,
},
xAxis: {
  labels: {
    y: 18,
  },
},
legend: {
  itemMarginTop: 4,
  itemMarginBottom: 4,
}
```

Then the developer screenshots it, sends it back, and the designer replies:

> “Better, but now the labels feel floaty.”

The chart goblin receives another coin.

### 5. The real fight is usually not the chart itself

The hard part is rarely “make a bar chart”.

It is:

* responsive behavior
* small screens
* long labels
* missing data
* huge values
* tiny values
* negative values
* mixed series
* hover behavior
* keyboard accessibility
* screen reader text
* translations
* theme tokens
* export behavior
* dashboard/grid integration
* business-specific formatting
* “this must work in Danish, Finnish, Swedish, Norwegian, and English”

The mockup shows four perfect bars named “Alpha, Beta, Gamma, Delta”.

Production data arrives with:

```ts
'Aggregated tax-adjusted investment portfolio performance after estimated currency impact'
```

And the x-axis quietly bursts into flames.

### 6. The classic conversation

Designer:

> “Can we make it look exactly like this?”

Developer:

> “Mostly.”

Designer:

> “What does mostly mean?”

Developer:

> “It means I can make it visually equivalent, but not necessarily by using the same structure you imagined.”

Designer:

> “That sounds dangerous.”

Developer:

> “It is frontend.”

### 7. Best working pattern

The healthy version is not designer throwing Figma over the wall and developer spelunking alone.

Better pattern:

**Designer owns:**

* visual hierarchy
* color intent
* spacing intent
* states
* what should be emphasized
* what can be simplified

**Developer owns:**

* Highcharts feasibility
* API mapping
* responsive behavior
* accessibility
* data edge cases
* reusable config structure
* performance/export constraints

The sweet spot is a shared “chart design system” layer:

```ts
const baseChartTheme = {
  chart: {
    backgroundColor: 'transparent',
    spacing: [12, 12, 12, 12],
  },
  title: { text: undefined },
  credits: { enabled: false },
  legend: {
    itemStyle: {
      fontWeight: '400',
    },
  },
  tooltip: {
    useHTML: true,
  },
};
```

Then feature work becomes:

> “Use the standard donut variant with compact legend and currency tooltip.”

Instead of:

> “Please rediscover the chart underworld every sprint.”

### The tiny moral

Highcharts gives developers a giant, powerful cockpit.

Designers usually want a clean steering wheel.

Good teams build a small internal chart API between them, so nobody has to remember whether the answer lives in `series`, `plotOptions`, `xAxis.labels`, `tooltip.formatter`, `accessibility.point`, or the forbidden drawer marked `renderer`.


## user:
yeah, usually its finding our that the ux the designer envisions is totally non standard (after wracking their brains on the api pages, google, samples and attempting a few hack only to recall how the hacks always end up breaking after a year and create a super bad user experience as compared to following highcharts as a design system, not a frikin rat rod... so you then try to talk town the designer and offer some possible "less fancy" solutions

i mainly need a list of classic scenarios / tasks a developer goes through in order to plan a bit for building some tooling to aid the process



Exactly. The real workflow is not “how do I configure a chart?”

It is:

> “How many hours until we discover the beautiful mockup is secretly a custom canvas product disguised as a normal chart?”

Here’s a practical list of **classic developer scenarios/tasks** worth planning tooling around.

## 1. Design feasibility triage

The developer looks at the Figma and tries to classify the request:

| Scenario                    | Developer question                                                      | Tooling idea                               |
| --------------------------- | ----------------------------------------------------------------------- | ------------------------------------------ |
| Standard Highcharts pattern | “Is this just column/line/donut with theme tweaks?”                     | Detect chart type and map to known presets |
| Slightly custom but sane    | “Can this be done with official config?”                                | Suggest supported Highcharts options       |
| Possible but fragile        | “Would this need renderer hacks, overlays, DOM poking, or custom sync?” | Flag as “maintenance risk”                 |
| Not really a chart anymore  | “Is this actually a custom visualization?”                              | Recommend custom component or simpler UX   |
| Design-system mismatch      | “Does this fight Highcharts defaults?”                                  | Suggest design-system-aligned variant      |

This is probably the most valuable tool category: **“Is this a rat rod?” detector** 🐀🔧

## 2. “What API option controls this?” lookup

Classic task:

> “Where the hell do I change this one tiny thing?”

Examples:

| Design request       | Highcharts area                                                 |
| -------------------- | --------------------------------------------------------------- |
| Bars closer together | `plotOptions.column.pointPadding`, `groupPadding`, `pointWidth` |
| Rounded bar corners  | `borderRadius`                                                  |
| Hide y-axis title    | `yAxis.title.text`                                              |
| Soften grid lines    | `yAxis.gridLineColor`, `gridLineDashStyle`, `gridLineWidth`     |
| Custom tooltip       | `tooltip.formatter`, `pointFormatter`, `useHTML`                |
| Legend spacing       | `legend.itemMarginTop`, `itemMarginBottom`, `symbolPadding`     |
| Donut center text    | `title`, `subtitle`, renderer, or external overlay              |
| Label formatting     | `dataLabels.formatter`, `xAxis.labels.formatter`                |
| Hover state          | `plotOptions.series.states.hover`                               |
| Empty state          | app-level wrapper, sometimes `lang.noData` / no-data module     |

Tooling idea: a **design-intent-to-Highcharts-option dictionary**.

Not docs. More like:

> “Designer says X. Try these options first. Avoid these hacks unless desperate.”

## 3. Supported vs hacked implementation check

Classic developer pain:

> “I found a StackOverflow answer from 2018 that works, which means it is probably haunted.”

Tooling should classify approaches:

| Approach                                     | Risk            |
| -------------------------------------------- | --------------- |
| Pure Highcharts config                       | Low             |
| Official formatter callback                  | Low-medium      |
| Official events                              | Medium          |
| Custom HTML tooltip                          | Medium          |
| Renderer-added SVG                           | Medium-high     |
| DOM mutation after render                    | High            |
| CSS targeting generated Highcharts internals | High            |
| Overlay div synced to chart dimensions       | High            |
| Measuring text/axis positions manually       | Goblin contract |

Useful output:

```md
Implementation risk: Medium-high

Reason:
This requires custom SVG rendering tied to chart dimensions. It may break with responsive resizing, exporting, accessibility, or Highcharts upgrades.

Safer alternative:
Use standard title/subtitle/legend/dataLabels pattern.
```

That kind of thing would save many “future-you hates present-you” tickets.

## 4. “Can we make this less fancy?” alternative generator

This is the designer negotiation tool.

Input:

> “Designer wants floating animated labels inside each column with custom curved connectors and clickable mini-legends.”

Output:

| Fancy ask                        | Safer alternative                                       |
| -------------------------------- | ------------------------------------------------------- |
| Floating labels inside bars      | Standard data labels outside/inside with overflow rules |
| Custom curved connector lines    | Standard tooltip or legend interaction                  |
| Fully custom donut center widget | Static center value plus normal legend                  |
| Clickable label chips            | Use legend, table, or external filter controls          |
| Overlaid comparison badges       | Use annotations or adjacent summary cards               |
| Complex hover panel              | Use standard tooltip with limited HTML                  |
| Multi-layer axis labels          | Use shorter labels plus tooltip/full table              |

This is where tooling can act as a diplomatic foam sword:

> “Here are three supported UX options, ranked by polish vs maintenance cost.”

## 5. Figma-to-chart gap analysis

Classic task:

> “What in this design is actually not Highcharts-native?”

The developer scans for things like:

* labels that sit in physically impossible places
* tooltip layouts that behave like full cards
* legends acting like filter controls
* per-point custom icons
* custom axis grouping
* custom scrollbar behavior
* nested labels
* mixed chart/table hybrids
* center content in donut charts
* animated transitions beyond native Highcharts behavior
* responsive layouts that change chart semantics, not just size

Tooling idea: checklist output:

```md
Potential non-standard items:
1. Donut center content with multiple lines and icon
2. Legend uses custom pill buttons
3. Tooltip contains action button
4. X-axis labels are grouped by category
5. Mobile layout changes from chart to card list

Recommended handling:
- Keep chart standard.
- Move controls outside chart.
- Use separate summary component above/beside chart.
```

## 6. Data edge-case review

The design always uses angelic sample data.

The API meets actual banking/product data and starts chewing drywall.

Classic cases:

| Edge case               | What breaks                              |
| ----------------------- | ---------------------------------------- |
| Very long labels        | Axis layout, clipping, rotation ugliness |
| Many categories         | Bars become hairlines                    |
| Null/missing values     | Gaps, tooltip weirdness                  |
| Negative values         | Color logic, axis expectations           |
| Tiny + huge values      | Small values disappear                   |
| Many series             | Legend becomes furniture                 |
| One data point          | Chart looks broken                       |
| Zero values only        | Empty-looking chart                      |
| Translations            | Labels suddenly become novels            |
| Currency/percentage mix | Tooltip/axis confusion                   |
| Mobile width            | Everything collapses into soup           |

Tooling idea: generate **test datasets** for each chart type.

For example:

```ts
const chartEdgeCases = {
  longLabels,
  manyCategories,
  nullValues,
  negativeValues,
  extremeOutliers,
  singlePoint,
  allZero,
  translatedLongText,
};
```

Then developers/designers can preview the beast before it escapes.

## 7. Accessibility and semantics check

Classic task:

> “It looks fine, but does it explain itself to screen readers?”

Questions:

* Does the chart need a text summary?
* Are colors the only differentiator?
* Does the tooltip content exist elsewhere?
* Is keyboard navigation usable?
* Are labels readable at zoom?
* Is there an accessible data table fallback?
* Are chart updates announced?
* Does the chart title describe the purpose, not just the type?

Tooling idea: chart config linter/checklist:

```md
Accessibility review:
- Missing chart description
- Tooltip contains important values not repeated elsewhere
- Color-only distinction between positive/negative values
- No table fallback for dense data
```

## 8. Theme/design-token mapping

Classic task:

> “Which purple is this, and why are there seven?”

Problems:

* Figma color does not map to code token
* Highcharts default colors sneak in
* hover/disabled/inactive states ignored
* dark/light mode not considered
* grid/axis/label colors inconsistent
* chart colors clash with semantic colors

Tooling idea:

```ts
chartTheme = {
  textColor: token.text.primary,
  mutedTextColor: token.text.secondary,
  gridLineColor: token.border.subtle,
  positiveColor: token.semantic.positive,
  negativeColor: token.semantic.negative,
  palette: token.chart.palette,
};
```

Then generate chart presets from tokens instead of hand-painted config confetti.

## 9. Reusable preset selection

Instead of every feature inventing a new chart snowflake:

| Need                  | Preset                   |
| --------------------- | ------------------------ |
| Simple trend          | `lineTrendChart`         |
| Historical values     | `columnTimeSeriesChart`  |
| Category comparison   | `barComparisonChart`     |
| Allocation            | `donutAllocationChart`   |
| Performance breakdown | `stackedColumnChart`     |
| Dense data            | `chartWithTableFallback` |
| KPI trend             | `sparklineWithSummary`   |

Tooling idea: internal **chart recipe catalog**.

Each recipe should include:

* visual example
* supported use cases
* known limitations
* allowed customization knobs
* forbidden hacks
* accessibility requirements
* example data
* Highcharts config

## 10. “This should be outside the chart” detection

A lot of bad Highcharts hacks come from trying to make the chart do app UI work.

Classic offenders:

| Designer wants inside chart | Usually better outside   |
| --------------------------- | ------------------------ |
| Filter buttons              | App controls above chart |
| Download/export button      | Toolbar                  |
| KPI summary                 | Summary card             |
| Explanation text            | Caption/helper text      |
| Clickable legend pills      | Segmented control        |
| Empty state illustration    | App-level empty state    |
| Toggle between views        | App-level switch         |
| Data table                  | Separate table component |

Tooling should say:

> “This is not chart responsibility. Put it in the wrapper component.”

This alone prevents a surprising amount of chart goblinry.

## 11. Export/print behavior review

Hacks often work on screen and then explode when exported.

Classic checks:

* Does custom HTML tooltip matter for export?
* Does renderer content appear in exported SVG/PDF/PNG?
* Are external overlays missing from export?
* Do custom fonts render?
* Are colors still readable in print?
* Does responsive layout affect export size?

Tooling idea: risk flag:

```md
Export risk:
External HTML overlay will not be included in native Highcharts export.
Use Highcharts-native title/subtitle/annotations if export parity is required.
```

## 12. Upgrade-resilience check

This is the “will this break in a year?” scanner.

Red flags:

* CSS selectors targeting `.highcharts-...` internals
* DOM queries into chart container
* manual pixel positioning
* lifecycle timing hacks
* `setTimeout` after render
* mutating chart internals
* unsupported examples copied from old issues
* depending on undocumented properties
* too much logic in formatter callbacks

Tooling output could be brutal and useful:

```md
Upgrade resilience: Poor

Reason:
The implementation depends on generated DOM structure and manual pixel offsets.

Recommendation:
Replace with native dataLabels/annotations or move the custom UI outside the chart.
```

## 13. Developer implementation path planner

Given a request, tooling could produce:

```md
Recommended implementation path:

1. Start from preset:
   donutAllocationChart

2. Apply safe options:
   - plotOptions.pie.innerSize
   - dataLabels.enabled
   - tooltip.pointFormatter
   - legend.align

3. Avoid:
   - custom center renderer unless export is not required
   - DOM positioning inside chart container

4. Confirm with designer:
   - Is center content essential?
   - Can legend handle the secondary labels?
   - Is mobile allowed to use a table/list view?

5. Test with:
   - long fund names
   - 1 segment
   - 12 segments
   - zero values
   - Danish/Swedish labels
```

That is the workflow gold nugget: not just config, but **decision path**.

## 14. Designer conversation helper

Classic final stage:

> “I need to talk this down without sounding like I’m just saying no.”

Tooling could generate a practical designer-facing explanation:

```md
The current design needs custom behavior that Highcharts does not support cleanly. 
We can build it, but it would rely on manual positioning and custom overlays, which are likely to break with resizing, exporting, accessibility, or future Highcharts upgrades.

Recommended option:
Use the standard Highcharts legend and tooltip pattern, with a summary card above the chart for the extra visual content.

This keeps the UX stable, accessible, and easier to maintain.
```

Useful categories:

* “Supported as designed”
* “Supported with small adjustment”
* “Possible but fragile”
* “Recommend moving outside chart”
* “Recommend custom visualization instead”

## 15. “Known good examples” finder

Developers often search:

* docs
* Google
* StackOverflow
* random Highcharts demos
* old internal code
* previous feature branches
* cursed snippets from 2021

Tooling should prefer:

1. internal verified examples
2. official Highcharts demos
3. current Highcharts docs
4. internal chart presets
5. external examples only with suspicion goggles

The best version is a **verified snippet library** where every example has been rendered/tested.

## Core tooling buckets I’d build

The useful tooling probably falls into five buckets:

### A. Chart feasibility classifier

Input: design/request description
Output: standard / custom / fragile / not recommended

### B. Design-intent mapper

Input: “make labels less noisy”
Output: relevant Highcharts options and safe presets

### C. Internal chart recipe catalog

Input: “allocation donut”
Output: approved config, examples, edge cases, accessibility notes

### D. Hack-risk linter

Input: proposed config/code
Output: upgrade/accessibility/export/responsive risks

### E. Designer negotiation generator

Input: fancy design + risk result
Output: safer alternatives and wording to discuss trade-offs

## The recurring developer journey

This is probably the cleanest process map:

1. Identify chart purpose.
2. Match to existing internal chart recipe.
3. Compare design against native Highcharts behavior.
4. Flag non-standard parts.
5. Check data edge cases.
6. Check accessibility/export/responsive needs.
7. Estimate hack risk.
8. Offer supported alternatives.
9. Agree on “boring but robust” version.
10. Implement from preset, not from scratch.
11. Add edge-case demos/tests.
12. Document limitations so the next poor soul does not reopen the crypt.

The tooling goal is basically:

> turn “wrack brains through API/docs/samples/hacks” into “classify, map, warn, suggest, implement from known-good recipes.”

That gives developers a shield, designers a menu, and Highcharts fewer opportunities to become a taxidermied race car.


## User:
if one were to build a .agents/skills util for frontenders, what might be the most vital parts of such a system ?

For a `.agents/skills` utility aimed at frontend devs working with Highcharts, the most vital part is **not** “more Highcharts docs”.

The most vital part is a **decision system** that helps devs avoid turning charts into haunted furniture.

The skill should help answer:

> “Is this design standard, safely configurable, mildly custom, or are we about to build a rat-rod chart that will punish us later?”

## 1. Feasibility classifier

This is the crown jewel.

The skill should classify a chart/design request into clear buckets:

| Category                     | Meaning                                                     |
| ---------------------------- | ----------------------------------------------------------- |
| **Standard**                 | Can be built with normal Highcharts config                  |
| **Theme tweak**              | Mostly standard, needs styling/token mapping                |
| **Supported custom**         | Uses official APIs like formatters, events, annotations     |
| **Fragile custom**           | Needs renderer, overlays, DOM/CSS hacks, manual positioning |
| **Not chart responsibility** | Should be handled by wrapper UI, table, card, filter, etc.  |
| **Custom visualization**     | Highcharts may be the wrong tool                            |

Example output:

```md
Feasibility: Fragile custom

Reason:
The proposed centered multi-line donut content depends on manual positioning and may break with resizing, export, accessibility, or label overflow.

Recommended alternative:
Use a standard donut with legend + tooltip, and place the summary content in a separate card above the chart.
```

This gives the developer a shield in design discussions.

## 2. “Designer intent” mapper

Designers rarely say:

> “Please set `plotOptions.column.groupPadding` to 0.12.”

They say:

> “The bars feel too chunky.”

The skill should translate design language into API areas.

| Designer says                  | Skill maps to                                          |
| ------------------------------ | ------------------------------------------------------ |
| “Cleaner”                      | remove axis titles, reduce ticks, soften grid lines    |
| “Less noisy”                   | label density, muted colors, fewer data labels         |
| “More breathable”              | chart spacing, margins, legend spacing                 |
| “Softer bars”                  | border radius, point padding, colors                   |
| “Tooltip should feel designed” | standard HTML tooltip pattern, not full interactive UI |
| “Can labels sit here?”         | dataLabels, axis labels, annotation, or probably no    |
| “Mobile should look different” | responsive rules or external mobile layout             |

This should be a practical dictionary, not encyclopedia soup.

## 3. Approved chart recipe catalog

The skill should strongly prefer **internal recipes** over fresh inventions.

For example:

```md
recipes/
  line-trend.md
  spline-trend.md
  column-comparison.md
  bar-ranking.md
  stacked-column.md
  donut-allocation.md
  compact-sparkline.md
  chart-with-table-fallback.md
```

Each recipe should include:

```md
# Donut allocation chart

Use when:
- Showing proportional allocation
- Number of segments is small
- Values add up to a meaningful whole

Avoid when:
- More than ~8-10 segments
- Labels are long
- Values are not parts of a total
- User needs precise comparison

Supported customization:
- palette
- tooltip format
- legend placement
- inner size
- center label, only simple/static

Forbidden:
- interactive controls inside donut
- DOM-positioned center widgets
- clickable custom SVG labels
```

This makes the skill a design-system helper, not a config slot machine.

## 4. Hack-risk detector

The skill should actively warn against things frontend devs know will age like milk in a laptop bag.

Red flags:

```md
- CSS targeting generated `.highcharts-*` internals
- DOM queries into the chart container
- manual pixel offsets
- custom SVG renderer for layout-critical UI
- `setTimeout` after chart render
- external overlays synced to chart dimensions
- logic-heavy tooltip/dataLabel formatters
- undocumented Highcharts properties
- copying old StackOverflow snippets
- relying on current generated DOM structure
```

Suggested risk levels:

| Risk     | Examples                                                  |
| -------- | --------------------------------------------------------- |
| Low      | normal config, theme options, standard tooltip            |
| Medium   | formatter callbacks, events, annotations                  |
| High     | renderer-based custom layout, complex HTML tooltip        |
| Critical | DOM mutation, CSS against internals, manual sync overlays |

This is probably one of the most valuable parts because it catches the “works today, cursed tomorrow” stuff.

## 5. “Move it outside the chart” guidance

Many bad Highcharts hacks happen because people try to make the chart do general UI work.

The skill should recognize when something belongs in the wrapper component.

| Requested inside chart        | Better outside chart          |
| ----------------------------- | ----------------------------- |
| filter buttons                | app-level filters             |
| toggle controls               | segmented control above chart |
| KPI summary                   | summary card                  |
| explanatory text              | caption/helper text           |
| download button               | toolbar                       |
| clickable custom legend chips | app-level legend/filter       |
| empty state illustration      | wrapper empty state           |
| data table                    | separate table component      |
| loading/error state           | wrapper component             |

This should be one of the skill’s loudest opinions.

## 6. Edge-case test matrix

The skill should never judge the design only against perfect Figma data.

For each chart type, it should ask for or generate test cases:

```ts
const edgeCases = [
  'long translated labels',
  'many categories',
  'one data point',
  'all zero values',
  'null/missing values',
  'negative values',
  'huge outlier',
  'very small decimals',
  'many series',
  'mobile width',
  'dark mode',
  'screen zoom',
];
```

For banking/product dashboards, I’d especially include:

```md
- long fund/product names
- currency formatting
- percentages with decimals
- negative performance values
- mixed positive/negative values
- localized labels
- empty portfolio/account states
- delayed/loading data
```

The skill should produce:

```md
Required edge-case demos:
1. Long Danish/Swedish/Norwegian labels
2. 1 segment / 12 segments for donut
3. Zero values
4. Negative values
5. Mobile 320px width
```

Tiny chart gremlins love edge cases. Feed them early.

## 7. Accessibility checklist

This should be built in, not sprinkled later like parsley.

The skill should check:

```md
- Is the chart purpose described?
- Is there a text summary?
- Are colors the only way to understand meaning?
- Is keyboard navigation acceptable?
- Is tooltip-only information available elsewhere?
- Are chart updates announced or otherwise understandable?
- Is there a table fallback for complex data?
- Are labels readable at zoom and mobile sizes?
- Does the chart title explain the data, not just the chart type?
```

Suggested output:

```md
Accessibility concern:
The tooltip contains values that are not available elsewhere. Add a visible data table or accessible summary.
```

## 8. Export/print/responsive warnings

A lot of custom chart work survives the happy path and dies during export or resizing.

The skill should ask:

```md
- Is export required?
- Is print required?
- Should custom labels/content appear in exported PNG/SVG/PDF?
- Does mobile need the same chart or a simplified view?
- Are external overlays acceptable if they do not export?
```

Risk example:

```md
Export risk:
The proposed HTML overlay will not appear in native Highcharts exports. Use Highcharts-native title/subtitle/annotations, or accept export mismatch.
```

## 9. Internal design-token/theme mapping

The skill should discourage hand-painting charts.

Include a theme guide:

```ts
const chartTheme = {
  text: tokens.text.primary,
  mutedText: tokens.text.secondary,
  gridLine: tokens.border.subtle,
  positive: tokens.semantic.positive,
  negative: tokens.semantic.negative,
  neutral: tokens.semantic.neutral,
  palette: tokens.chart.palette,
};
```

The skill should say:

```md
Do not hardcode chart colors unless creating or updating an approved chart token.
```

And it should know which options are normally theme-level vs feature-level.

## 10. Safe implementation path generator

For any requested chart, the skill should produce a plan like:

```md
Recommended path:

1. Start from recipe:
   `donut-allocation`

2. Use official Highcharts options:
   - `plotOptions.pie.innerSize`
   - `tooltip.pointFormatter`
   - `legend.align`
   - `plotOptions.pie.dataLabels`

3. Put outside chart:
   - KPI summary
   - filter controls

4. Avoid:
   - custom renderer center widget
   - CSS targeting generated internals
   - DOM measurement hacks

5. Test:
   - long labels
   - 1 segment
   - 12 segments
   - zero values
   - mobile width
```

This is better than just dumping config.

## 11. Negotiation text for designers/product owners

This is surprisingly important.

The skill should help devs explain trade-offs without sounding like they are just blocking design.

Example:

```md
The design is possible, but not cleanly supported by Highcharts. To build it as shown, we would need custom positioning/overlay logic, which is likely to create issues with resizing, exports, accessibility, and future upgrades.

Recommendation:
Keep the chart itself close to the standard Highcharts pattern, and move the extra visual content into a separate summary component next to or above the chart.
```

Useful generated options:

```md
Option A: Standard, low risk
Option B: Slightly customized, acceptable risk
Option C: Full design fidelity, high maintenance risk
```

That gives designers a choice instead of a brick wall.

## 12. Verified examples only

This is where `.agents/skills` can become genuinely useful.

Have the skill rely on:

```md
examples/
  verified-column-basic.md
  verified-bar-ranking.md
  verified-donut-allocation.md
  verified-line-timeseries.md
  verified-spline-comparison.md
  verified-tooltip-html.md
  verified-accessibility-summary.md
```

Each example should say:

```md
Validated with:
- Highcharts version
- Rendered successfully
- Known limitations
- Screenshot or expected visual notes
```

Avoid letting the agent invent imaginary options. That is how config goblins breed.

## 13. Strong anti-hallucination rules

The skill should include explicit rules like:

```md
Never invent Highcharts option names.

If unsure:
- say which part is uncertain
- recommend checking the official API
- prefer a known internal recipe
- do not provide confident fake config
```

Also:

```md
When suggesting config, separate:
1. verified options
2. likely options needing validation
3. conceptual pseudo-code
```

That separation alone prevents a lot of “looks plausible, compiles never” AI sludge.

## 14. Skill structure I’d use

Something like this:

```text
.agents/
  skills/
    highcharts-frontend/
      SKILL.md
      recipes/
        column-comparison.md
        bar-ranking.md
        line-trend.md
        spline-trend.md
        donut-allocation.md
        chart-wrapper-pattern.md
      references/
        design-intent-map.md
        hack-risk-rules.md
        accessibility-checklist.md
        edge-cases.md
        theme-token-map.md
        export-responsive-risks.md
      examples/
        verified-column.ts
        verified-donut.ts
        verified-line.ts
      prompts/
        feasibility-review.md
        designer-negotiation.md
        implementation-plan.md
```

## 15. The most vital `SKILL.md` behavior

The main skill should force this workflow:

```md
1. Identify the chart purpose.
2. Match to an approved recipe.
3. Compare requested UX against native Highcharts behavior.
4. Flag non-standard or fragile parts.
5. Suggest safer alternatives.
6. Check accessibility, responsiveness, export, and edge cases.
7. Generate implementation plan.
8. Only then suggest config.
```

This ordering matters.

Bad flow:

```md
User asks for fancy chart
→ agent generates config
→ developer discovers it is cursed
```

Good flow:

```md
User asks for fancy chart
→ agent classifies feasibility
→ agent warns about cursed parts
→ agent suggests safe variants
→ agent generates config from approved recipe
```

## My “must-have” top 8

The absolute essentials:

1. **Feasibility classifier**
2. **Hack-risk detector**
3. **Approved chart recipes**
4. **Design-intent-to-API mapper**
5. **“Move outside chart” guidance**
6. **Edge-case test matrix**
7. **Accessibility/export/responsive checklist**
8. **Designer negotiation wording**

That turns the skill from “Highcharts helper” into a **chart design-system guardrail**.

The goal is not to help developers build any possible chart.

The goal is to help them build the chart that will still behave in production next summer, after three framework upgrades, two design refreshes, one accessibility audit, and a surprise PDF export requirement wearing a little hat.





