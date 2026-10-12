import os
import zipfile

def create_zip(zip_filename, source_dir):
    exclusions = {'node_modules', '__pycache__', 'venv', 'env'} # Keep .git
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            dirs[:] = [d for d in dirs if d not in exclusions]
            
            for file in files:
                if file.endswith('.zip') or file in exclusions:
                    continue
                    
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=source_dir)
                zipf.write(file_path, arcname)

if __name__ == '__main__':
    create_zip('AI_ResumeAnalyzer.zip', '.')
    print(f"Project successfully zipped to AI_ResumeAnalyzer.zip")
