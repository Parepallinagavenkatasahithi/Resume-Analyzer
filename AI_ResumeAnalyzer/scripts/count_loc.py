import os
import sys

def count_loc(directory, extensions):
    total_loc = 0
    excluded_dirs = {'.git', 'node_modules', 'build', 'dist', 'cache', '__pycache__', 'venv', 'env', 'tests'}
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in excluded_dirs and not d.endswith('_tests')]
        
        for file in files:
            if file.endswith(extensions):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        # Count non-empty, non-comment lines loosely
                        valid_lines = [l for l in lines if l.strip() and not l.strip().startswith(('#', '//', '/*'))]
                        total_loc += len(valid_lines)
                except Exception:
                    pass
    return total_loc

if __name__ == '__main__':
    backend_loc = count_loc('backend', ('.py',))
    frontend_loc = count_loc('frontend', ('.ts', '.tsx', '.js', '.jsx', '.css'))
    print(f"Backend LOC: {backend_loc}")
    print(f"Frontend LOC: {frontend_loc}")
    print(f"Total Meaningful Production LOC: {backend_loc + frontend_loc}")
