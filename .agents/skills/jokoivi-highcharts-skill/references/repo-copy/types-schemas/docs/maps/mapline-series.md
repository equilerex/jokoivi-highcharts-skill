Map line series
===============

A `mapline` series is a special case of the map series where the value colors are applied to the strokes rather than the fills.
It can also be used for freeform drawing of lines in the map.

<iframe style="width: 100%; height: 520px; border: none;" src="" allow="fullscreen"></iframe>

Configuration
-------------

To create a `mapline` series, set the series `type` to
mapline. More information
about data formatting and available options can be found in the
API. As you can see
in the demo above we can create a `mapline` series in combination with a standard
`map` series, then plot our shape data via the
geometry options. To achieve a better
separation between the structure and the data, it is recommended to use
mapData to define
the `geometry` instead of defining it on the data points themselves.

The geometry object is compatible to that of a `feature` in GeoJSON, so features of GeoJSON can be passed directly into the `data`, optionally after first filtering and processing it.


A more advanced demo with customized line shapes to indicate flight routes
--------------------------------------------------------------------------

<iframe style="width: 100%; height: 520px; border: none;" src="" allow="fullscreen"></iframe>
