# Appendix A: Option Component children

The table below shows what Highcharts option the child content of each option
component will be bound to.

| Component                                                                            | Highcharts API Option                                                          |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| [Title](./react/components/chart-elements/title)       | title.text                 |
| [Subtitle](./react/components/chart-elements/subtitle) | subtitle.text           |
| [Credits](./react/components/chart-elements/credits)   | credits.text             |
| [Tooltip](./react/components/chart-elements/tooltip)   | tooltip.format         |
| [XAxis](./react/components/chart-elements/x-axis)      | xAxis.title.text     |
| [YAxis](./react/components/chart-elements/y-axis)      | yAxis.title.text     |
| [Legend](./react/components/chart-elements/legend)     | legend.labelFormat |

## Advanced configuration

It is possible to change this binding by setting the `_HCReact.childOption`
property of the component.

```ts
import { Tooltip } from "@highcharts/react";

Tooltip._HCReact.childOption = "footerFormat";
```

The above will apply to all tooltip components.
