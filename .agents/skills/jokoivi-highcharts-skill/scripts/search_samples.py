import os
import sys

def search_samples(keyword):
    skill_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    samples_dir = os.path.join(skill_dir, 'references', 'repo-copy', 'types-schemas', 'samples')
    
    if not os.path.exists(samples_dir):
        print(f"Error: Samples directory not found at {samples_dir}")
        sys.exit(1)
        
    matches = []
    keyword_lower = keyword.lower()
    
    for root, dirs, files in os.walk(samples_dir):
        if 'demo.js' in files:
            # Get relative path from samples_dir
            rel_path = os.path.relpath(root, samples_dir).replace('\\', '/')
            if keyword_lower in rel_path.lower():
                matches.append(rel_path)
                
    if matches:
        print(f"Found {len(matches)} matching sample paths:")
        for m in sorted(matches)[:15]:
            print(f"  - {m}")
        if len(matches) > 15:
            print(f"  ... and {len(matches) - 15} more matches.")
    else:
        print(f"No samples found matching keyword: {keyword}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python search_samples.py <keyword>")
        sys.exit(1)
    search_samples(sys.argv[1])
