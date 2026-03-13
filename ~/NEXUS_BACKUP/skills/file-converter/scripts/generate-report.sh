#!/bin/bash
# Generate professional PDF report from markdown
INPUT="$1"
OUTPUT="${2:-${INPUT%.md}.pdf}"
TEMPLATE="${3:-business}"

echo "Generating report: $INPUT → $OUTPUT"

if command -v pandoc &> /dev/null; then
    pandoc "$INPUT" -o "$OUTPUT" \
        --pdf-engine=xelatex \
        --variable geometry:margin=1in \
        --variable fontsize=11pt \
        --variable documentclass=article \
        --include-in-header=<(echo '\\usepackage{fancyhdr} \\pagestyle{fancy} \\fancyhead[C]{Jones Net Group} \\fancyfoot[C]{\\thepage}') \
        2>/dev/null || echo "Using basic conversion..."
    
    # Fallback if xelatex not available
    if [ ! -f "$OUTPUT" ]; then
        pandoc "$INPUT" -o "$OUTPUT"
    fi
    
    echo "✅ Report generated: $OUTPUT"
else
    echo "Error: pandoc not installed"
    exit 1
fi
