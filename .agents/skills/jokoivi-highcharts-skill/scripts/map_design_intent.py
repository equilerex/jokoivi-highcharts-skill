import sys

# Mapping design terminology to Highcharts API properties.
# This prevents an LLM or developer from hunting blindly for where an option lives.
INTENT_MAP = {
    # Spacing and layout
    "spacing": {
        "description": "Adjusting the breathing room of the chart or elements.",
        "api_paths": ["chart.spacing", "chart.margin", "plotOptions.series.pointPadding", "plotOptions.series.groupPadding", "legend.itemMarginTop", "legend.itemMarginBottom"],
        "advice": "Use chart.spacing for the outer container instead of CSS padding. For column bars, use pointPadding/groupPadding."
    },
    "overlap": {
        "description": "Fixing labels or elements that are colliding.",
        "api_paths": ["xAxis.labels.staggerLines", "dataLabels.crop", "dataLabels.overflow", "dataLabels.allowOverlap"],
        "advice": "Highcharts collision detection is robust. Do not manually measure and hide text. Tweak allowOverlap or use staggerLines."
    },
    "softer": {
        "description": "Making charts look 'cleaner' or less noisy (often a designer request).",
        "api_paths": ["yAxis.gridLineColor", "yAxis.gridLineDashStyle", "yAxis.gridLineWidth", "plotOptions.series.borderRadius", "xAxis.lineWidth", "xAxis.tickWidth"],
        "advice": "Reduce opacity of gridlines, use Dash style, or add a subtle borderRadius to columns/pies."
    },
    "tooltip": {
        "description": "Customizing the hover popup.",
        "api_paths": ["tooltip.formatter", "tooltip.pointFormatter", "tooltip.useHTML", "tooltip.split"],
        "advice": "Avoid building your own HTML tooltip overlays. Use useHTML: true and formatters, or tooltip.split for comparing multiple series gracefully."
    },
    "chip": {
        "description": "A 'chip' or 'tag' usually implies an interactive legend item, or an annotation.",
        "api_paths": ["legend", "annotations", "plotOptions.series.dataLabels"],
        "advice": "Think laterally: if a designer wants a 'clickable chip', they probably want a legend item (styled heavily) or an Annotation. Avoid adding raw DOM elements."
    },
    "donut text": {
        "description": "Putting a number or label in the center of a donut chart.",
        "api_paths": ["title", "subtitle", "plotOptions.pie.innerSize"],
        "advice": "Instead of renderer hacks, vertically align the title/subtitle to the middle, or use a dataLabel on a dummy center point."
    },
    "animation": {
        "description": "Customizing how charts draw.",
        "api_paths": ["chart.animation", "plotOptions.series.animation", "tooltip.animation"],
        "advice": "Highcharts handles enter and update animations natively. Do not use CSS transitions on generated SVG paths."
    },
    "colors": {
        "description": "Applying brand palettes.",
        "api_paths": ["colors", "chart.backgroundColor", "plotOptions.series.colorByPoint"],
        "advice": "Set the root `colors` array. Don't style SVG fills via CSS unless using styledMode."
    }
}

def map_intent(query):
    query_lower = query.lower()
    matches = []
    
    # We do a loose substring match to be forgiving
    for key, data in INTENT_MAP.items():
        if key in query_lower or query_lower in key:
            matches.append((key, data))
            
    # Also check descriptions
    if not matches:
        for key, data in INTENT_MAP.items():
            if query_lower in data["description"].lower():
                matches.append((key, data))

    if matches:
        print(f"--- Highcharts Design Intent Map ---")
        for key, data in matches:
            print(f"\nKeyword Match: '{key}'")
            print(f"Intent: {data['description']}")
            print(f"Relevant API Paths: {', '.join(data['api_paths'])}")
            print(f"💡 Advice: {data['advice']}")
        print("\nNote: Always verify the exact types for these paths using `grep_ts_definitions.py`!")
    else:
        print(f"No direct mapping found for '{query}'.")
        print(f"Try broader keywords like: {', '.join(INTENT_MAP.keys())}.")
        print("Remember to think laterally: a designer's term might map to an unexpected Highcharts feature.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python map_design_intent.py '<designer_keyword>'")
        sys.exit(1)
        
    map_intent(sys.argv[1])
