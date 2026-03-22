#!/bin/bash
# Echotyne Business Intelligence Report Generator
# Usage: ./generate_bi_report.sh [client_name] [industry_focus]

CLIENT_NAME="${1:-Sample Client}"
INDUSTRY_FOCUS="${2:-AI/Automation}"
WEEK_OF=$(date +"%Y-%m-%d")
NEXT_REPORT=$(date -v+7d +"%Y-%m-%d" 2>/dev/null || date -d "+7 days" +"%Y-%m-%d")

TEMPLATE="~/clawd/echotyne/services/business-intelligence/templates/weekly_report_template.md"
OUTPUT_DIR="~/clawd/echotyne/services/business-intelligence/reports"
OUTPUT_FILE="$OUTPUT_DIR/${CLIENT_NAME// /_}_${WEEK_OF}.md"

# Create report from template
cp "$TEMPLATE" "$OUTPUT_FILE"

# Replace placeholders
sed -i '' "s/{{WEEK_OF}}/$WEEK_OF/g" "$OUTPUT_FILE"
sed -i '' "s/{{CLIENT_NAME}}/$CLIENT_NAME/g" "$OUTPUT_FILE"
sed -i '' "s/{{INDUSTRY_FOCUS}}/$INDUSTRY_FOCUS/g" "$OUTPUT_FILE"
sed -i '' "s/{{NEXT_REPORT_DATE}}/$NEXT_REPORT/g" "$OUTPUT_FILE"

echo "Report generated: $OUTPUT_FILE"
