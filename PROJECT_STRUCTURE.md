# Resume Builder - Project Structure

## Directory Layout

```
resume-builder/
├── flake.nix                 # Nix flake for package management
├── flake.lock                # Locked dependency versions
├── setup.py                  # Python setuptools configuration
├── resume_builder.py         # Main application (40KB, ~900 lines)
├── resume-builder.desktop    # Linux desktop entry
├── LICENSE                   # Apache 2.0 license
├── README.md                 # User documentation
├── CONTRIBUTING.md           # Developer guide
├── CHANGELOG.md              # Version history
├── CODE_REVIEW.md            # Code analysis and review
├── .gitignore                # Git ignore patterns
└── PROJECT_STRUCTURE.md      # This file
```

## File Descriptions

### Core Application
- **resume_builder.py** (40,631 bytes)
  - Main GTK3 application
  - ResumeBuilder class (main window)
  - Dialog classes for data entry
  - HTML generation with embedded CSS
  - Save/Load JSON functionality

### Packaging Files
- **flake.nix** (2,922 bytes)
  - Nix flake configuration
  - Package definition
  - Development shell
  - Desktop integration

- **flake.lock** (1,497 bytes)
  - Locked dependency versions
  - Reproducible builds

- **setup.py** (1,824 bytes)
  - Traditional Python packaging
  - PyPI metadata
  - Entry points

### Documentation
- **README.md** (3,763 bytes)
  - Installation instructions
  - Usage guide
  - Features overview

- **CONTRIBUTING.md** (1,714 bytes)
  - Contribution guidelines
  - Development setup
  - Code style

- **CHANGELOG.md** (1,173 bytes)
  - Version history
  - Release notes

- **CODE_REVIEW.md** (5,312 bytes)
  - Architecture analysis
  - Security review
  - Performance notes
  - Recommendations

### Configuration
- **.gitignore** (315 bytes)
  - Python artifacts
  - Generated files
  - IDE files

- **resume-builder.desktop** (269 bytes)
  - Linux desktop integration
  - Menu entry

### Legal
- **LICENSE** (9,648 bytes)
  - Full Apache 2.0 license text

## Technology Stack

### Runtime Dependencies
- Python 3.8+
- GTK 3.0
- PyGObject (gi)
- GObject Introspection

### Development Tools
- Nix (optional, for reproducible builds)
- Python setuptools (for traditional installation)
- Git (for version control)

### Build Systems
1. **Nix Flakes** (recommended)
   - Reproducible builds
   - Development shell
   - All dependencies managed

2. **Python setuptools** (traditional)
   - PyPI compatible
   - Standard Python packaging
   - Manual dependency installation

## Installation Methods

### 1. Nix Flakes
```bash
nix run github:yourusername/resume-builder
```

### 2. From Source
```bash
git clone https://github.com/yourusername/resume-builder.git
cd resume-builder
python3 resume_builder.py
```

### 3. System Installation
```bash
python3 setup.py install
resume-builder
```

## Data Flow

```
User Input (GTK Forms)
    ↓
ResumeBuilder.resume_data (dict)
    ↓
JSON Serialization (Save)
    ↓
HTML Template (Export)
    ↓
Browser/PDF (Print)
```

## Code Architecture

### Main Classes

1. **ResumeBuilder**
   - Main window
   - Form management
   - Data collection
   - File operations

2. **ExperienceDialog**
   - Job entry form
   - Bullet point editor

3. **ProjectDialog**
   - Project entry form
   - Description editor

4. **EducationDialog**
   - Education entry form
   - Notes field

5. **SkillDialog**
   - Skill category form
   - Skills list

### Key Methods

- `collect_form_data()` - Gather form inputs
- `generate_html()` - Create HTML output
- `on_export_clicked()` - Export to file
- `on_save_json()` - Save as JSON
- `on_load_json()` - Load from JSON

## Security Features

✅ HTML escaping for all user inputs
✅ Safe JSON serialization (no eval/pickle)
✅ File dialog validation
✅ No arbitrary code execution

## Future Enhancements

See CODE_REVIEW.md for detailed roadmap.

### Planned for v1.1
- Input validation (email, dates)
- Keyboard shortcuts
- Undo/redo functionality
- Unit tests

### Planned for v2.0
- Multiple templates
- PDF export
- Print preview
- Internationalization

## License

Apache License 2.0 - See LICENSE file for details.

## Contact

Report issues at: https://github.com/yourusername/resume-builder/issues
