Tables
===

Including the export-data module will enable viewing the chart as a data table. This module also requires the exporting module.

```html
<script src=""></script>
<script src=""></script>
<script src=""></script>
```

There are three different ways to access the data table:
1. Clicking the export menu and then "Show data table".
2. A hidden button for screen reader users to access the table before the chart.
3. You can set the option `exporting.showTable`. The table will then show up when the page is rendered.

```js
Highcharts.chart('container', {
    exporting: {
        showTable: true,
    }
    // ...
});
```

<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

View demo code

Note that simply showing the chart data as a table is not considered a sufficient accessible alternative to a chart, and you should still enable the Accessibility module unless there is a specific reason not to do so.

See our [data-module documentation article](./working-with-data/data-module) for more information on the data module and working with tables in Highcharts.
