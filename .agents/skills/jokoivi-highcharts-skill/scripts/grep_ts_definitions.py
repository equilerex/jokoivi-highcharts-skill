import os
import sys
import json

def search_ts(query):
    skill_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    api_map_file = os.path.join(skill_dir, 'highcharts_api_map.json')
    
    if not os.path.exists(api_map_file):
        print(f"Error: API map not found at {api_map_file}")
        sys.exit(1)

    with open(api_map_file, 'r', encoding='utf-8') as f:
        api_map = json.load(f)

    if query in api_map:
        print(f"--- MATCH FOUND FOR '{query}' ---")
        print(json.dumps(api_map[query], indent=2))
    else:
        # Fallback partial match
        print(f"No strict interface match for '{query}'. Searching for partial matches...")
        matches = [k for k in api_map.keys() if query.lower() in k.lower()]
        if matches:
            print(f"Found {len(matches)} partial matches:")
            for m in matches[:10]:
                print(f" - {m}")
            if len(matches) > 10:
                print("... [TRUNCATED]")
        else:
            print("No matches found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python grep_ts_definitions.py <InterfaceOrType>")
        sys.exit(1)
    
    search_ts(sys.argv[1])
