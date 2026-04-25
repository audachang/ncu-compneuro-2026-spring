"""Compile homeworks/week06/吳心圓.md -> 吳心圓.pdf using the verified CJK pipeline."""
import subprocess
from pathlib import Path

FONT_MAIN = "Times New Roman"
FONT_CJK  = "Microsoft JhengHei"
FONT_SIZE = "14pt"
GEOMETRY  = "margin=1in"
DOC_CLASS = "extarticle"

base = Path(r"c:\Users\audachang\Dropbox\02_Academic_Work\courses\ComputerCogneuro\2026_Spring_CompBigData\homeworks\week06")
src  = base / "吳心圓.md"
tex  = base / "吳心圓.tex"
pdf  = base / "吳心圓.pdf"

print(f"Source: {src}")

# 1. md -> tex
subprocess.run([
    "pandoc", str(src), "-o", str(tex), "--standalone",
    "-V", f"documentclass={DOC_CLASS}",
    "-V", f"fontsize={FONT_SIZE}",
    "-V", f"mainfont={FONT_MAIN}",
    "-V", f"CJKmainfont={FONT_CJK}",
    "-V", f"geometry={GEOMETRY}",
], check=True)
print("pandoc done")

# 2. Patch linethickness bug
t = tex.read_text(encoding="utf-8")
tex.write_text(
    t.replace(r"\rule{0.5\linewidth}{\linethickness}",
              r"\rule{0.5\linewidth}{0.4pt}"),
    encoding="utf-8",
)
print("patch done")

# 3. tex -> pdf
subprocess.run(
    ["xelatex.exe", "-interaction=nonstopmode", str(tex)],
    cwd=str(base),
    check=True,
)
print(f"Done -> {pdf}")
