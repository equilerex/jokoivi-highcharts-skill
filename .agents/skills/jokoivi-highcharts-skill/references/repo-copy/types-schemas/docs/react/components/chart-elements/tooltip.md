# Tooltip

You can customize the [chart tooltip](./chart-concepts/tooltip) using the `Tooltip` component:

```tsx
import { Chart, Tooltip } from "@highcharts/react";
import { LineSeries } from "@highcharts/react/series/Line";

export default function TooltipChart() {
  return (
    <Chart>
      <Tooltip>{"<b>{series.name}</b>: {point.y} USD"}</Tooltip>
      <LineSeries data={[3, 4, 1, 5, 2]} />
    </Chart>
  );
}
```

The `Tooltip` component accepts all tooltip API options as props. The tooltip format can be passed as `children`.

**Note:** For a more structured tooltip, it's a good practice to use the `data-hc-option` attribute to map child elements to specific tooltip options. See the [Option binding](./react/options-component-format#option-binding) documentation for more details.
