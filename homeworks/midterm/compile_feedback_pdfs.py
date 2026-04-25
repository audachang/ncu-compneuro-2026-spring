"""Compile midterm individual feedback MD files to PDFs named by Chinese student name.

Two compilation paths:
  1. Windows (MiKTeX + Microsoft JhengHei): pandoc -> xelatex.exe via xeCJK.
  2. Linux (pandoc + weasyprint): pandoc -> HTML -> weasyprint PDF (fallback).
"""
import os
import shutil
import subprocess
from pathlib import Path

FONT_MAIN = "Times New Roman"
FONT_CJK  = "Microsoft JhengHei"
FONT_SIZE = "14pt"
GEOMETRY  = "margin=1in"
DOC_CLASS = "extarticle"

STUDENTS = [
    ("feedback_113825002.md", "呂杰驛"),
    ("feedback_114825002.md", "何官臻"),
    # Wu (113892001) did not submit the midterm
]

CSS_LINUX = """
@page { size: A4; margin: 2cm; }
body {
  font-family: "Droid Sans Fallback", "Noto Sans CJK TC", "Microsoft JhengHei", sans-serif;
  font-size: 12pt; line-height: 1.5; color: #111;
}
h1 { font-size: 20pt; border-bottom: 2px solid #444; padding-bottom: 4pt; margin-top: 0; }
h2 { font-size: 16pt; margin-top: 18pt; color: #222; }
h3 { font-size: 13pt; margin-top: 14pt; color: #333; }
blockquote { border-left: 4px solid #888; background: #f5f5f5; padding: 6pt 10pt;
             margin: 10pt 0; color: #333; font-size: 10.5pt; }
table { border-collapse: collapse; width: 100%; margin: 10pt 0; font-size: 10pt; }
th, td { border: 1px solid #888; padding: 4pt 8pt; vertical-align: top; text-align: left; }
th { background: #e8eef8; font-weight: bold; }
code { background: #f0f0f0; padding: 1pt 3pt; border-radius: 2pt; font-size: 10pt; }
hr { border: none; border-top: 1px solid #888; margin: 12pt 0; }
strong { color: #000; }
"""


def compile_windows(src_md: Path, out_name: str):
    base = src_md.parent
    tex = base / f"{out_name}.tex"
    pdf = base / f"{out_name}.pdf"

    subprocess.run([
        "pandoc", str(src_md), "-o", str(tex), "--standalone",
        "-V", f"documentclass={DOC_CLASS}",
        "-V", f"fontsize={FONT_SIZE}",
        "-V", f"mainfont={FONT_MAIN}",
        "-V", f"CJKmainfont={FONT_CJK}",
        "-V", f"geometry={GEOMETRY}",
    ], check=True)

    t = tex.read_text(encoding="utf-8")
    tex.write_text(
        t.replace(r"\rule{0.5\linewidth}{\linethickness}",
                  r"\rule{0.5\linewidth}{0.4pt}"),
        encoding="utf-8",
    )

    subprocess.run(
        ["xelatex.exe", "-interaction=nonstopmode", str(tex)],
        cwd=str(base),
        check=True,
    )
    print(f"  -> {pdf.name} generated (xelatex).")


def compile_linux(src_md: Path, out_name: str):
    from weasyprint import HTML, CSS
    base = src_md.parent
    html = base / f"{out_name}.html"
    pdf  = base / f"{out_name}.pdf"
    css  = base / "_feedback.css"
    css.write_text(CSS_LINUX, encoding="utf-8")

    subprocess.run(
        ["pandoc", str(src_md), "-o", str(html), "--standalone",
         "--css", str(css), "--metadata", f"title={out_name}"],
        check=True,
    )
    HTML(filename=str(html)).write_pdf(str(pdf), stylesheets=[CSS(filename=str(css))])
    print(f"  -> {pdf.name} generated (weasyprint).")


if __name__ == "__main__":
    base = Path(__file__).parent
    use_windows = shutil.which("xelatex.exe") is not None
    compile_fn = compile_windows if use_windows else compile_linux
    print(f"Using compile path: {'xelatex (Windows)' if use_windows else 'weasyprint (Linux)'}")

    for src_file, chinese_name in STUDENTS:
        src = base / src_file
        print(f"\n{'='*60}\nCompiling {src_file} -> {chinese_name}.pdf ...\n{'='*60}")
        compile_fn(src, chinese_name)
    print("\nDone — all PDFs generated.")
