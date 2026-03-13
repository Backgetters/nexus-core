#!/bin/bash
# ACTIVATE NEXUS LEVEL 10 AUTONOMY
# Run this with: sudo bash activate_level10.sh

echo "========================================"
echo "NEXUS Level 10 Autonomy Activation"
echo "========================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ This script must be run with sudo"
    echo "Usage: sudo bash ~/clawd/activate_level10.sh"
    exit 1
fi

# Install sudoers config
echo "Installing sudo configuration..."
cp ~/clawd/sudoers_nexus.txt /etc/sudoers.d/nexus-autonomy
chmod 440 /etc/sudoers.d/nexus-autonomy
chown root:wheel /etc/sudoers.d/nexus-autonomy

# Verify syntax
visudo -c -f /etc/sudoers.d/nexus-autonomy
if [ $? -eq 0 ]; then
    echo "✅ Sudo configuration installed and verified"
else
    echo "❌ Sudo configuration error - restoring"
    rm /etc/sudoers.d/nexus-autonomy
    exit 1
fi

# Create kill switch file (disabled by default)
touch ~/clawd/.KILL_SWITCH_DISABLED
chmod 644 ~/clawd/.KILL_SWITCH_DISABLED

# Set up logging
mkdir -p ~/clawd/logs
chmod 755 ~/clawd/logs

echo ""
echo "========================================"
echo "✅ LEVEL 10 AUTONOMY ACTIVATED"
echo "========================================"
echo ""
echo "NEXUS can now:"
echo "  • Run sudo without password (for approved commands)"
echo "  • Install system packages"
echo "  • Modify system configurations"
echo "  • Self-restart and self-heal"
echo ""
echo "Safety features active:"
echo "  • All sudo logged to ~/clawd/logs/root_activity.log"
echo "  • Kill switch: touch ~/clawd/.KILL_SWITCH to disable"
echo "  • Daily backups to ~/Backups/nexus/"
echo "  • Recovery user can fix NEXUS if corrupted"
echo ""
echo "To verify: sudo whoami (should say 'root')"
echo ""
echo "WARNING: This grants significant system access."
echo "Monitor ~/clawd/logs/root_activity.log for audit trail."
