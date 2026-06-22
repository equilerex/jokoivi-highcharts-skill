3D pyramid
===

Pyramid 3D series type is a 3D variant of the Pyramid Chart. It represents data in the same way as a [Funnel Chart](./chart-and-series-types/funnel-series) but reversed and without a neck width and neck height. Use this chart type for displaying percentage ratio or for visualizing volumes in different phases.

<iframe style="width: 100%; height: 532px; border: none;" src="" allow="fullscreen"></iframe>

Setting up
----------

Pyramid 3D is part of the Highcharts library. Load first `highcharts.js` and then sequentially the following files: `highcharts-3d.js`, `modules/cylinder.js`, `modules/funnel3d.js`, and `modules/pyramid3d.js`.

The 3D perspective will be enabled by setting `options3d.enabled` to true.

Series type could be set on chart level or in series options.

Configuration options
---------------------

Each segment of the 3d pyramid has a height that relates to the data point’s value. The size of the pyramid fills the plot area by default but can be configured by setting the `width` and `height` properties.

See the API for all other options related to the Pyramid 3d Chart.
