Column chart
============

Column charts display data as vertical bars. A feature of column charts allows for different data to be compared alongside one another.
It is similar to bar charts, the difference being that bar charts have a horizontal representation of the data.

<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

The column chart has the same options as a series. For an overview of the column chart options see the API reference.

Histogram
---------

Column charts can be used to make histogram charts by setting the padding between points and groups to 0.

```js
    plotOptions: {
        column: {
            pointPadding: 0,
            borderWidth: 0,
            groupPadding: 0,
            shadow: false
        }
    }
```

Note that borderWidth and shadows are also turned off in the example so the columns do not overlap.

Stacked Column chart
--------------------
An essential feature of column charts is to represent data as stacked columns. Read more about [stacking charts](./advanced-chart-features/stacking-charts).

<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>
