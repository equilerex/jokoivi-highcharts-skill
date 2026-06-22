# Highcharts Skill: Test Commands

This document provides commands to manually test the autonomous skill helper tools locally.

### 1. Test AST Dictionary Extraction
Retrieves the pruned, valid JSON interface definition directly from the `highcharts_api_map.json` file.

```powershell
python .agents/skills/jokoivi-highcharts-skill/scripts/grep_ts_definitions.py ChartOptions
```
*If you misspell a name, it will suggest partial matches.*

### 2. Test Deprecation & Hallucination Checker
This tool validates whether the keys you are using exist *anywhere* in the Highcharts API map. If you use a deprecated key (which we pruned out) or completely hallucinate a key, it throws an error.

**Windows PowerShell Tip:**
Passing raw JSON strings via the command line in Windows can cause escaping errors (e.g., `Error: Input is not valid JSON`). To avoid this, write your test configuration to a file (like `test.json`) and pass the file path:

```powershell
# 1. Create a quick test file
echo '{"chart": {"type": "line"}, "title": {"text": "Valid Chart"}}' > test.json

# 2. Run the checker on the file
python .agents/skills/jokoivi-highcharts-skill/scripts/deprecation_checker.py test.json
```

### 3. Test Sample Extraction
Pulls verified Highcharts configurations directly from the official `samples` directory to provide a known-working baseline.

```powershell
python .agents/skills/jokoivi-highcharts-skill/scripts/extract_sample_config.py line-chart
python .agents/skills/jokoivi-highcharts-skill/scripts/extract_sample_config.py 3d-pie-donut
```

### 4. Search Local Official Docs
We have retained the official Highcharts markdown documentation in the skill for fast lookup.

```powershell
python .agents/skills/jokoivi-highcharts-skill/scripts/search_local_docs.py "accessibility"
python .agents/skills/jokoivi-highcharts-skill/scripts/search_local_docs.py "color axis"
```
