# Understanding Highcharts Grid

Highcharts Grid displays structured data in columns and rows, using a standard
HTML table as its foundation. Most Grid setups start with a data source, then
define how columns and cells should look and behave, and finally add features
such as pagination, editing, accessibility, and exporting.

![table](ill_table.png)

## Overall structure

Most Grid setups combine a few core options:

```js
Grid.grid('container', {
    data: {
        columns: {
            product: ['Apple', 'Pear', 'Orange'],
            price: [3.5, 2.5, 3]
        }
    }
}
```

The `data` object defines how Grid receives, prepares, and updates data. For column data, use `data.columns` (an object where each key is a column ID and each value is an array of cell values). Alternatively, pass an existing `DataTable` instance via `data.dataTable`. The DataTable class stores key-value pairs: each key becomes a header label, and each value is an array with the corresponding column values. When users edit cells (for example via edit mode), Grid writes changes back through the configured data provider.
Read more about [data handling and the DataTable class](./dashboards/data-table).

Use `data.autogenerateColumns` to control how provider columns are rendered:
- `true` (default): provider columns are rendered automatically, and custom
  columns from `columns[]` that are missing in provider data are appended.
- `false`: Grid renders only columns explicitly configured in `columns[]` (or
  referenced in `header[]`).

For detailed behavior and examples, see the
[Columns article](./grid/columns/index).

Instead of `data.columns` or `data.dataTable`, you can also use data connectors for loading data.

```js
{
    data: {
        connector: {
            type: JSON,
            data: [
                ['colA', 'colB'],
                [1, 2],
                [3, 4]
            ]
        }
    }
}
```

### Data providers
Grid reads and writes data through a data provider. The default `LocalDataProvider` works with an in-memory `DataTable`, but you can register a custom provider for other data sources. In Grid Pro, the `RemoteDataProvider` is available for server-backed data and on-demand paging. For details and configuration examples, see the [Data handling article](./grid/data-handling/overview).

### Data modifiers

When you have an existing [DataTable](./dashboards/data-table) instance (for example, one created with a [Math Modifier](./dashboards/mathmodifier-module) from Highcharts Dashboards library to add computed columns), pass it via `data.dataTable`.

You can read more about Data Modifiers [here](./dashboards/data-modifiers).

## columnDefaults and columns[]
```js
{
    columnDefaults: {
        cells: {
            editMode: {
                enabled: true
            }
        }
    },
    columns: [{
        id: 'price',
        cells: {
            format: '${value}'
        }
    }],
    pagination: {
        enabled: true
    }
});
```

In practice, you will usually work with a few main topics: how data is loaded,
how columns are defined, how rows are rendered, and how cell content is
formatted or edited.

## Start here

If you are new to Grid, begin with:

- [General](./grid/general)
- [Installation](./grid/installation)

Then continue with the topic area that matches the part of Grid you are working
on.

## Core topics

### Data handling

Data handling covers how Grid receives data, how it stores it internally, and
whether sorting, filtering, and pagination happen in the browser or on the
server.

Start with:

- [Data handling / Overview](./grid/data-handling/overview)
- [Data handling / Client-side](./grid/data-handling/clientside)
- [Data handling / Server-side](./grid/data-handling/serverside)
- [Data handling / Connectors](./grid/data-handling/connectors)

### Columns

Columns define the structure of the Grid. This includes header labels, grouped
headers, column sizing, sorting, filtering, and column-level styling.

Start with:

- [Columns](./grid/columns/index)
- [Header](./grid/columns/header)
- [Grouping](./grid/columns/grouping)
- [Resizing and width](./grid/columns/resizing-and-width)
- [Sorting](./grid/columns/sorting)
- [Filtering](./grid/columns/filtering)
- [Styling and theming](./grid/columns/styling-and-theming)

### Rows

Rows focus on the rendered dataset: row access, pagination, virtualization, and
performance when displaying large amounts of data.

Start with:

- [Rows](./grid/rows/index)
- [Row data](./grid/rows/data)
- [Pagination](./grid/rows/pagination)
- [Pinning](./grid/rows/pinning)
- [Tree view](./grid/rows/tree-view)
- [Virtualization](./grid/rows/virtualization)
- [Performance and rendering](./grid/rows/performance)

### Cells

Cells control how individual values are presented, styled, and formatted inside
the Grid.

Start with:

- [Cells](./grid/cells/index)
- [Styling and theming](./grid/cells/styling-and-theming)
- [Formatting](./grid/cells/formatting)

### Editing __grid_pro__

Editing covers end-user value editing, built-in renderers, validation rules,
and custom editing behavior.

Start with:

- [Editing](./grid/editing/index)
- [Renderers](./grid/editing/renderers)
- [Validation](./grid/editing/validation)
- [Custom renderers](./grid/editing/custom-renderers)

### Theming

Theming covers CSS variables, theme customization, conditional styling, and
custom icons.

Start with:

- [Theming](./grid/theming/index)
- [Grid variables](./grid/theming/grid-variables)
- [Element variables](./grid/theming/element-variables)
- [Conditional theming](./grid/theming/conditional)
- [Custom icons](./grid/theming/custom-icons)

### Frameworks

Framework articles show how to use Grid with supported frameworks.

Start with:

- [Frameworks](./grid/frameworks/index)
- [Angular](./grid/frameworks/angular)
- [Next.js](./grid/frameworks/nextjs)
- [React](./grid/frameworks/react)
- [Vue](./grid/frameworks/vue)

## Additional topics

- [Responsive grid](./grid/responsive-grid) for container-based layout changes
- [Events](./grid/events) for lifecycle and interaction events
- [Accessibility](./grid/accessibility) for screen reader support and accessibility features
- [Internationalization](./grid/internationalization) for translated UI text and locale-aware formatting
- [Exporting data](./grid/exporting) for CSV and JSON export
- [Sparklines](./grid/sparklines)  for inline charts inside cells

Use this page as an overview of the main Grid concepts. Once you know which
part of the Grid you are working on, the linked topic article should be the
next step.
