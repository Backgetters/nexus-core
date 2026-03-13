#!/bin/bash
# Convert Excel to PDF
INPUT="$1"
OUTPUT="${2:-${INPUT%.xlsx}.pdf}"

echo "Converting $INPUT to PDF..."

if command -v libreoffice &> /dev/null; then
    libreoffice --headless --convert-to pdf --outdir "$(dirname "$OUTPUT")" "$INPUT"
elif command -v soffice &> /dev/null; then
    soffice --headless --convert-to pdf --outdir "$(dirname "$OUTPUT")" "$INPUT"
else
    echo "Error: LibreOffice not installed"
    exit 1
fi

echo "✅ Created: $OUTPUT"
