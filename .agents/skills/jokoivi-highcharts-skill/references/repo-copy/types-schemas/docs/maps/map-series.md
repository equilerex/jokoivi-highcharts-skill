Map series
==========

The `map` series is the basic series type in Highcharts Maps. It creates a
[choropleth map](./chart-concepts/dataviz-glossary#choropleth-map) offering
the ability to create map shapes and visualize their values through color coding
or patterns.

<iframe style="width: 100%; height: 520px; border: none;" src="" allow="fullscreen"></iframe>

Initialize the constructor
--------------------------

When setting the `mapChart` constructor, the default series `type` is `map`.
If the `type` option is not specified, it is inherited from `chart.type`.
For an overview of the `map` series options see the API reference.

```js
Highcharts.mapChart('container', {
   // ...
});
```

<iframe style="width: 100%; height: 520px; border: none;" src="" allow="fullscreen"></iframe>

Load the map
------------
Highcharts Maps loads its maps from TopoJSON or GeoJSON.
A more detailed instruction on how to work with it is written here: [Load the map](./maps/getting-started#load-the-map)

Add and join data
-----------------
In this [link](./maps/getting-started#add-and-join-data), you can find detailed descriptions of how to work with series.map.data, and series.joinBy.

You can also find there another way of joining the data by omitting mapData and setting the path directly on the data point.
