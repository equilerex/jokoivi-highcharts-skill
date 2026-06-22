Getting started with Highcharts Maps
===

Highcharts Maps is Highcharts for geo maps. Highcharts Maps supports [tiled web maps](./maps/tiledwebmap) with external tile providers, and [choropleth maps](./chart-concepts/dataviz-glossary#choropleth-map) where the color intensity relates to some value of a geographic area. It also supports different features like lines (roads, rivers etc.) and points (cities, points of interest) and more, and is closely tied up to the standard TopoJSON and GeoJSON formats. Highcharts Maps comes in two flavors, either as a standalone JavaScript file, or as a plugin for Highcharts.

Load the required files
-----------------------

For basics, see Highcharts installation. The framework requirements and installation is the same for Highcharts Maps as for Highcharts. To load Highcharts Maps as a standalone product (if you don't have a license for Highcharts), include this script tag:


```html
<script src=""></script>
```

If you already have Highcharts installed in the web page and want to run Highcharts Maps as a plugin, include this script tag _after_ `highcharts.js`:

```html
<script src=""></script>
```

Load the map
------------
For working with tiled web maps, see [the documentation article](./maps/tiledwebmap).

For maps based on geometry objects, Highcharts Maps loads its maps from TopoJSON or GeoJSON which are open standards for description of geographic features. Most GIS software supports these formats as export from for instance Shapefile or KML export. Read more in the API reference and see the live demo.

There are three basic sources for your geometry-based map:

1.  Use our Map collection. Read the tutorial article on the map collection to get started.
2.  Find an SVG map online and convert it using our (experimental) online converter. 
3.  Create your own map from scratch using an SVG editor, then convert them online. Read our tutorial on [Custom maps for Highcharts Maps](./maps/create-custom-maps).

Initialize the map
------------------

Read more on initializing a chart in Your first chart. The map is constructed with the `Highcharts.mapChart` constructor:

```js
    Highcharts.mapChart('container', {
       ...
    });
```

Add and join data for choropleth maps
-------------------------------------

Tiled web maps do not load data, as they work like a layer with a tile background.

Other series types, like the choropleth `map` series, typically rely on a GeoJSON or TopoJSON map source with geometric information. Once the empty map is in place, we're ready to add the data to the series.data option. For the joining to work, each data point must have some identifier that relates to the same identifier in the map data set. This or these identifiers are then specified in the joinBy option. See detailed documentation and examples there.

Another way to join the data is to simply skip the `mapData` and set the geometry directly on the data point. This mixes the data and the structure and is not generally recommended, but it performs faster, and may be considered in situations where you have static data and a backend to perform the joining.

<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>
