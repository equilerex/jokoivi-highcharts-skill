Working with data
=================

In Highcharts core, you specify the data through the series.data option directly on the configuration object. However, this is not always the simplest way to add data, for example if you are loading data from a CSV file, a HTML table or a Google Spreadsheet.

## DataTables: A more structured approach

Highcharts since v13 offers the `dataTable` and `dataMapping` options as a structured way to work with tabular data. This approach is particularly useful when:

- Loading data from **structured sources** like databases, CSV files, or APIs
- Displaying **multiple series from the same source** with different column mappings
- **Sharing data between Grid and Chart components** for synchronized visualizations
- Implementing **reactive data updates** without manual point management
- Building **dashboards with multiple synchronized components**

For a comprehensive guide, see Using DataTables with Series.

## Data module and custom preprocessing

In most of these cases you can use our built-in data parsing features from the _Data module_. Alternatively, if you don't have control over the data structure, you may need to preprocess the data by setting up your own _data parser_.

We will cover the following topics:

*   Using DataTables with Series
*   Data compression
*   Using the Data module
*   Custom preprocesssing
*   Live data
*   Data from a database
*   Getting data across domains (JSONP)
