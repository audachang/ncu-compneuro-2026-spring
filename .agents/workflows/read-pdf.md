---
description: How to extract text from PDF files, including CJK (Chinese/Japanese/Korean) PDFs
---

# PDF Text Extraction Workflow

## Problem Context
Many PDFs—especially those exported from Word, Google Docs, or presentation tools—embed Chinese text as **images or custom-encoded fonts** that lack proper ToUnicode mappings. Standard text extraction libraries (PyPDF2, pdfminer) will return only bullet markers or garbled fragments.

## Recommended Approach (Tiered)

### Tier 1: Try `pymupdf` (fitz) text extraction first
// turbo
```bash
pip install pymupdf
```

```python
import fitz
doc = fitz.open("path/to/file.pdf")
for page in doc:
    text = page.get_text()
    print(text)
```

**If this returns complete, readable text → done.** This works for most well-formed PDFs.

### Tier 2: If Tier 1 returns only bullet markers or garbled text
The PDF likely has embedded images or custom fonts without Unicode mappings. **Convert pages to images and read them visually:**

// turbo
```python
import fitz
doc = fitz.open("path/to/file.pdf")
for i in range(len(doc)):
    page = doc[i]
    pix = page.get_pixmap(dpi=200)  # 200 DPI is sufficient for reading
    pix.save(f"page_{i+1}.png")
```

Then use `view_file` on each PNG image to read the content visually.

### Tier 3: If OCR is needed for scanned documents
```bash
pip install pytesseract Pillow
```

```python
import pytesseract
from PIL import Image
text = pytesseract.image_to_string(Image.open("page_1.png"), lang="chi_tra+eng")
```
Requires Tesseract OCR installed with Chinese language pack.

## What NOT to Do
- **Don't use PyPDF2 for CJK PDFs** — it frequently fails on Chinese text extraction.
- **Don't use pdfminer.six as first choice** — it handles layout well but still fails on image-embedded or custom-font CJK text.
- **Don't try browser-based PDF reading** — local `file://` URLs are blocked by the browser security policy.

## Diagnostic Check
To determine which tier is needed, check the font metadata:
```python
import fitz
doc = fitz.open("path/to/file.pdf")
page = doc[0]
fonts = page.get_fonts()
print(fonts)  # If fonts lack CID mappings or show only symbol fonts, go to Tier 2
```
