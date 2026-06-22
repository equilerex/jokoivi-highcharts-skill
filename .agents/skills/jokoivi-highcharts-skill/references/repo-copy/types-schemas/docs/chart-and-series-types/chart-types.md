Chart types
===========

Highcharts support a range of different chart types so data can be displayed in a meaningful way. Highcharts supports a long list of different chart types, among others `line`, `spline`, `area`, `areaspline`, `column`, `bar`, `pie`, `scatter`, `gauge`, `arearange`, `areasplinerange` and `columnrange`. For the full list of available chart types, see the API for Highcharts, Highcharts Stock, Highcharts Maps and Highcharts Gantt respectively.

To set a default chart type use:

```js
chart: {
    type: 'line'
}
```

Several chart types can also be combined in one chart using the type attribute on series to set different chart types for each series:

```js
series: [{
    type: 'line'
    data: []
},{
    type: 'column'
    data: []
}]
```

See Combining chart types for more information on how to combine chart types.

For more information on each chart type, see the left menu.
