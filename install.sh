#!/bin/bash
# Quick install script for Resume Builder
# Copyright 2025 Resume Builder Contributors
# Licensed under Apache-2.0

set -e

echo "Resume Builder Installation Script"
echo "===================================="
echo ""

# Detect installation method
if command -v nix &> /dev/null; then
    if nix --version | grep -q "flakes"; then
        echo "✓ Nix with flakes detected"
        echo ""
        echo "Recommended installation method:"
        echo "  nix profile install ."
        echo ""
        echo "Or run directly:"
        echo "  nix run ."
        echo ""
        read -p "Install with Nix now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            nix profile install .
            echo ""
            echo "✓ Installation complete!"
            echo "Run with: resume-builder"
        fi
        exit 0
    else
        echo "⚠ Nix detected but flakes not enabled"
        echo "Enable flakes in ~/.config/nix/nix.conf:"
        echo "  experimental-features = nix-command flakes"
    fi
fi

# Check for Python and GTK
echo "Checking dependencies..."
echo ""

MISSING_DEPS=0

if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found"
    MISSING_DEPS=1
else
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✓ Python $PYTHON_VERSION"
fi

if ! python3 -c "import gi" 2>/dev/null; then
    echo "✗ PyGObject not found"
    MISSING_DEPS=1
else
    echo "✓ PyGObject installed"
fi

if ! python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" 2>/dev/null; then
    echo "✗ GTK 3 not found"
    MISSING_DEPS=1
else
    echo "✓ GTK 3 installed"
fi

echo ""

if [ $MISSING_DEPS -eq 1 ]; then
    echo "Missing dependencies detected!"
    echo ""
    echo "Install with:"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0"
    echo ""
    echo "Fedora:"
    echo "  sudo dnf install python3-gobject gtk3"
    echo ""
    echo "Arch:"
    echo "  sudo pacman -S python-gobject gtk3"
    echo ""
    exit 1
fi

echo "All dependencies satisfied!"
echo ""
echo "Installation options:"
echo ""
echo "1. Run directly (no installation):"
echo "   python3 resume_builder.py"
echo ""
echo "2. Install with pip:"
echo "   python3 -m pip install --user ."
echo "   resume-builder"
echo ""
echo "3. Install with setup.py:"
echo "   python3 setup.py install --user"
echo "   resume-builder"
echo ""

read -p "Install with pip now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 -m pip install --user .
    echo ""
    echo "✓ Installation complete!"
    echo ""
    echo "Run with: resume-builder"
    echo "Or: ~/.local/bin/resume-builder"
    echo ""
    echo "Add to PATH if needed:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
else
    echo ""
    echo "No problem! Run directly with:"
    echo "  python3 resume_builder.py"
fi
