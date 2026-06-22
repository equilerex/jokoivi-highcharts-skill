Advanced accessibility configuration
===

The Accessibility module is highly configurable. While the goal of the module is to provide the most accessible charts possible out of the box, it can sometimes be advantageous or necessary to make changes to the configuration.

The most important configuration for the module is the text description. Read more about the [basic configuration of the chart](./accessibility/accessibility-module#basic-configuration).


Configuration of screen reader behavior
---------------------------------------

Any text exposed to a screen reader in Highcharts can be configured. The most common configurations are outlined below, but for a complete overview, please refer to the Accessibility API options and the Accessibility language options. Note that several individual chart elements also have configurable accessibility options, including series, legend, and the chart exporting menu.

### Information region before the chart

To configure the information text that is exposed to screen readers before the chart, refer to the `accessibility.screenReaderSection.beforeChartFormat` option. The format string is used to generate basic HTML with the information text.

See example:

```js
Highcharts.chart('container', {
    accessibility: {
        screenReaderSection: {
            beforeChartFormat: '<h5>{chartTitle}</h5>' +
                '<div>{typeDescription}</div>' +
                '<div>{chartSubtitle}</div>' +
                '<div>{chartLongdesc}</div>' +
                '<div>{viewTableButton}</div>'
        },
    },
    // ...
});
```
<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

View demo code

If more detailed control is required, the `accessibility.screenReaderSection.beforeChartFormatter` option allows for defining a function to return the HTML string, receiving the chart as an argument.

### Individual data points

To configure what screen readers read out for individual data points, see the `accessibility.point.valueDescriptionFormat` option. You can then easily configure what values you want to show to the user. Example:

```js
Highcharts.chart('container', {
    accessibility: {
        point: {
            valueDescriptionFormat:
            'On {xDescription}, there were {point.y}'
        }
    }
    // ...
});
```

<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

View demo code

If more detailed control is required, the `accessibility.point.descriptionFormatter` option allows for specifying a function to return the entire description of the point, receiving the point as an argument.

Example:

```js
Highcharts.chart('container', {
   accessibility: {
        point: {
            descriptionFormatter: function (p) {
                return p.series.name + ', ' + p.category + ', ' + p.y + '°F.';
            }
        }
    },
    // ...
});
```
<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

View demo code

### Prefixes and suffixes
Options are also available for specifying value prefixes and suffixes. Uses `tooltip.valueSuffix` if not defined.

```js
Highcharts.chart('container', {
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    // ...
});
```

Example with `tooltip.valueSuffix`:
<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

View demo code

### Additional text descriptions

Note that you can also provide additional text descriptions for individual points and series using `point.accessibility.description` and `series.accessibility.description`. This description is by default added to the existing description of the point/series, and can be useful to highlight points or series of interest. 
```js
Highcharts.chart('container', {
    series: [{
        name: 'Percentage usage',
        data: [{
            name: 'JAWS',
            y: 30.2,
            accessibility: {
                description: 'This is the most used desktop screen reader'
            }
        }, 
        //..
    }]
    // ...
});
```

<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

View demo code

*Compatibility note:* Some of the options above, such as `valueDescriptionFormat`, were not available until Highcharts v8.0.0. Prior versions should use `accessibility.pointDescriptionFormatter` and `accessibility.seriesDescriptionFormatter` functions, corresponding to the current `accessibility.point.descriptionFormatter` and `accessibility.series.descriptionFormatter` options.


Large data series
-----------------

Be aware that for charts with a large set of data points, individual data points are not by default exposed to screen reader users. This can be configured with the `accessibility.series.pointDescriptionEnabledThreshold` option.

```js
Highcharts.chart('container', {
    accessibility: {
        series: {
            pointDescriptionEnabledThreshold: 1
        }
    },
    // ...
});
```
<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

View demo code

It is possible to set a similar threshold for keyboard navigation, but this is disabled by default.

It is also always possible to expose a data series as a group only - without exposing the individual data points - by using the `series.accessibility.exposeAsGroupOnly` option. 

```js
Highcharts.chart('container', {
    series: [{
        accessibility: {
            exposeAsGroupOnly: true,
            descriptionFormat: 'Emma did not reach her step goal which was ' +
                '70000 steps in one week. She walked {sum} steps.'
        },
        // ..
    }]
    // ...
});
```
<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

View demo code

For large data series, [sonification](./sonification/getting-started) can be a great tool for making trends and patterns more accessible to screen reader users.

<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

View demo code

Axis configuration
------------------

Highcharts will by default describe a chart's axes and their ranges to screen reader users. The axes will by default be described by their titles, but this title can be overridden by setting the `axis.accessibility.description` option.

The overall description format can be set in the various axis `lang.accessibility` options, see for example `lang.accessibility.axis.xAxisDescriptionSingular`.

The range description for an axis can be overridden by setting the `axis.accessibility.rangeDescription` option.

Example of setting the [`axis.accessibility.rangeDescription`] and [`axis.accessibility.description`]
```js
Highcharts.chart('container', {
     yAxis: {
        accessibility: {
            description: 'Daily steps in total for all three persons',
            rangeDescription: 'Ranges from 22214 steps to 33730 steps'
        },
    },
    // ...
});
```

<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

View demo code

See more demos using the Accessibility module.
