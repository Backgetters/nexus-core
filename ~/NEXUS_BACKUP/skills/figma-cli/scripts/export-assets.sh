#!/bin/bash
# Figma Asset Export Script
# Usage: export-assets.sh --file <file-key> [--format <format>] [--scale <scale>]

FIGMA_TOKEN="${FIGMA_ACCESS_TOKEN:-YOUR_TOKEN_HERE}"
FILE_KEY=""
FORMAT="svg"
SCALE="1"

while [[ $# -gt 0 ]]; do
  case $1 in
    --file) FILE_KEY="$2"; shift 2 ;;
    --format) FORMAT="$2"; shift 2 ;;
    --scale) SCALE="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [ -z "$FILE_KEY" ]; then
  echo "Usage: export-assets.sh --file <file-key> [--format <format>] [--scale <scale>]"
  exit 1
fi

echo "Exporting assets from Figma file: $FILE_KEY"
echo "Format: $FORMAT, Scale: $SCALE"

# Get file data
RESPONSE=$(curl -s "https://api.figma.com/v1/files/$FILE_KEY" \
  -H "X-Figma-Token: $FIGMA_TOKEN")

echo "File data received"
echo "$RESPONSE" | head -c 500

# Export images
IMAGES=$(curl -s "https://api.figma.com/v1/images/$FILE_KEY?format=$FORMAT&scale=$SCALE" \
  -H "X-Figma-Token: $FIGMA_TOKEN")

echo ""
echo "Image URLs:"
echo "$IMAGES" | grep -o '"https://[^"]*"' | tr -d '"'
