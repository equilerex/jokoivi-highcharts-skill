# Generate Highcharts Config (Strict CoT)

You must follow this Strict Chain of Thought (CoT) when generating or patching an actual Highcharts configuration.
The goal is to physically prevent you from hallucinating deprecated or non-existent API keys.

## 1. Extract a Baseline (Optional but Recommended)
Do not try to build complex charts from memory.
Use `python .agents/skills/jokoivi-highcharts-skill/scripts/extract_sample_config.py <chart-type>` to pull a verified configuration straight from the official Highcharts samples repository.
*(Hint: You can use `list_dir` on `.agents/skills/jokoivi-highcharts-skill/references/repo-copy/types-schemas/samples` to find exact sample names if the tool fails).*

## 2. Query the AST Dictionary (Mandatory)
Before you add any new property to the configuration, you **must** verify its exact type and existence in our local AST map.
**Command:** `python .agents/skills/jokoivi-highcharts-skill/scripts/grep_ts_definitions.py <InterfaceName>`
*(Example: `python .agents/skills/jokoivi-highcharts-skill/scripts/grep_ts_definitions.py ChartOptions`)*

**Why?** This dictionary contains over 3,800 strictly typed Highcharts interfaces. All deprecated properties have been aggressively pruned out. If a property is not in this map, it does not exist.

## 3. Apply the A11y Baseline
Always ensure the generated configuration aligns with our corporate accessibility standard.
*(Load `pathways/a11y_baseline.md` if you haven't already).*

## 4. Draft and Validate (Mandatory)
Write out your configuration object as JSON and run it through our strict validation checker.
**Command:**
1. Save your draft to a temporary file: `test_draft.json`
2. Run `python .agents/skills/jokoivi-highcharts-skill/scripts/deprecation_checker.py test_draft.json`

**If the tool throws an error:** You have hallucinated a key or used a pruned/deprecated one. You MUST revise your draft and run the tool again until it passes cleanly.

## 5. Output
Only once validation passes, output the final typed `Highcharts.Options` object.
If the user asked for a patch, output a surgical diff block—never regenerate the full config.
