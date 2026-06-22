import os
import sys
import re

def extract_sample(chart_path):
    skill_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    samples_dir = os.path.join(skill_dir, 'references', 'repo-copy', 'types-schemas', 'samples')
    
    if not os.path.exists(samples_dir):
        print(f"Error: Samples directory not found at {samples_dir}")
        sys.exit(1)

    # Attempt to find the specific demo folder. Path might look like "highcharts/demo/line-basic"
    demo_js_path = os.path.join(samples_dir, chart_path, 'demo.js')
    
    if not os.path.exists(demo_js_path):
        # Fallback: try searching across directories if path isn't exact
        found = False
        for root, dirs, files in os.walk(samples_dir):
            if chart_path in root and 'demo.js' in files:
                demo_js_path = os.path.join(root, 'demo.js')
                found = True
                break
        
        if not found:
            print(f"Error: Could not find demo.js for {chart_path}")
            sys.exit(1)

    print(f"Extracting from: {demo_js_path}")
    with open(demo_js_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Attempt to extract Highcharts.chart(..., {...}) payload
    match = re.search(r"Highcharts\.chart\(\s*['\"].*?['\"]\s*,\s*(\{.*?\})\s*\);?", content, re.DOTALL)
    if match:
        print("--- EXTRACTED CONFIG ---")
        print(match.group(1))
    else:
        print("Could not parse Highcharts.chart call. Dumping raw demo.js:")
        print(content[:2000])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_sample_config.py <demo-path>")
        sys.exit(1)
    
    extract_sample(sys.argv[1])
