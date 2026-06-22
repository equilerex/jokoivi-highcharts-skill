TiledWebMap
==========

Tiled web map, in short TWM, allows users to dynamically create maps from small (most often 256x256 pixels) images called tiles, that are dynamically pulled from a third party provider's server by using a custom URL. These tiles are later joined and displayed seamlessly as a Highcharts map.


<iframe style="width: 100%; height: 520px; border: none;" src="" allow="fullscreen"></iframe>

Configuration
--------------------------

In order to use the `tiledwebmap` series as a base map, firstly import the `tiledwebmap.js` module.

```html
<script src=""></script>

```
Secondly, set the series type to `tiledwebmap`. The tiled web map series can be considered a map layer. It does not require any data or GeoJSON geometry to run. The implementer only has to specify which provider should be used to fetch the tiles from. This series doesn’t have information about what region we want to focus at, so in most cases the implementer wants to set either mapView.center and mapView.zoom or mapView.fitToGeometry or add another series with geometry data, which will calculate the proper bounds for the map view. There are additional options such as a theme for the tiles, a subdomain for the provider’s URL and an API key if needed.

Sample code:

```js
series: [{
    type: 'tiledwebmap',
    name: 'Basemap Tiles',
    provider: {
        type: 'OpenStreetMap',
        theme: 'Standard',
        subdomain: 'a'
    }
}]

```
Alternatively, you can enter your own URL template, and omit all of the aforementioned properties. The URL has to include variables for `{x}`, `{y}` and `{z}`/`{zoom}` in a given format.

```js
series: [{
    type: 'tiledwebmap',
    url: '{x}/{y}/{z}.png'
}]

```
Generally in Highcharts Maps, the series array can be thought of as layers that are stacked on top of each other, and the ordering of the layers is determined by source order and can be overridden through the index option or the zIndex option.

<iframe style="width: 100%; height: 520px; border: none;" src="" allow="fullscreen"></iframe>

Providers properties
------------
Highcharts by default supports the following tile providers: `OpenStreetMap`, `Thunderforest`, `Esri`, `Stamen`, `USGS` and `LimaLabs`. Each provider has their own themes and possible subdomains. Tiles are provided in a specific map projection, usually it is a WebMercator projection.

Providers supported natively by Highcharts force map chart configuration to set an appropriate map projection. If the user sets their own projection, which is not supported, there will be a warning in the console and tiles might not load properly. Other providers can be added by using a custom URL in the `provider.url` property or another provider can be custom built and plugged in.

Available providers
------------
* `OpenStreetMap`

    OpenStreetMap (OSM) is a free, open geographic database updated and maintained by a community of volunteers via open collaboration. URL: 

    Available properties:

    ```js
        theme: 'Standard’, ‘Hot’, ‘Mapnik’, ‘OpenTopoMap’
        subdomain: ‘a’, ‘b’, ‘c’
    ```
* `Thunderforest`

    Thunderforest is a global provider of thoughtfully-created activity maps. URL: 

    Available properties:

    ```js
    theme: ‘OpenCycleMap’, ‘Transport’, ‘TransportDark’, ‘SpinalMap’, ‘Landscape’, ‘Outdoors’, ‘Pioneer’, ‘MobileAtlas’, ‘Neighbourhood’
    subdomain: ‘a’, ‘b’, ‘c’

    ```
* `Esri`

    Esri is the global market leader in geographic information system (GIS) software, location intelligence, and mapping. URL: 

    Available properties:

    ```js
    theme: ‘WorldStreetMap’, ‘DeLorme’, ‘WorldTopoMap’, ‘WorldImagery’, ‘WorldTerrain’, ‘WorldShadedRelief’, ‘WorldPhysical’, ‘NatGeoWorldMap’, ‘WorldGrayCanvas’, ’WorldDarkGrayCanvas’
    ```
* `Stamen`

    Stamen is a San Francisco design and development studio focused on data visualization and map-making. Stamen heavily uses OpenStreetMap data in many of their map visualizations, and their developers have worked on many important tools and product offerings around OpenStreetMap.
    URL: 

    Available properties:

    ```js
    theme: ‘Toner’, ‘TonerBackground’, ‘TonerLite’, ‘Terrain’, ‘TerrainBackground’, ‘Watercolor’
    subdomain: ‘a’, ‘b’, ‘c’, ‘d’
    ```
* `USGS`

    The United States Geological Survey (USGS), formerly simply known as the Geological Survey, is a scientific agency of the United States government.
    URL: 

    Available properties:

    ```js
    theme: ‘USTopo’, ‘USImagery’, ‘USImageryTopo’
    ```
* `LimaLabs`

    LimaLabs provides tiles as free for any user needing < 20,000,000 tiles yearly. URL: 


    Available properties:

    ```js
    theme: ‘Standard’
    ```
API Reference
-------------
For an overview of the `tiledwebmap` series options see the API reference.
