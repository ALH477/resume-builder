# Installation Verification Guide

This document provides steps to verify your Resume Builder installation.

## Quick Start Test

### Method 1: Direct Execution
```bash
python3 resume_builder.py
```

**Expected Result:** Application window opens with form sections visible.

### Method 2: Nix Flake (if available)
```bash
nix run .#resume-builder
```

**Expected Result:** Application launches from Nix store.

### Method 3: Installed Binary
```bash
resume-builder
```

**Expected Result:** Application launches from system PATH.

## Functional Tests

### Test 1: Basic Form Entry
1. ✅ Enter name: "Test User"
2. ✅ Enter subtitle: "Software Developer"
3. ✅ Verify text appears in fields

### Test 2: Contact Information
1. ✅ Enter website: "https://example.com"
2. ✅ Enter email: "test@example.com"
3. ✅ Enter phone: "555-1234"
4. ✅ Verify all fields accept input

### Test 3: Add Experience
1. ✅ Click "Add Experience"
2. ✅ Dialog opens
3. ✅ Fill in:
   - Title: "Developer"
   - Company: "Tech Corp"
   - Location: "Remote"
   - Start Date: "2020"
   - End Date: "Present"
   - Bullets: "Built applications\nManaged team"
4. ✅ Click OK
5. ✅ Entry appears in list
6. ✅ Can remove entry

### Test 4: Add Project
1. ✅ Click "Add Project"
2. ✅ Fill in project details
3. ✅ Verify entry added

### Test 5: Add Education
1. ✅ Click "Add Education"
2. ✅ Fill in degree information
3. ✅ Verify entry added

### Test 6: Add Skills
1. ✅ Click "Add Skill Category"
2. ✅ Enter category: "Programming"
3. ✅ Enter skills: "Python, C++, JavaScript"
4. ✅ Verify entry added

### Test 7: Save JSON
1. ✅ Click "Save JSON"
2. ✅ Choose location
3. ✅ File saves successfully
4. ✅ JSON file contains data

### Test 8: Load JSON
1. ✅ Click "Load JSON"
2. ✅ Select saved file
3. ✅ Data populates form
4. ✅ All entries restored

### Test 9: Export HTML
1. ✅ Click "Export HTML"
2. ✅ Choose location
3. ✅ File saves successfully
4. ✅ Open HTML in browser
5. ✅ Resume displays correctly
6. ✅ Print preview looks good

### Test 10: Preview
1. ✅ Click "Update Preview"
2. ✅ Preview text appears
3. ✅ Contains resume data

## Edge Cases

### Test 11: Empty Fields
1. ✅ Try exporting with no data
2. ✅ Application handles gracefully

### Test 12: Special Characters
1. ✅ Enter: `<script>alert('xss')</script>`
2. ✅ Export HTML
3. ✅ Verify HTML escaping works
4. ✅ No script execution in browser

### Test 13: Very Long Text
1. ✅ Enter 1000+ character bullet point
2. ✅ Application doesn't crash
3. ✅ HTML renders correctly

### Test 14: Unicode Characters
1. ✅ Enter: "Résumé • 中文 • Emoji 🚀"
2. ✅ Save and load
3. ✅ Export HTML
4. ✅ Characters preserved

## Platform-Specific Tests

### Linux Desktop Integration
1. ✅ `.desktop` file installed
2. ✅ Application appears in menu
3. ✅ Icon displays (if available)
4. ✅ Launches from menu

### GTK Theme
1. ✅ Application respects system theme
2. ✅ Dark mode works (if enabled)
3. ✅ Fonts render correctly

## Performance Tests

### Test 15: Large Resume
1. ✅ Add 10 experience entries
2. ✅ Add 20 projects
3. ✅ Application remains responsive
4. ✅ Export completes quickly (<2s)

### Test 16: Multiple Save/Load
1. ✅ Save 10 times
2. ✅ Load 10 times
3. ✅ No memory leaks
4. ✅ No slowdown

## Error Handling

### Test 17: Invalid JSON
1. ✅ Create corrupted JSON file
2. ✅ Try to load
3. ✅ Error message displayed
4. ✅ Application doesn't crash

### Test 18: Read-Only Directory
1. ✅ Try to save to `/`
2. ✅ Error handled gracefully

### Test 19: Disk Full (simulation)
1. ✅ Handle export failure
2. ✅ User notified

## Dependency Check

### Python Version
```bash
python3 --version
# Should be 3.8 or higher
```

### GTK Version
```bash
pkg-config --modversion gtk+-3.0
# Should be 3.0 or higher
```

### PyGObject
```python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
print("PyGObject OK")
```

## Nix-Specific Tests

### Test 20: Flake Check
```bash
nix flake check
```
**Expected:** No errors

### Test 21: Build
```bash
nix build
```
**Expected:** Successful build, `result` symlink created

### Test 22: Development Shell
```bash
nix develop
```
**Expected:** Shell with all dependencies

## HTML Output Validation

### Test 23: W3C Validation
1. ✅ Export HTML
2. ✅ Upload to https://validator.w3.org/
3. ✅ Should pass validation

### Test 24: Browser Compatibility
1. ✅ Open in Firefox
2. ✅ Open in Chrome
3. ✅ Open in Safari
4. ✅ Consistent rendering

### Test 25: Print Test
1. ✅ Open HTML
2. ✅ Print preview (Ctrl+P)
3. ✅ Fits on one page
4. ✅ No cut-off content

## Accessibility

### Test 26: Keyboard Navigation
1. ✅ Tab through all fields
2. ✅ Enter submits dialogs
3. ✅ Escape cancels dialogs

### Test 27: Screen Reader (optional)
1. ⚠️ Test with Orca/NVDA
2. ⚠️ Labels are announced

## Success Criteria

All ✅ tests should pass. Tests marked ⚠️ are optional but recommended.

## Reporting Issues

If any test fails:
1. Note the test number
2. Describe what happened vs expected
3. Include:
   - OS and version
   - Python version
   - GTK version
   - Error messages
4. Report at: https://github.com/yourusername/resume-builder/issues

## Sign-Off

Installation verified by: _______________
Date: _______________
Platform: _______________
All critical tests passed: [ ] Yes [ ] No
