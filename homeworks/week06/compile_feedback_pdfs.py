"""
Split feedback.md into per-student Markdown files (named by Chinese name)
and compile each to PDF using the verified CJK pipeline:
  pandoc (md -> tex) + Python linethickness patch + xelatex
"""
import subprocess
from pathlib import Path

FONT_MAIN = "Times New Roman"
FONT_CJK  = "Microsoft JhengHei"
FONT_SIZE = "14pt"
GEOMETRY  = "margin=1in"
DOC_CLASS = "extarticle"

# Map: Chinese name -> content to write into individual MD file
# We read from feedback.md and split by student.

HEADER = "# Week 06 作業回饋（Posner Spatial Cueing Task — Builder + Pavlovia）\n\n"

# Student sections with their Chinese names and student IDs
STUDENTS = [
    ("呂杰驛", "113825002"),
    ("何官臻", "114825002"),
    ("吳心圓", "113892001"),
]


def split_feedback(feedback_path: Path) -> dict[str, str]:
    """Return {chinese_name: markdown_content} for each student."""
    text = feedback_path.read_text(encoding="utf-8")

    # Split on the horizontal rules (--- lines)
    # The file structure:
    #   HEADER
    #   --- (after header)
    #   ## 113825002 呂杰驛 section
    #   ---
    #   ## 114825002 何官臻 section
    #   ---
    #   ## 未繳交 section (includes 吳心圓 mention)
    #   ---
    #   ## 成績總覽 (summary table)

    # Find section boundaries by locating "## " headings
    lines = text.splitlines(keepends=True)

    # Collect section start line indices (0-indexed)
    section_indices = []
    for i, line in enumerate(lines):
        if line.startswith("## "):
            section_indices.append(i)

    sections = {}
    for idx, start in enumerate(section_indices):
        end = section_indices[idx + 1] if idx + 1 < len(section_indices) else len(lines)
        # Trim trailing --- separator lines
        chunk_lines = lines[start:end]
        # Remove trailing blank lines and --- separators
        while chunk_lines and chunk_lines[-1].strip() in ("", "---"):
            chunk_lines.pop()
        chunk = "".join(chunk_lines).strip()

        heading = lines[start].strip()  # e.g. "## 113825002 呂杰驛 — 94／100"

        # Match to a student
        for name, sid in STUDENTS:
            if name in heading or (sid in heading) or (name in chunk):
                if name not in sections:
                    sections[name] = chunk
                break
        else:
            # "未繳交" section — find 吳心圓 here
            if "吳心圓" in chunk and "吳心圓" not in sections:
                sections["吳心圓"] = chunk

    return sections


def compile_one(md_path: Path):
    tex = md_path.with_suffix(".tex")
    pdf = md_path.with_suffix(".pdf")

    # 1. md -> tex
    subprocess.run([
        "pandoc", str(md_path), "-o", str(tex), "--standalone",
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

    # 3. tex -> pdf (run in same dir so aux/log files stay there)
    subprocess.run(
        ["xelatex.exe", "-interaction=nonstopmode", str(tex)],
        cwd=str(md_path.parent),
        check=True,
    )
    print(f"  -> {pdf.name} generated.")


if __name__ == "__main__":
    base = Path(__file__).parent
    feedback_md = base / "feedback.md"

    print("Splitting feedback.md by student ...")
    sections = split_feedback(feedback_md)

    for name, sid in STUDENTS:
        content = sections.get(name)
        if content is None:
            print(f"  WARNING: no section found for {name}, skipping.")
            continue

        # Build a standalone MD with a top-level title
        md_content = f"{HEADER}{content}\n"
        out_md = base / f"{name}.md"
        out_md.write_text(md_content, encoding="utf-8")
        print(f"  Written: {out_md.name}")

    print("\nCompiling PDFs ...")
    for name, sid in STUDENTS:
        md_path = base / f"{name}.md"
        if not md_path.exists():
            print(f"  SKIP (no MD): {name}")
            continue
        print(f"\n{'='*60}\nCompiling {md_path.name} ...\n{'='*60}")
        compile_one(md_path)

    print("\nDone — all PDFs generated.")
