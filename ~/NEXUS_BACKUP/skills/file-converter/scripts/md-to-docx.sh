#!/bin/bash
# Convert Markdown to Word document
INPUT="$1"
OUTPUT="${2:-${INPUT%.md}.docx}"

echo "Converting $INPUT to Word document..."

if command -v pandoc &> /dev/null; then
    pandoc "$INPUT" -o "$OUTPUT" --reference-doc=reference.docx 2>/dev/null || pandoc "$INPUT" -o "$OUTPUT"
    echo "✅ Created: $OUTPUT"
else
    echo "Error: pandoc not installed. Install with: brew install pandoc"
    exit 1
fi
