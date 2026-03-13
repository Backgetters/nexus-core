#!/bin/bash
# Playwright Automation Script
# Usage: automate.sh --url <url> --action <action> [options]

URL=""
ACTION="screenshot"
OUTPUT="screenshot.png"
SELECTOR=""
DATA=""
TIMEOUT=30000

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --url) URL="$2"; shift 2 ;;
    --action) ACTION="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --selector) SELECTOR="$2"; shift 2 ;;
    --data) DATA="$2"; shift 2 ;;
    --timeout) TIMEOUT="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [ -z "$URL" ]; then
  echo "Usage: automate.sh --url <url> --action <action>"
  echo "Actions: screenshot, extract-text, fill-form, click, wait, scroll"
  exit 1
fi

# Check if npx is available
if ! command -v npx &> /dev/null; then
  echo "Error: npx not found. Install Node.js first."
  exit 1
fi

# Create temporary Node.js script
TMP_SCRIPT=$(mktemp)
cat > "$TMP_SCRIPT" << 'EOF'
const { chromium } = require('playwright');

(async () => {
  const args = process.argv.slice(2);
  const url = args[0];
  const action = args[1];
  const selector = args[2] || '';
  const data = args[3] || '{}';
  const output = args[4] || 'screenshot.png';
  
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  try {
    await page.goto(url, { waitUntil: 'networkidle' });
    
    switch(action) {
      case 'screenshot':
        await page.screenshot({ path: output, fullPage: true });
        console.log(`Screenshot saved to: ${output}`);
        break;
        
      case 'extract-text':
        const text = await page.evaluate(() => document.body.innerText);
        console.log(text);
        break;
        
      case 'click':
        if (!selector) {
          console.error('Error: --selector required for click action');
          process.exit(1);
        }
        await page.click(selector);
        console.log(`Clicked: ${selector}`);
        break;
        
      case 'fill-form':
        const formData = JSON.parse(data);
        for (const [key, value] of Object.entries(formData)) {
          await page.fill(`[name="${key}"], #${key}, input[placeholder*="${key}"]`, value);
        }
        console.log('Form filled');
        break;
        
      case 'wait':
        if (!selector) {
          console.error('Error: --selector required for wait action');
          process.exit(1);
        }
        await page.waitForSelector(selector, { timeout: 30000 });
        console.log(`Element found: ${selector}`);
        break;
        
      case 'scroll':
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
        console.log('Scrolled to bottom');
        break;
        
      default:
        console.error(`Unknown action: ${action}`);
        process.exit(1);
    }
    
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
EOF

# Run the script
npx playwright install chromium 2>/dev/null || true
node "$TMP_SCRIPT" "$URL" "$ACTION" "$SELECTOR" "$DATA" "$OUTPUT"
EXIT_CODE=$?

# Cleanup
rm "$TMP_SCRIPT"

exit $EXIT_CODE
