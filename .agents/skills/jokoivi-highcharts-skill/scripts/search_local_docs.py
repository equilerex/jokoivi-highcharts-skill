import os
import sys
import re

def search_docs(query):
    skill_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    docs_dir = os.path.join(skill_dir, 'references', 'repo-copy', 'types-schemas', 'docs')
    
    if not os.path.exists(docs_dir):
        print(f"Error: Docs directory not found at {docs_dir}")
        sys.exit(1)

    print(f"Searching Highcharts local docs for: '{query}'\n")
    
    match_count = 0
    query_lower = query.lower()
    
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md') or file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            if query_lower in line.lower():
                                # Get a small snippet around the match
                                start = max(0, i - 1)
                                end = min(len(lines), i + 2)
                                snippet = "".join(lines[start:end]).strip()
                                
                                rel_path = os.path.relpath(file_path, docs_dir)
                                print(f"--- MATCH in {rel_path} (Line {i+1}) ---")
                                print(snippet)
                                print("-" * 40)
                                match_count += 1
                                
                                if match_count >= 15:
                                    print("... [TOO MANY MATCHES. TRUNCATING OUTPUT]")
                                    sys.exit(0)
                except Exception as e:
                    pass

    if match_count == 0:
        print("No matches found in the local docs.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search_local_docs.py '<query>'")
        sys.exit(1)
    
    search_docs(sys.argv[1])
