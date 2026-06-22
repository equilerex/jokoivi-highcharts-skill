Getting started with Highcharts Stock
===

Highcharts Stock allows to create financial and general timeline charts for your web and mobile applications. Features sophisticated navigation for high-volume data, user annotations, advanced data grouping and over 40 built-in [Technical Indicators](./stock/technical-indicator-series).

Find demos of Highcharts Stock charts here to quickly get an overview of its capabilities.

Get started
-----------

Example of loading Highcharts Stock into a webpage as a standalone library when there is no need for other Highcharts dependencies:

```html
<script src=""></script>
```
Load Highcharts Stock as a module when a project needs both Highcharts and Highcharts Stock loaded at the same time. Place the script tag or import statement after loading the main library:

```html
<script src=""></script>
<script src=""></script>
```
For alternative loading and bundling patterns, for UMD, AMD, CommonJS or ES6 modules, find more information here. Highcharts Stock follows the same patterns as described for Highcharts.

Constructor
-----------

Run the `stockChart` constructor for initializing a Stock chart visualization. The constructor takes two required parameters (container ID and a config object) and a third optional parameter, which is the callback function run after the chart has loaded.

```js
Highcharts.stockChart(containerID, {
    // configuration options object
}, callback);
```

1.  `containerID:` The HTML element used for rendering the chart.
2.  `config`: An object with configuration options for defining the Stock chart.
3.  `callback`: (Optional) A callback for getting a handle on the chart once it's loaded.

See also explained here in Stock API

Basic example
--------------

To create your first basic stock chart, all you need to do is to define the dataset appropriate for the series type that you choose. The default series type is a line series.

That's all you need to get started with Highcharts Stock:

```js
Highcharts.stockChart('container', {
    series: [{
        data: [1, 2, 3]
    }]
});
```

Instead of hardcoded data, see how you can use the data from external API/database below.

<iframe src="" width="100%" height="400" allow="fullscreen"></iframe>


<br />

Learn more about Stock specific chart features at [Understanding Highcharts Stock](./stock/understanding-highcharts-stock).
