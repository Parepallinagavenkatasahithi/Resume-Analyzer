import os
import glob

components_dir = 'frontend/src/components/generated'
files = glob.glob(os.path.join(components_dir, '*.tsx'))

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the inflexible flex container with a wrapping one
    content = content.replace('className="mt-4 flex space-x-2"', 'className="mt-4 flex flex-wrap gap-2"')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed flex layout in components.")
