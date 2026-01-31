import os
import glob

root_dir = os.getcwd()
week_folders = sorted([d for d in os.listdir(root_dir) if os.path.isdir(d) and d.startswith("week-")])

print("## Course Materials by Week")
print("")

for folder in week_folders:
    # Get week number and description from folder name
    # Format: week-XX-description_text
    parts = folder.split("-")
    if len(parts) >= 3:
        week_num = parts[1]
        # Replace underscores with spaces and title case
        topic = " ".join(parts[2:]).replace("_", " ").title()
        
        print(f"### Week {week_num}: {topic}")
        print(f"**Folder:** `/{folder}`")
        print("")
        
        files = sorted(os.listdir(os.path.join(root_dir, folder)))
        files = [f for f in files if not f.startswith(".") and f != "__pycache__"]
        
        if files:
            print("| File | Description |")
            print("|------|-------------|")
            for f in files:
                # Basic description based on extension
                ext = os.path.splitext(f)[1]
                desc = "File"
                if ext == ".ipynb":
                    desc = "Jupyter Notebook"
                elif ext == ".pdf":
                    desc = "PDF Document"
                elif ext == ".py":
                    desc = "Python Script"
                elif ext == ".md":
                    desc = "Markdown Documentation"
                elif ext == ".csv":
                    desc = "Data File"
                
                print(f"| `{f}` | {desc} |")
        else:
            print("*No files currently uploaded.*")
        
        print("")
