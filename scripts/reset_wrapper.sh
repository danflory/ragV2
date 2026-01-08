#!/bin/bash
# Wrapper to run reset in a spawned terminal with proper completion handling

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
GRAVITAS_DIR="$(dirname "$SCRIPT_DIR")"

# Spawn a new terminal to run the reset
gnome-terminal --title="Gravitas Reset" -- bash -c "
    cd '$GRAVITAS_DIR' || exit 1
    
    # Run the reset script
    bash '$SCRIPT_DIR/reset_gravitas.sh'
    EXIT_CODE=\$?
    
    if [ \$EXIT_CODE -eq 0 ]; then
        echo ''
        echo '═════════════════════════════════════════════════════════════'
        echo '                    SUCCESS!!!!!!!!'
        echo '═════════════════════════════════════════════════════════════'
        echo ''
        echo 'Gravitas is now running on http://localhost:5050'
        echo 'Supervisor is running on http://localhost:8000'
        echo ''
        echo 'Press ENTER to close this window and return to terminal...'
        read
        # Switch focus back to parent terminal (if possible)
        wmctrl -a Terminal 2>/dev/null || true
    else
        echo ''
        echo '❌ RESET FAILED with exit code: '\$EXIT_CODE
        echo ''
        echo 'Press ENTER to close this window...'
        read
    fi
" &

echo "🚀 Reset process started in new terminal window..."
echo "   Watch that window for progress and completion status."
