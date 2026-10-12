import os
import glob

components_dir = 'frontend/src/components/generated'
files = glob.glob(os.path.join(components_dir, '*.tsx'))

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace literal \n that was accidentally added to tags and blocks
    content = content.replace("\\n", "\n")
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

pages_dir = 'frontend/src/pages/generated'
files = glob.glob(os.path.join(pages_dir, '*.tsx'))

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace literal \n that was accidentally added
    content = content.replace("\\n", "\n")
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed literal newlines in components and pages.")
