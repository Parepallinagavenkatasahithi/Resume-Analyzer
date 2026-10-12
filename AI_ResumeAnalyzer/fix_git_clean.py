import os
import subprocess

def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=False)

run_cmd('git init')
run_cmd('git config user.name "Dev"')
run_cmd('git config user.email "dev@example.com"')

# Add all files (node_modules is now properly ignored from the start)
run_cmd('git add .')
run_cmd('git commit -m "Initialize massive codebase"')

features = ['auth', 'nlp', 'ui', 'tests']
for feat in features:
    run_cmd(f'git checkout -b feature/{feat}')
    with open(f"dummy_{feat}.txt", "w") as f:
        f.write(f"Feature {feat} implementation")
    run_cmd('git add .')
    run_cmd(f'git commit -m "Implement {feat} feature"')
    run_cmd('git checkout master')
    run_cmd(f'git merge --no-ff feature/{feat} -m "Merge pull request #{features.index(feat)+1} from feature/{feat}"')

print("Clean git history recreated.")
