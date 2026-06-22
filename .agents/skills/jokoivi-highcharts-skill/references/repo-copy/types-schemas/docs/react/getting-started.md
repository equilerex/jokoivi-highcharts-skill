# Getting started

## Requirements

The release has been tested with:

- The Highcharts npm package version 12.0.0 and newer
- Vite with plugin-react version 4.3.3 and newer
- React and react-dom version 18.3.1 and newer

## 1. Install Highcharts React

Install Highcharts React by running:

```sh
npm install @highcharts/react
```

> **Note:** Highcharts is included as a peer dependency and is installed automatically with npm v7+.

## 2. Create your chart

Start by creating a simple chart using a series component:

```tsx
import { Chart } from "@highcharts/react";
import { LineSeries } from "@highcharts/react/series/Line";

export default function LineChart() {
  return (
    <Chart>
      <LineSeries data={[3, 4, 1, 5, 2]} />
    </Chart>
  );
}
```

## 3. Customize your chart

Highcharts React provides dedicated React components for chart elements and modules to customize your chart.

### Chart elements

You can use element components to shape your chart structure:

```tsx
import { Chart, Title, Legend } from "@highcharts/react";
import { ColumnSeries } from "@highcharts/react/series/Column";

export default function ColumnChart() {
  return (
    <Chart options={{ chart: { className: "column-chart" } }}>
      <Title>Column chart</Title>
      <Legend>{"{index}: {name}"}</Legend>
      <ColumnSeries data={[3, 4, 1, 5, 2]} name="Column series" color="red" />
    </Chart>
  );
}
```

Learn more about the concepts used:

- See the [Chart](./react/components/chart) documentation to configure your chart.
- See the [Series types](./react/components/series-types) documentation to work with different series types.
- See the [Legend](./react/components/chart-elements/legend) documentation as an example of working with chart elements.

The result should look like this:

<iframe src="" title="Basic Highcharts React chart example"></iframe>

### Modules (optional)

You can use module components to load additional Highcharts modules:

```tsx
import { Chart } from "@highcharts/react";
import { LineSeries } from "@highcharts/react/series/Line";
import { Accessibility } from "@highcharts/react/modules/Accessibility";
import { Exporting } from "@highcharts/react/modules/Exporting";

export default function ModulesChart() {
  return (
    <Chart>
      <Accessibility />
      <Exporting />
      <LineSeries data={[3, 4, 1, 5, 2]} />
    </Chart>
  );
}
```

> **Note:** Each component automatically includes the corresponding Highcharts module.

To explore modules with dedicated components, see the [Module components](./react/components/modules/accessibility) documentation. If a module doesn't have a dedicated component, we recommend importing it directly from Highcharts using its ESM version:

```tsx
import { Chart, YAxis } from "@highcharts/react";
import { ScatterSeries } from "@highcharts/react/series/Scatter";

import "highcharts/es-modules/masters/modules/marker-clusters.src.js";

export default function MarkerClustersChart() {
  return (
    <Chart>
      <YAxis min={0} max={10} />
      <ScatterSeries
        data={[
          [1, 4],
          [1, 5],
          [1, 6],
        ]}
        cluster={{ enabled: true }}
      />
    </Chart>
  );
}
```

> **Note:** For more information on ESM imports, see the [Bundling and tree shaking](./react/bundling-and-tree-shaking) documentation.
