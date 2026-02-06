"""
Fix issues introduced by refactoring:
1. Fix CSV file name references (training_data.csv -> train.csv)
2. Fix seaborn parameter names (dataset= -> data=)
3. Ensure variable consistency
"""

import re
import json
from pathlib import Path

def fix_notebook(notebook_path):
    """Fix issues in a notebook"""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        modified = False
        
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') != 'code':
                continue
            
            source_lines = cell.get('source', [])
            if not source_lines:
                continue
            
            source = ''.join(source_lines)
            new_source = source
            
            # Fix 1: CSV file names - revert incorrect changes
            # training_data.csv -> train.csv (if file exists)
            if 'training_data.csv' in new_source:
                # Check if train.csv exists in the same directory
                if (notebook_path.parent / 'train.csv').exists():
                    new_source = new_source.replace('"training_data.csv"', '"train.csv"')
                    new_source = new_source.replace("'training_data.csv'", "'train.csv'")
            
            # Fix 2: Seaborn parameter - dataset= should be data=
            # But be careful - only fix seaborn calls
            new_source = re.sub(r'sns\.\w+\(dataset=', r'sns.\1(data=', new_source)
            new_source = re.sub(r'sns\.\w+\(dataset=', r'sns.\1(data=', new_source)  # Second pass
            
            # Fix 3: Other common seaborn patterns
            new_source = re.sub(r'plt\.\w+\(dataset=', r'plt.\1(data=', new_source)
            
            if source != new_source:
                cell['source'] = new_source.split('\n')
                if cell['source'] and cell['source'][-1] == '':
                    cell['source'] = cell['source'][:-1]
                modified = True
        
        if modified:
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=1, ensure_ascii=False)
            return True
        return False
    except Exception as e:
        print(f"  Error: {notebook_path}: {e}")
        return False

def fix_python_file(file_path):
    """Fix issues in Python files"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        
        # Fix CSV file names
        if 'training_data.csv' in new_content:
            if (file_path.parent / 'train.csv').exists():
                new_content = new_content.replace('"training_data.csv"', '"train.csv"')
                new_content = new_content.replace("'training_data.csv'", "'train.csv'")
        
        # Fix seaborn parameters
        new_content = re.sub(r'sns\.\w+\(dataset=', r'sns.\1(data=', new_content)
        
        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    except Exception as e:
        print(f"  Error: {file_path}: {e}")
        return False

def main():
    base_dir = Path('.')
    
    notebooks = [f for f in base_dir.rglob('*.ipynb') 
                 if 'fix' not in str(f).lower() and 'refactor' not in str(f).lower()]
    python_files = [f for f in base_dir.rglob('*.py') 
                    if 'fix' not in str(f).lower() and 'refactor' not in str(f).lower()]
    
    print(f"Fixing {len(notebooks)} notebooks, {len(python_files)} Python files...\n")
    
    nb_count = 0
    py_count = 0
    
    for nb in notebooks:
        if fix_notebook(nb):
            nb_count += 1
            if nb_count <= 10:
                print(f"  [FIXED] {nb}")
    
    for py_file in python_files:
        if fix_python_file(py_file):
            py_count += 1
            if py_count <= 10:
                print(f"  [FIXED] {py_file}")
    
    print(f"\nFixed {nb_count} notebooks, {py_count} Python files")
    print("[COMPLETE] Fixes applied!")

if __name__ == '__main__':
    main()
