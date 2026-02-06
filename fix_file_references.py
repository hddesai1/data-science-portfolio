"""
Fix file references that were incorrectly changed
The refactoring changed CSV filenames but files weren't renamed
"""

import json
import re
from pathlib import Path

# File reference fixes
FILE_FIXES = {
    'training_data.csv': 'train.csv',
    'test_data.csv': 'test.csv',
}

# Code fixes - seaborn uses 'data=' not 'dataset='
CODE_FIXES = {
    'dataset=dataset': 'data=dataset',
    'dataset=': 'data=',
    'target=': 'y=',  # seaborn uses 'y=' not 'target='
}

def fix_notebook(notebook_path):
    """Fix file references in notebook"""
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
            
            # Fix file references
            for wrong_name, correct_name in FILE_FIXES.items():
                if wrong_name in new_source:
                    new_source = new_source.replace(wrong_name, correct_name)
                    modified = True
            
            # Fix code issues (seaborn parameters) - do this more carefully
            # Fix dataset=dataset -> data=dataset
            if 'dataset=dataset' in new_source:
                new_source = new_source.replace('dataset=dataset', 'data=dataset')
                modified = True
            # Fix dataset=variable -> data=variable (but be careful)
            new_source = re.sub(r'dataset=(\w+)', r'data=\1', new_source)
            if new_source != source:
                modified = True
            # Fix target= -> y= for seaborn
            new_source = re.sub(r'target=(\w+)', r'y=\1', new_source)
            if new_source != source:
                modified = True
            
            if source != new_source:
                cell['source'] = new_source.split('\n')
                if cell['source'] and cell['source'][-1] == '':
                    cell['source'] = cell['source'][:-1]
        
        if modified:
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=1, ensure_ascii=False)
            return True
        return False
    except Exception as e:
        print(f"  Error: {notebook_path}: {e}")
        return False

def fix_python_file(file_path):
    """Fix file references in Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        modified = False
        
        for wrong_name, correct_name in FILE_FIXES.items():
            if wrong_name in new_content:
                new_content = new_content.replace(wrong_name, correct_name)
                modified = True
        
        for wrong_code, correct_code in CODE_FIXES.items():
            if wrong_code in new_content:
                new_content = new_content.replace(wrong_code, correct_code)
                modified = True
        
        if modified:
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
                 if 'fix' not in str(f).lower()]
    python_files = [f for f in base_dir.rglob('*.py') 
                    if 'fix' not in str(f).lower()]
    
    print("Fixing file references...")
    print(f"Found {len(notebooks)} notebooks, {len(python_files)} Python files\n")
    
    nb_count = sum(1 for nb in notebooks if fix_notebook(nb))
    py_count = sum(1 for py_file in python_files if fix_python_file(py_file))
    
    print(f"Fixed {nb_count} notebooks, {py_count} Python files")
    print("[COMPLETE] File references fixed!")

if __name__ == '__main__':
    main()
