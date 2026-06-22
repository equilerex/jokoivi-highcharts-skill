# Credits

You can customize the chart credits using the `Credits` component:

```tsx
import { Chart, Credits } from "@highcharts/react";
import { LineSeries } from "@highcharts/react/series/Line";

export default function CreditsChart() {
  return (
    <Chart>
      <Credits href="">Credits text</Credits>
      <LineSeries data={[3, 4, 1, 5, 2]} />
    </Chart>
  );
}
```

The `Credits` component accepts all credits API options as props. The credit text can be passed as `children`.
