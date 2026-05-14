"""Compile week05 individual feedback MD files to PDFs named by Chinese student name."""
import subprocess
from pathlib import Path

FONT_MAIN = "Times New Roman"
FONT_CJK  = "Microsoft JhengHei"
FONT_SIZE = "14pt"
GEOMETRY  = "margin=1in"
DOC_CLASS = "extarticle"

# Map: source MD (student ID) -> output PDF name (Chinese name)
STUDENTS = [
    ("feedback_113825002.md", "呂杰驛"),
    ("feedback_113892001.md", "吳心圓"),
    ("feedback_114825002.md", "何官臻"),
]


def compile_one(src_md: Path, out_name: str):
    base = src_md.parent
    tex = base / f"{out_name}.tex"
    pdf = base / f"{out_name}.pdf"

    # 1. md -> tex (output named by Chinese name)
    subprocess.run([
        "pandoc", str(src_md), "-o", str(tex), "--standalone",
        "-V", f"documentclass={DOC_CLASS}",
        "-V", f"fontsize={FONT_SIZE}",
        "-V", f"mainfont={FONT_MAIN}",
        "-V", f"CJKmainfont={FONT_CJK}",
        "-V", f"geometry={GEOMETRY}",
    ], check=True)

    # 2. Patch linethickness bug
    t = tex.read_text(encoding="utf-8")
    tex.write_text(
        t.replace(r"\rule{0.5\linewidth}{\linethickness}",
                  r"\rule{0.5\linewidth}{0.4pt}"),
        encoding="utf-8",
    )

    # 3. tex -> pdf
    subprocess.run(
        ["xelatex.exe", "-interaction=nonstopmode", str(tex)],
        cwd=str(base),
        check=True,
    )
    print(f"  -> {pdf.name} generated.")


if __name__ == "__main__":
    base = Path(__file__).parent
    for src_file, chinese_name in STUDENTS:
        src = base / src_file
        print(f"\n{'='*60}\nCompiling {src_file} -> {chinese_name}.pdf ...\n{'='*60}")
        compile_one(src, chinese_name)
    print("\nDone — all PDFs generated.")
