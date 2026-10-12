import os
import zipfile

def create_zip(zip_filename, source_dir):
    exclusions = {'node_modules', '__pycache__', '.git', 'venv', 'env', '.env'}
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Modify dirs in-place to skip exclusions
            dirs[:] = [d for d in dirs if d not in exclusions]
            
            for file in files:
                # Exclude specific files if needed
                if file.endswith('.zip') or file in exclusions:
                    continue
                    
                file_path = os.path.join(root, file)
                # Ensure the path inside the zip starts from the root of the project
                arcname = os.path.relpath(file_path, start=source_dir)
                zipf.write(file_path, arcname)

if __name__ == '__main__':
    create_zip('AI_ResumeAnalyzer.zip', '.')
    print(f"Project successfully zipped to AI_ResumeAnalyzer.zip")
