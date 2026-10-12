import os
import glob

pages_dir = 'frontend/src/pages/generated'
files = glob.glob(os.path.join(pages_dir, '*.tsx'))

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the incorrect import path
    content = content.replace("import { Component", "import { Component").replace("'../components/generated/", "'../../components/generated/")
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed imports in pages.")
