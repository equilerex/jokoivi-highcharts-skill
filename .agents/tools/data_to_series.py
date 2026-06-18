"""
data_to_series.py

Converts REST API JSON (array of objects) to Highcharts series[] format.

Usage:
    python data_to_series.py --input data.json --type column --x month --y revenue
    python data_to_series.py --input data.json --type line --x date --y value --datetime
    python data_to_series.py --input data.json --type pie --name segment --y revenue
    python data_to_series.py --input data.json --type grouped-column --x quarter --y revenue --group region

Output: JSON string — paste directly into Highcharts.Options.series[]

Supported chart types:
    column, bar         → [{ name, data: [y, ...] }] with xAxis.categories
    line, spline        → [{ name, data: [y, ...] }] or datetime [{ name, data: [[ms, y], ...] }]
    pie                 → [{ type: 'pie', data: [{ name, y }, ...] }]
    grouped-column      → multiple series split by --group column
    grouped-bar         → same
    stacked-column      → same structure as grouped; stacking set separately in plotOptions
    scatter             → [{ name, data: [[x, y], ...] }]
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ── ISO datetime → Highcharts ms timestamp ─────────────────────────────────

def to_ms(value: str) -> int:
    """Convert ISO 8601 string to milliseconds since epoch."""
    formats = [
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%d/%m/%Y',
        '%m/%d/%Y',
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(value.strip(), fmt)
            return int(dt.replace(tzinfo=timezone.utc).timestamp() * 1000)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse datetime: {value!r}. Supply --datetime-format if non-standard.")


# ── Builders ────────────────────────────────────────────────────────────────

def build_category_series(
    rows: list[dict],
    x_col: str,
    y_col: str,
    series_name: str,
) -> tuple[list[Any], list[str]]:
    """Single series + categories list."""
    categories = []
    data = []
    for row in rows:
        categories.append(str(row[x_col]))
        val = row[y_col]
        data.append(None if val is None else float(val))
    series = [{'name': series_name, 'data': data}]
    return series, categories


def build_datetime_series(
    rows: list[dict],
    x_col: str,
    y_col: str,
    series_name: str,
) -> list[Any]:
    """Single time-series — data as [[ms_timestamp, value], ...]."""
    data = []
    for row in rows:
        ms = to_ms(str(row[x_col]))
        val = row[y_col]
        data.append([ms, None if val is None else float(val)])
    return [{'name': series_name, 'data': data}]


def build_pie_series(
    rows: list[dict],
    name_col: str,
    y_col: str,
) -> list[Any]:
    """Pie / donut series."""
    data = [
        {'name': str(row[name_col]), 'y': float(row[y_col])}
        for row in rows
        if row[y_col] is not None
    ]
    return [{'type': 'pie', 'data': data}]


def build_grouped_series(
    rows: list[dict],
    x_col: str,
    y_col: str,
    group_col: str,
    datetime_mode: bool,
) -> tuple[list[Any], list[str] | None]:
    """Multiple series split by group column. Returns (series[], categories | None)."""
    groups: dict[str, dict[str, Any]] = {}
    x_order: list[str] = []
    seen_x: set[str] = set()

    for row in rows:
        grp = str(row[group_col])
        x_val = str(row[x_col])
        if grp not in groups:
            groups[grp] = {}
        groups[grp][x_val] = row[y_col]
        if x_val not in seen_x:
            x_order.append(x_val)
            seen_x.add(x_val)

    if datetime_mode:
        series = []
        for grp, mapping in groups.items():
            data = [[to_ms(x), float(v) if v is not None else None] for x, v in mapping.items()]
            series.append({'name': grp, 'data': data})
        return series, None
    else:
        series = []
        for grp, mapping in groups.items():
            data = [float(mapping.get(x, None)) if mapping.get(x) is not None else None for x in x_order]
            series.append({'name': grp, 'data': data})
        return series, x_order


def build_scatter_series(
    rows: list[dict],
    x_col: str,
    y_col: str,
    series_name: str,
) -> list[Any]:
    """Scatter — data as [[x, y], ...]."""
    data = [
        [float(row[x_col]), float(row[y_col])]
        for row in rows
        if row[x_col] is not None and row[y_col] is not None
    ]
    return [{'name': series_name, 'type': 'scatter', 'data': data}]


# ── Output formatter ────────────────────────────────────────────────────────

def emit(series: list[Any], categories: list[str] | None, chart_type: str) -> None:
    """Print result as Highcharts-ready JSON with xAxis hint if applicable."""
    output: dict[str, Any] = {'series': series}

    if categories:
        output['xAxis_hint'] = {
            '_comment': 'Add this to your xAxis config',
            'categories': categories,
        }

    if chart_type in ('line', 'spline') and series and series[0].get('data') and isinstance(series[0]['data'][0], list):
        output['xAxis_hint'] = {
            '_comment': 'Add this to your xAxis config',
            'type': 'datetime',
        }

    print(json.dumps(output, indent=2, ensure_ascii=False))


# ── CLI ─────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description='Convert REST API JSON to Highcharts series[]')
    p.add_argument('--input',   '-i', required=True,  help='Path to JSON file (array of objects)')
    p.add_argument('--type',    '-t', required=True,
                   choices=['column', 'bar', 'line', 'spline', 'pie',
                            'grouped-column', 'grouped-bar', 'stacked-column', 'scatter'],
                   help='Target chart type')
    p.add_argument('--x',       '-x', help='Column for x-axis / categories')
    p.add_argument('--y',       '-y', help='Column for y-axis values')
    p.add_argument('--name',    '-n', help='Column for point names (pie charts)')
    p.add_argument('--group',   '-g', help='Column to split into multiple series')
    p.add_argument('--series-name', default='Series 1', help='Series name (single-series charts)')
    p.add_argument('--datetime', action='store_true',
                   help='x column contains datetime strings → convert to ms timestamps')
    p.add_argument('--datetime-format', help='strptime format string for non-standard datetimes')
    return p.parse_args()


def load_data(path: str) -> list[dict]:
    text = Path(path).read_text(encoding='utf-8')
    data = json.loads(text)
    if isinstance(data, dict):
        # Common REST pattern: { data: [...] } or { results: [...] } or { items: [...] }
        for key in ('data', 'results', 'items', 'records'):
            if key in data and isinstance(data[key], list):
                return data[key]
        raise ValueError(f"JSON object has no recognized array key. Keys: {list(data.keys())}")
    if not isinstance(data, list):
        raise ValueError(f"Expected JSON array or object with array. Got: {type(data)}")
    return data


def main() -> None:
    args = parse_args()
    rows = load_data(args.input)

    if not rows:
        print('[]')
        return

    chart_type = args.type

    if chart_type == 'pie':
        if not args.name or not args.y:
            sys.exit('pie requires --name and --y')
        series = build_pie_series(rows, args.name, args.y)
        emit(series, None, chart_type)

    elif chart_type == 'scatter':
        if not args.x or not args.y:
            sys.exit('scatter requires --x and --y')
        series = build_scatter_series(rows, args.x, args.y, args.series_name)
        emit(series, None, chart_type)

    elif chart_type in ('grouped-column', 'grouped-bar', 'stacked-column'):
        if not args.x or not args.y or not args.group:
            sys.exit(f'{chart_type} requires --x, --y, and --group')
        series, categories = build_grouped_series(rows, args.x, args.y, args.group, args.datetime)
        emit(series, categories, chart_type)

    else:
        # column, bar, line, spline — single series
        if not args.x or not args.y:
            sys.exit(f'{chart_type} requires --x and --y')

        if args.datetime:
            series = build_datetime_series(rows, args.x, args.y, args.series_name)
            emit(series, None, chart_type)
        else:
            series, categories = build_category_series(rows, args.x, args.y, args.series_name)
            emit(series, categories, chart_type)


if __name__ == '__main__':
    main()
