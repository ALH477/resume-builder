# GTK Resume Builder

A GTK3-based desktop application for building professional HTML resumes with clean, modern styling.

## Features

- **Visual Form Interface**: Easy-to-use GTK interface for entering resume data
- **Multiple Sections**: Support for Experience, Projects, Education, and Skills
- **Save/Load**: Save your resume data as JSON and load it later for editing
- **HTML Export**: Generate a complete, styled HTML resume ready for printing or web use
- **Preview**: View a text preview of your HTML output before exporting

## Installation

### Using Nix Flakes (Recommended)

If you have Nix with flakes enabled:

```bash
# Run directly without installing
nix run github:yourusername/resume-builder

# Or install to your profile
nix profile install github:yourusername/resume-builder

# Then run
resume-builder
```

### Local Development with Nix

```bash
# Clone the repository
git clone https://github.com/yourusername/resume-builder.git
cd resume-builder

# Enter development shell
nix develop

# Run the application
python3 resume_builder.py

# Or build and run
nix build
./result/bin/resume-builder
```

### Traditional Installation

#### Requirements

- Python 3
- GTK 3
- PyGObject (gi)

#### Ubuntu/Debian:
```bash
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

#### Fedora:
```bash
sudo dnf install python3-gobject gtk3
```

#### Arch Linux:
```bash
sudo pacman -S python-gobject gtk3
```

## Usage

1. Run the application:
   ```bash
   python3 resume_builder.py
   ```
   or
   ```bash
   ./resume_builder.py
   ```

2. Fill in your information:
   - **Header**: Enter your name and professional subtitle
   - **Contact**: Add your website, email, and phone number
   - **Experience**: Click "Add Experience" to add job entries with bullet points
   - **Projects**: Click "Add Project" to add project entries
   - **Education**: Click "Add Education" to add educational background
   - **Skills**: Click "Add Skill Category" to organize your skills

3. Export your resume:
   - Click "Update Preview" to see a text preview
   - Click "Export HTML" to save your resume as an HTML file
   - Click "Save JSON" to save your data for future editing
   - Click "Load JSON" to load previously saved resume data

## Generated HTML Features

The exported HTML includes:
- Professional letter-sized layout (8.5" × 11")
- Print-optimized styling
- Timeline visualization with decorative elements
- Clean, modern typography using Open Sans font
- Sidebar layout with contact info and skills
- Responsive bullet points and formatting
- Ready for PDF conversion via browser print

## Tips

- **Dates**: Use formats like "2024", "Present", "Jan 2024" for consistency
- **Bullet Points**: Enter one achievement per line in the text area
- **Skills**: Separate individual skills with commas (e.g., "Python, JavaScript, C++")
- **Save Often**: Use "Save JSON" to preserve your work and make iterative edits

## File Structure

- `resume_builder.py` - Main application file
- `resume_data.json` - Saved resume data (created when you save)
- `resume.html` - Exported HTML resume (created when you export)

## Customization

The HTML template is embedded in the application. To customize the styling, you can:
1. Export an HTML file
2. Edit the `<style>` section directly in the HTML
3. Use the modified HTML as needed

The CSS uses CSS variables for easy customization of:
- Page dimensions
- Color scheme
- Spacing and padding
- Font sizes

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Credits

Created as a tool for building professional resumes with modern web standards.

