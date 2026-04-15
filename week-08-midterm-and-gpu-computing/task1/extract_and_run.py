import os
import json
import subprocess
import glob
import sys

def extract_code_from_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    script_content = []
    
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            if isinstance(source, str):
                source = source.splitlines(keepends=True)
            
            clean_source = []
            for line in source:
                # Comment out magics
                if line.strip().startswith('!') or line.strip().startswith('%'):
                    clean_source.append(f"# {line}")
                else:
                    clean_source.append(line)
            
            script_content.append("".join(clean_source))
            script_content.append("\n# " + "-"*20 + " Cell End " + "-"*20 + "\n\n")
            
    return "".join(script_content)

def main():
    notebooks = sorted(glob.glob("*.ipynb"))
    results = {}
    
    print(f"Found {len(notebooks)} notebooks in {os.getcwd()}")
    
    for nb_file in notebooks:
        # if nb_file != "1-03_memory_management.ipynb": continue # Debugging focus if needed
        
        script_name = nb_file.replace('.ipynb', '.py')
        print(f"Extracting {nb_file} -> {script_name}")
        
        try:
            code = extract_code_from_notebook(nb_file)
            with open(script_name, 'w', encoding='utf-8') as f:
                f.write(code)
                
            print(f"Running {script_name}...")
            # Run the script with the CURRENT environment (assuming this script is run within the target env)
            # or use sys.executable
            proc = subprocess.run(
                [sys.executable, script_name],
                capture_output=True,
                text=True
            )
            
            if proc.returncode == 0:
                print(f"PASS: {nb_file}")
                results[nb_file] = "PASS"
            else:
                print(f"FAIL: {nb_file}")
                print("Error Output (Last 20 lines):")
                lines = proc.stderr.splitlines()
                for line in lines[-20:]:
                    print(line)
                results[nb_file] = f"FAIL: {lines[-1] if lines else 'Unknown Error'}"
                
        except Exception as e:
            print(f"ERROR processing {nb_file}: {e}")
            results[nb_file] = f"ERROR: {str(e)}"
        
        print("="*60)
        
    print("\nSummary:")
    for nb, res in results.items():
        print(f"{nb}: {res}")

if __name__ == "__main__":
    main()
