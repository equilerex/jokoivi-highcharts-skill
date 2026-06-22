Bullet chart
===

A bullet graph is a variation of a bar graph. The bullet series features a single measure, compares it to a target, and displays it in the context of qualitative ranges of performance, that could be set using plotBands on yAxis.

_For more detailed samples and documentation check the API._

<iframe style="width: 100%; height: 349px; border: none;" src="" allow="fullscreen"></iframe>

Click here to check the code.

How to create a bullet chart
----------------------------

Bullet series requires the following module “modules/bullet.js”.

To create a bullet series, add the following configuration in the series option:

```js
{
    type : 'bullet',
    data : [{
        y : 20,     // The value of a point
        target: 50  // The target value of a point
    }],
    targetOptions: { // Options related with look and position of targets
        width: '140%',        // The width of the target
        height: 3,            // The height of the target
        borderWidth: 0,       // The border width of the target
        borderColor: 'black', // The border color of the target
        color: 'black'        // The color of the target
    }
}
```

The `targetOptions` could be set for each point to create individual target options. On point level and even on series level the `targetOptions` are optional - default options will be set. The default options values can be found in the API reference.
