Heatmap
===

A heat map is a graphical representation of data where the individual values contained in a matrix are represented as colors.

<iframe style="width: 100%; border: none; height: 500px;" src="" allow="fullscreen"></iframe>

### Setting up the heat map series

In Highcharts Core, load the heatmap module (modules/heatmap.js) to use heat maps. In Highcharts Maps, the heatmap functionality is built in, so you don’t need to load the module separately.

The heat map series is defined by setting the type to `heatmap`. A heat map has an X and Y axis like any cartesian series. The point definitions however, take three values, `x`, `y` as well as `value`, which serves as the value for color coding the point. These values can also be given as an array of three numbers.

### The color axis

Heat maps borrow a central concept from Highcharts Maps, the color axis. See the docs article on color axis for details

### Interpolation

Heat maps have an interpolation feature, which allows for displaying seamlessly transitioning data points. Check out the featured demo here.

### Resources

See the featured demos at Heat map and Large heatmap. The latter demonstrates how a HTML5 canvas can be plugged in to optimize rendering times.

See heatmap in the Highcharts Maps docs.
