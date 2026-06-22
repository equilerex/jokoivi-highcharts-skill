Client side export
===

### Local exports by default

Starting from version 12.3.0, the exporting.js module handles exports to PNG, JPEG and SVG formats locally by default, without requiring the offline-exporting.js module. This behavior is controlled by the exporting.local option, which is set to `true` by default.

Offline exporting logic allows for image export of charts without sending data to an external server. This is the solution if you:

*   Want to avoid having users send your chart configs to Highsoft's servers
*   Want to save the cost of setting up your own server
*   Don't require the export to work with old browsers

View it live on jsFiddle.

Setting the exporting.local to `false` will send export requests to the remote export server.

### The offline-exporting module

The only exception, which requires the offline-exporting.js module for local export, is the **PDF format**.

The module makes use of modern browser technology to accomplish this, and therefore does not work flawlessly with older browsers. For a detailed table of supported browsers, see below. In the case of an unsupported browser, the module will by default fall back to the export server, but this can be disabled with the exporting.fallbackToExportServer option.

Additionally, Internet Explorer requires the canvg library in order to export to PNG and to export charts with embedded images. PDF export also requires the jsPDF and svg2pdf for all browsers. Highcharts will only load these files on demand when exporting.libURL is explicitly set. Otherwise, include the scripts on the page yourself. If the scripts have already been loaded by the page, Highcharts will not load them again. Note that even when loading these files, no chart data is sent to our server.

PDF does not support exporting with images and will fall back to the export server.

*Note*: PDF export in the client-side export module is an opt-in feature. Enabling local PDF export (for example, by adding `downloadPDF` to `contextButton.menuItems`) requires external third-party libraries. These libraries are not provided, licensed, or warrantied under the Highcharts license and Highcharts cannot take responsibility for their security or maintenance.

To use the module, simply include it after the exporting module. The exporting module is a required dependency even if fallback is disabled.


    <script src=""></script>
    <script src=""></script>
    <script src=""></script>

### Browser support table

|                                         | Chrome (latest) | Firefox (latest) | Edge (latest) | Safari (latest) | Safari 5.1                | IE 10-11                  | Android (latest) | Android (4.0)             | Chrome for Android | Safari for iOS     | Chrome for iOS            |
|-----------------------------------------|-----------------|------------------|---------------|-----------------|---------------------------|---------------------------|------------------|---------------------------|--------------------|--------------------|---------------------------|
| SVG                                     | OK              | OK               | OK            | OK              | Opens data URI            | OK                        | OK               | Opens data URI            | OK                 | OK                 | OK                        |
| PNG/JPEG                                | OK              | OK               | OK            | OK              | Opens data URI            | OK                        | OK               | Opens data URI            | OK                 | OK                 | OK                        |
| PDF                                     | OK              | OK               | OK            | OK              | Fallback to export server | Fallback to export server | OK               | Fallback to export server | OK                 | OK                 | OK                        |
| SVG w/images (same server)              | OK              | OK               | OK            | OK              | Opens data URI            | OK                        | OK               | Opens data URI            | OK                 | OK                 | OK                        |
| PNG/JPEG w/images (same server)         | OK              | OK               | OK            | OK              | Suboptimal image          | Fallback to export server | OK               | Opens data URI            | OK                 | OK                 | OK                        |
| SVG w/images (CORS enabled server)      | OK              | OK               | OK            | OK              | Fallback to export server | Fallback to export server | OK               | Fallback to export server | OK                 | OK                 | OK                        |
| PNG/JPEG w/images (CORS enabled server) | OK              | OK               | OK            | OK              | Fallback to export server | Fallback to export server | OK               | Fallback to export server | OK                 | OK                 | OK                        |

Internet Explorer 9 and older will attempt to fall back to export server in all cases.

Decision flowchart of the module (click for large version):

![Offline export decision flowchart]()


### Export local PDF in a language containing non-Latin characters or Unicode Characters/UTF-8

As described in the jsPDF docs, the 14 standard fonts in PDF are limited to the ASCII-codepage. Therefore, in order to support for example Chinese text in the exported PDF, one or more TTF font files have to be passed on to the exporting module.

TTF font files are available from several resources online. A good resource is Google Fonts, and the Noto set of fonts that support a variety of different languages. Given the volume of languages and glyphs, there is no single font files that covers all languages.

For the sake of our feature demo, we are loading font files from our own website:

```
exporting: {
    pdfFont: {
        normal: '',
        bold: '',
        bolditalic: '',
        italic: ''
    }
}
```
View it live on jsFiddle
