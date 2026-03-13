#!/bin/bash
# Resize image to specific dimensions
INPUT="$1"
WIDTH="$2"
HEIGHT="$3"
OUTPUT="${4:-${INPUT%.*}_resized.${INPUT##*.}}"

echo "Resizing $INPUT to ${WIDTH}x${HEIGHT}..."

if command -v convert &> /dev/null; then
    convert "$INPUT" -resize "${WIDTH}x${HEIGHT}>" "$OUTPUT"
    echo "✅ Resized: $OUTPUT"
elif command -v sips &> /dev/null; then
    # macOS built-in
    sips -Z "${WIDTH}" "$INPUT" --out "$OUTPUT"
    echo "✅ Resized: $OUTPUT"
else
    echo "Error: ImageMagick not installed. Install with: brew install imagemagick"
    exit 1
fi
