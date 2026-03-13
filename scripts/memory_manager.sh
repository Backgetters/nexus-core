#!/bin/bash
# Memory Management Script - Enforces 200-line cap on memory files
# Run this before writing to memory files

MEMORY_DIR="/Users/tomegathericon/clawd/memory"
ARCHIVE_DIR="$MEMORY_DIR/archive"
MAX_LINES=200
ARCHIVE_CHUNK=100

# Create archive directory if it doesn't exist
mkdir -p "$ARCHIVE_DIR"

# Function to check and archive memory file if needed
check_and_archive() {
    local file="$1"
    local basename=$(basename "$file")
    
    if [ ! -f "$file" ]; then
        return 0
    fi
    
    local line_count=$(wc -l < "$file")
    
    if [ "$line_count" -gt "$MAX_LINES" ]; then
        # Archive the oldest 100 lines
        local archive_date=$(date +%Y%m%d_%H%M%S)
        local archive_file="$ARCHIVE_DIR/${basename%.md}_${archive_date}.md"
        
        # Extract oldest 100 lines to archive
        head -n $ARCHIVE_CHUNK "$file" > "$archive_file"
        
        # Remove oldest 100 lines from original file
        tail -n +$((ARCHIVE_CHUNK + 1)) "$file" > "$file.tmp"
        mv "$file.tmp" "$file"
        
        echo "Archived $ARCHIVE_CHUNK lines from $basename to $archive_file"
        return 0
    fi
    
    return 0
}

# Check all memory files
for memfile in "$MEMORY_DIR"/*.md; do
    if [ -f "$memfile" ]; then
        check_and_archive "$memfile"
    fi
done

# Check MEMORY.md specifically
if [ -f "/Users/tomegathericon/clawd/MEMORY.md" ]; then
    check_and_archive "/Users/tomegathericon/clawd/MEMORY.md"
fi

echo "Memory management complete - $(date)"
