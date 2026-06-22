Understanding Highcharts Stock
===

Highcharts Stock is based on Highcharts, meaning it has all the core functionality of Highcharts, plus some additional features.

![understanding_highstock.png](understanding_highstock.png)

Highcharts Stock also supports various financial series types.

<iframe style="width: 100%; height: 540px; border: none;" src="" allow="fullscreen"></iframe>

```js
chart.series[0].update({
    type: 'candlestick'
});
```

See Update series method and series API options.

Navigator and scrollbar
---------

Allows you to fine tune the range of the chart which is displayed and scroll through it.

See Navigator for more information.

<iframe style="width: 100%; height: 610px; border: none;" src="" allow="fullscreen"></iframe>

```js
chart.update({
    navigator: {
        enabled: true,
        height: 100
    },
    scrollbar: {
        enabled: false
    }
});
```
To update navigator and scrollbar use Chart update. See navigator API options.


Range selector
--------------

Allows you to quickly select a range to be shown on the chart or specify the exact interval to be shown.

<iframe style="width: 100%; height: 540px; border: none;" src="" allow="fullscreen"></iframe>

See Range selector for more information.

```js
chart.update({
    rangeSelector: {
        enabled: true
    }
});
```

To update range selector use Chart update. See range selector API options.

Crosshair
---------

Shows a line perpendicular to the corresponding axis which is following the mouse position or nearest point, depending on the `crosshair.snap` property. This functionality can be found in the axis API options. Crosshairs can also be used in Highcharts Core (without Stock module), but are not enabled by default.

<iframe style="width: 100%; height: 570px; border: none;" src="" allow="fullscreen"></iframe>

```js
chart.xAxis[0].update({
    crosshair: {
        snap: false
    }
});
```

Crosshair is an axis property, therefore update it via Axis update. See axis API options.

Data grouping
---------

Automatically groups multiple points into a single point to improve readability. The displayed value for a grouped point depends on the approximation function which is set by default depending on the series type, but can be manually overwritten. The amount of points in a single group is selected based on the zoom level, data density and user options.

<iframe style="width: 100%; height: 600px; border: none;" src="" allow="fullscreen"></iframe>

See [Data grouping](./stock/data-grouping) for more information.

```js
chart.series[0].update({
    dataGrouping: {
        groupAll: true
    }
});
```

Data grouping is a series property, therefore update it via Series update. See data grouping API options.
