import os
import sys
import json

def check_deprecation(config_string):
    skill_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    api_map_file = os.path.join(skill_dir, 'highcharts_api_map.json')
    
    if not os.path.exists(api_map_file):
        print(f"Error: API map not found at {api_map_file}")
        sys.exit(1)
        
    try:
        # Check if the input is a file path to avoid Windows CLI escaping issues
        if os.path.exists(config_string) and os.path.isfile(config_string):
            with open(config_string, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = json.loads(config_string)
    except json.JSONDecodeError as e:
        print(f"Error: Input is not valid JSON. {e}")
        sys.exit(1)

    with open(api_map_file, 'r', encoding='utf-8') as f:
        api_map = json.load(f)

    # Flatten the user config to extract all property keys used
    keys_used = set()
    def extract_keys(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                keys_used.add(k)
                extract_keys(v)
        elif isinstance(obj, list):
            for item in obj:
                extract_keys(item)
                
    extract_keys(config)
    
    # Iterate through the API map and build a fast lookup of ALL VALID keys
    valid_registry = set()
    for interface_name, interface_data in api_map.items():
        if "properties" in interface_data:
            for prop_name in interface_data["properties"].keys():
                valid_registry.add(prop_name)
                    
    # Find any keys used in the config that DO NOT exist anywhere in the Highcharts API
    hallucinated_keys = keys_used - valid_registry
    
    if hallucinated_keys:
        print("ERROR: The following keys do not exist in the Highcharts API (Possible Hallucination/Deprecated):")
        for w in hallucinated_keys:
            print(f" - {w}")
        sys.exit(1)
    else:
        print(f"Success: Checked {len(keys_used)} keys. No deprecated properties detected.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deprecation_checker.py '<json_config_string>'")
        sys.exit(1)
    
    check_deprecation(sys.argv[1])
