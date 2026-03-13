---
name: file-converter
description: Convert files between formats - Word, Excel, PDF, Images, and more. Generate reports, graphics, and documents for delivery.
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["pandoc", "libreoffice", "convert"] },
      },
  }
---

# File Converter

Convert documents, spreadsheets, and images between formats for professional delivery.

## Supported Conversions

### Documents:
- Word (.docx) ↔ PDF
- Word (.docx) ↔ Markdown
- PDF → Word (extract text)
- HTML → PDF
- Markdown → PDF

### Spreadsheets:
- Excel (.xlsx) → PDF
- Excel (.xlsx) → CSV
- CSV → Excel (.xlsx)
- JSON → Excel

### Images:
- PNG ↔ JPG
- Resize images
- Compress images
- PDF → Images (pages)

## Quick Start

```bash
# Convert Word to PDF
{baseDir}/scripts/doc-to-pdf.sh input.docx output.pdf

# Convert Excel to PDF
{baseDir}/scripts/excel-to-pdf.sh input.xlsx output.pdf

# Convert Markdown to Word
{baseDir}/scripts/md-to-docx.sh input.md output.docx

# Resize image
{baseDir}/scripts/resize-image.sh input.png 800 600 output.png

# Create report PDF from markdown
{baseDir}/scripts/generate-report.sh report.md report.pdf
```

## Report Generation

Generate professional reports with:
- Headers and footers
- Company branding
- Table of contents
- Charts and graphs

```bash
{baseDir}/scripts/create-report.sh --template business --output monthly-report.pdf
```
