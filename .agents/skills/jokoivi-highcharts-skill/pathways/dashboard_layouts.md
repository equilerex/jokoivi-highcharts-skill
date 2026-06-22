# Dashboard Layouts (@highcharts/dashboards)

## Objective
Provide consistent, reliable layout structures when using the `@highcharts/dashboards` package.

## Core Rules
1. Dashboards use a grid layout system (rows and cells).
2. Ensure components reference `renderTo` elements that match the cell IDs.
3. Keep layout structure separated from component specific options when assembling complex views.

## Component Definition Standard
- Always specify `type: 'Highcharts'` for standard chart components.
- Data connectors should be abstracted outside the view layer when possible.
- Avoid mixing HTML components heavily unless explicitly requested.
