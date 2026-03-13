#!/bin/bash
# Convert Word document to PDF
INPUT="$1"
OUTPUT="${2:-${INPUT%.docx}.pdf}"

echo "Converting $INPUT to PDF..."

# Check if libreoffice is available
if command -v libreoffice &> /dev/null; then
    libreoffice --headless --convert-to pdf --outdir "$(dirname "$OUTPUT")" "$INPUT"
elif command -v soffice &> /dev/null; then
    soffice --headless --convert-to pdf --outdir "$(dirname "$OUTPUT")" "$INPUT"
else
    echo "Error: LibreOffice not installed. Install with: brew install --cask libreoffice"
    exit 1
fi

echo "✅ Created: $OUTPUT"
