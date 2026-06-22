Map View and Projection
===

The map view is the basic class and options set dealing with how the map is projected and displayed inside the chart.

 * API options
 * Class reference

### Center and zoom
By default, a map is centered within the plot area of the chart. For custom zoom and placement, use the center and zoom options, where `center` is given as `[longitude, latitude]` and `zoom` is a number where 0 renders the world as 256x256 pixels, and increase of 1 zooms in to a quarter of the viewed area.

<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

The center and zoom options can be updated in run time by the setView function.

### Projection
The map view also controls the map's projection settings. Highcharts Maps includes some basic built-in projections, other projections can be custom built and plugged in. By default, Highcharts will guess the best projection to use for a map, based on the geographic extent. For more details see the API docs or try out the Projection Explorer below.

<iframe style="width: 100%; height: 900px; border: none;" scrolling="yes" src="" allow="fullscreen"></iframe>

### Insets
Insets are small maps that are inset in parts of the main map. Highcharts Maps typically uses insets for rendering non-contiguous areas of a country closer to the mainland. Examples are Alaska and Hawaii for the USA, or the France map with multiple overseas territories. Many of the TopoJSON maps of the Map Collection come with built-in recommended `mapView` settings, where insets are included. These recommended insets can all be overridden by supplying options with the same `id`. By overriding them, the insets can for example be placed in different areas of the main map. For more details, see the general insetOptions and the item specific insets.

<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

### Coordinate systems
A map view operates with three different coordinate systems:

* The geographic coordinates
* The projected plane on which the geographic coordinates are projected, and
* The pixel positions within the plot area, onto which the projected plane is scaled and translated.

The MapView class contains conversion functions between these coordinate systems. In addition to that, all pointer events are extended with `lon` and `lat` properties, allowing longitude and latitude to be read directly from for example a click event.

