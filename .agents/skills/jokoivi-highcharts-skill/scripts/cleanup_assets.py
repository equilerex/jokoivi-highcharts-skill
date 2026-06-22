import os
import shutil

def cleanup():
    skill_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    samples_dir = os.path.join(skill_dir, 'references', 'repo-copy', 'types-schemas', 'samples')
    
    if not os.path.exists(samples_dir):
        print(f"Error: Samples directory not found at {samples_dir}")
        return

    print(f"Starting cleanup in {samples_dir}...")
    
    # 1. Clear samples/data directory entirely except for readme
    data_dir = os.path.join(samples_dir, 'data')
    if os.path.exists(data_dir):
        for item in os.listdir(data_dir):
            item_path = os.path.join(data_dir, item)
            if item == 'readme.md':
                continue
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Deleted directory: {item_path}")
            else:
                os.remove(item_path)
                print(f"Deleted file: {item_path}")

    # 2. Walk samples and remove .html, .details, gitignore, and image/graphic assets
    # We keep .js, .scss, .css as requested.
    extensions_to_delete = {
        '.html', '.details', '.png', '.jpg', '.jpeg', '.gif', '.svg', 
        '.woff', '.woff2', '.ttf', '.otf', '.gitignore', '.cur', '.htm',
        '.details~head', '.details~origin_master'
    }
    
    deleted_count = 0
    for root, dirs, files in os.walk(samples_dir):
        for file in files:
            _, ext = os.path.splitext(file.lower())
            if ext in extensions_to_delete or file.lower() in extensions_to_delete:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

    print(f"Cleanup complete. Deleted {deleted_count} files.")

if __name__ == '__main__':
    cleanup()
