Patterns and contrast
===

The default palette of Highcharts is designed with accessibility in mind, so that any two neighbor colors are tested for different types of color blindness. In addition to that, there are a few ways to increase contrast, both for the visually impaired or for grayscale prints, but also for the charts to be more readable in general.

Keep in mind that you should not rely on color alone to provide information in the chart. Consider using data labels and/or the series-label module in addition.

## Examples
Below you will see some examples of different ways to increase contrast.

### Monochrome color palettes
Consider using monochrome color palettes.
<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

View demo code

### High contrast theme
Consider using a [high contrast theme](./chart-design-and-style/themes).
<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

View demo code

### Dash styles
Consider applying dash styles to line series. This will make lines distinguishable even on poor black/white prints. See the live demo of dash styles.

<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

View demo code

For more examples of dash styles, you can take a look at this demo showing the name of different dash styles:
 <iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>
 
View demo code

### Pattern fill
Consider applying a pattern fill to areas, columns or plot bands. This can be accomplished through the pattern fill module. Pattern fills can be very useful for distinguishing series visually, if correctly used. For more information, see our [documentation on pattern fills](./chart-design-and-style/pattern-fills).

```html
<script src=""></script>
```
  <iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

  View demo code



Keep in mind that pattern fills and dash styles could make your charts visually confusing and less accessible to some users, and that not all charts will be improved by adding these features. Subtle patterns are often preferred.

<iframe style="width: 100%; height: 470px; border: none;" src="" allow="fullscreen"></iframe>

Read more about [themes](./chart-design-and-style/themes) or [pattern fills](./chart-design-and-style/pattern-fills).
