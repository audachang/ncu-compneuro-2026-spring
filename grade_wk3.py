import os
import json

base_dir = r"c:\Users\audachang\Dropbox\02_Academic_Work\courses\ComputerCogneuro\2026_Spring_CompBigData\homeworks\week03"
students = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

for student in sorted(students):
    student_dir = os.path.join(base_dir, student)
    files = [f for f in os.listdir(student_dir) if f.endswith('.ipynb')]
    if files:
        file_path = os.path.join(student_dir, files[0])
        print(f"\n{'='*60}\nStudent: {student}\nFile: {files[0]}\n{'='*60}")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            q_num = 1
            for cell in data.get('cells', []):
                if cell['cell_type'] == 'code':
                    source = "".join(cell.get('source', []))
                    if source.strip() and "===" in source:
                        print(f"\n--- Q{q_num} CODE CELL ---")
                        print(source)
                        q_num += 1
    else:
        print(f"\nNo .ipynb found for {student}")
