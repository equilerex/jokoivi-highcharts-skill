Setting up your own export server
=================================

There may be cases where you don't want to use Highcharts' export server running at export.highcharts.com, for instance if you are running a secure website or if you don't want your data to be passed to the Highcharts CDN. 

Before setting up your own server, consider using the client side export module.
In short, a dedicated server is only needed if you are having problems with the features listed in the client side export browser support table.

Node export server
------------------

Install with `npm install highcharts-export-server -g` or clone from 

Documentation on GitHub

The export server running at export.highcharts.com is a Node.js\-based service, which is easy to install and integrate on any system.
It accepts either chart configurations or SVGs, together with additional resources, and uses Puppeteer to render charts to images (PNG, JPG, PDF and SVG) to be sent back to the user.
