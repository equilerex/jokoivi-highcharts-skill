---
sidebar_label: "Overview"
---

# Rows overview

Rows are driven by the configured data provider. These articles cover
how row data is accessed, how large result sets are presented, and how row
rendering is optimized.

## Data

Rows are formed from the configured column data and accessed through the
active `dataProvider`. See
[Row data](./grid/rows/data).

## Pagination

Use pagination when rows should be split into pages with configurable page
size and navigation controls. See
[Row pagination](./grid/rows/pagination).

## Pinning

Use row pinning to keep selected rows visible at the top or bottom while the
main row set scrolls normally. See
[Row pinning](./grid/rows/pinning).

## Tree view

Use TreeView to present flat source rows as an expandable hierarchy with
parent-child context, sticky ancestors, and runtime expand/collapse control.
See [Tree view](./grid/rows/tree-view).

## Virtualization

Use row virtualization to render only the visible window of rows when working
with large datasets. See
[Row virtualization](./grid/rows/virtualization).

## Performance and rendering

Tune row rendering with options such as buffer size, strict heights, and
minimum visible rows. See
[Performance and rendering](./grid/rows/performance).
