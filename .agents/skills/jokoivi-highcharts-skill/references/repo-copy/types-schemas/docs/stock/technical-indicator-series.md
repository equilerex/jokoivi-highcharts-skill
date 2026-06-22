Technical indicators
===

Technical Indicators, like annotations, are powerful tools that help to understand charts and make decisions with ease. The mathematical algorithms use the existing data to indicate trends, events, etc. and help to set up boundaries for strategies and to look for patterns.

Technical indicators require the indicators/indicators.js main module. The main module includes SMA (Simple Moving Average). Each technical indicator, except the SMA, is a separate module and should be loaded after the main module.

A full list of supported technical indicators could be divided into two main groups. Overlays use the same scale and are plotted on the same xAxis and yAxis as the main series. The second group (oscillators and other technical indicators) requires additional yAxis because of the different extremes.


| Overlays  | Oscillators and others |
| ------------- | ------------- |
| Acceleration Bands | Absolute Price Oscillator |
| Bollinger Bands | A/D (Accumulation/Distribution) |
| DEMA (Double Exponential Moving Average) | Aroon |
| EMA (Exponential Moving Average) | Aroon Oscillator |
| Ichimoku Kinko Hyo | ATR (Average True Range) |
| Keltner Channels | Awesome Oscillator |
| Linear Regression | CCI (Commodity Channel Index) |
| Pivot Points | Chaikin |
| Price Channel | CMF (Chaikin Money Flow) |
| Price Envelopes | CMO (Chande Momentum Oscillator) |
| PSAR (Parabolic SAR) | Detrended price |
| SMA (Simple Moving Average) | Disparity Index |
| Super Trend | DMI (Directional Movement Index) |
| TEMA (Triple Exponential Moving Average) | Klinger Oscillator |
| Trendline | Linear Regression Angle |
| VbP (Volume by Price) | Linear Regression Intercept |
| VWAP (Volume Weighted Average Price) | Linear Regression Slope  |
| WMA (Weighted Moving Average) | MACD (Moving Average Convergence Divergence) |
| Zig Zag | MFI (Money Flow Index) |
| | Momentum |
| | NATR (Normalized Average True Range) |
| | OBV (On-Balance Volume) |
| | Percentage Price oscillator |
| | RoC (Rate of Change) |
| | RSI (Relative Strength Index) |
| | Slow Stochastic |
| | Stochastic |
| | TRIX (Triple exponential average) |
| | Williams %R |


_For more detailed samples and documentation check the API._

Technical indicators modules are implemented as series, that means almost all of the default options for [series](./chart-concepts/series) are available. The main option, which needs to be set for an indicator, is `series.linkedTo`. That option binds an indicator to a series: an indicator will use `series.data` for all calculations, even when the dataset is changing (e.g. by `series.addPoint()`). Additionally, each indicator has its own list of parameters, available under `params` options, which allows easy customization (e.g. `params.period`, `params.algorithm`).

There are no limitations to the number of technical indicators that can be bound to one main series. The following example creates a chart with four series: one main, two SMA, and one EMA:

```js
series: [{
  id: 'main-series',
  data: [ … ]
}, {
  type: 'sma',
  linkedTo: 'main-series',
  params: {
    period: 14
  }
}, {
  type: 'sma',
  linkedTo: 'main-series',
  params: {
    period: 28
  }
}, {
  type: 'ema',
  linkedTo: 'main-series',
  params: {
    period: 7
  }
}]
```

<iframe style="width: 100%; height: 650px; border: none;" src="" allow="fullscreen"></iframe>

Click here to check the code.

yAxis bindings
-------------

All Overlay type technical indicators (the ones listed in the left column of the above table, e.g. SMA, EMA, etc.) can be placed on the same yAxis as the main series. However, other technical indicators (right column, e.g. Oscillators: MACD, RSI, etc.), should use a separate yAxis. This is caused by values calculated by algorithms: yAxis extremes for the main series can be `<250, 255>` but for the Stochastic technical indicator, values are within `<0, 100>` extremes. A technical indicator can be placed on a separate yAxis as any other series:

1. Create required yAxis:

```js
yAxis: [{
  // Main series yAxis:
  height: '50%'
}, {
  // yAxis for Stochastic technical indicator:
  top: '50%',
  height: '50%'
}]
```

2. Bind indicator to this yAxis:

```js
series: [{
  id: 'main-series',
  data: [ … ]
}, {
  type: 'stochastic',
  linkedTo: 'main-series',
  yAxis: 1
}]
```

Multiple series bindings
------------------------

Some of the technical indicators require two series for calculations. Here is a full list of those indicators:

*   Accumulation/Distribution
*   Chaikin Oscillator
*   CMF
*   Klinger oscillator
*   MFI
*   OBV (On Balance Volume)
*   Volume by Price
*   Volume Weighted Average Price

These indicators require the following parameter `params.volumeSeriesID` to calculate properly:

```js
series: [{
  id: 'main-series',
  data: [ … ]
}, {
  id: 'volume-series',
  yAxis: 1,
  data: [ … ]
}, {
  type: 'mfi',
  linkedTo: 'main-series',
  yAxis: 2,
  params: {
    volumeSeriesID: 'volume-series'
  }
}]
```
