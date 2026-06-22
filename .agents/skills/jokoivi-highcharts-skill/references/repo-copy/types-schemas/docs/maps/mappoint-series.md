Map point series
================

A `mappoint` series is a special form of `scatter` series where points are laid out on top of a map using `lon` and `lat` coordinates.

<iframe style="width: 100%; height: 520px; border: none;" src="" allow="fullscreen"></iframe>

This allows us to place a marker on a specific position determined from mappoint.data. It is useful to mark any point of interest, like cities or the location of events in new stories. We can set these positions with the values of lat and lon coordinates.

It also supports setting the location as a geometry object. A geometry is directly compliant to GeoJSON feature collections and TopoJSON geometries, so that these can be used directly either as data or mapData.

<iframe style="width: 100%; height: 520px; border: none;" src="" allow="fullscreen"></iframe>

For generalization of dense map points, the marker-clusters module can be used. It interactively combines points into clusters which respond to zooming in and out or dynamically updating the data.

<iframe style="width: 100%; height: 520px; border: none;" src="" allow="fullscreen"></iframe>



API Reference
=============

You can find more available options and information in the API.
