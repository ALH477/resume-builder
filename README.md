# Resume Builder

A GTK3 and web-based application for creating professional HTML resumes with clean, modern styling.

## Overview

Resume Builder provides two interfaces for generating polished, professional resumes:

- **Desktop Interface (GTK3)**: Full-featured desktop application with visual form editing
- **Web Interface (Flask)**: Browser-based application suitable for containers and remote access

Both interfaces produce identical, professionally styled HTML output optimized for printing and PDF conversion.

## Features

### Desktop Interface
- Visual form interface for entering resume data
- Multiple sections: Experience, Projects, Education, and Skills
- Save and load resume data as JSON for future editing
- Live preview of HTML output
- Keyboard shortcuts: Ctrl+S (save), Ctrl+O (load), Ctrl+E (export), Ctrl+P (preview)

### Web Interface
- Responsive web UI accessible from any browser
- REST API for programmatic access
- Real-time preview updates
- JSON import/export functionality
- Docker-ready deployment

### Generated HTML Output
- Professional letter-sized layout (8.5" x 11")
- Print-optimized styling
- Timeline visualization with decorative elements
- Clean typography using Open Sans font
- Sidebar layout with contact information and skills
- PDF-ready via browser print function

## Installation

### Nix Flakes (Recommended)

For systems with Nix and flakes enabled:

```bash
# Run directly without installation
nix run github:ALH477/resume-builder

# Install to user profile
nix profile install github:ALH477/resume-builder

# Launch application
resume-builder
```

### Local Development with Nix

```bash
# Clone the repository
git clone https://github.com/ALH477/resume-builder.git
cd resume-builder

# Enter development shell
nix develop

# Run the desktop application
python3 resume_builder.py

# Or build and run
nix build
./result/bin/resume-builder
```

### Traditional Installation

#### Requirements
- Python 3.8+
- GTK 3.0
- PyGObject (gi)

#### Ubuntu/Debian
```bash
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

#### Fedora
```bash
sudo dnf install python3-gobject gtk3
```

#### Arch Linux
```bash
sudo pacman -S python-gobject gtk3
```

### Web Interface Installation

```bash
# Install dependencies
pip install flask

# Run web server
python3 resume_builder.py --web --port 5000

# Access at http://localhost:5000
```

## Usage

### Desktop Application

1. Launch the application:
   ```bash
   python3 resume_builder.py
   ```

2. Enter your information using the form sections:
   - **Header**: Full name and professional subtitle
   - **Contact**: Website, email, and phone number
   - **Experience**: Add work history with bullet points
   - **Projects**: Add notable projects with descriptions
   - **Education**: Add educational background
   - **Skills**: Organize skills by category

3. Export your resume:
   - Use **Update Preview** to view HTML output
   - Use **Export HTML** to save the resume file
   - Use **Save JSON** to preserve data for later editing
   - Use **Load JSON** to restore previously saved data

### Web Interface

1. Start the web server:
   ```bash
   python3 resume_builder.py --web --port 5000
   ```

2. Open http://localhost:5000 in your web browser

3. Use the form to enter resume data and click Preview or Export

### Docker Deployment

#### Web Container (Recommended)
```bash
docker run -p 5000:5000 alh477/resume-builder:web
```

#### Desktop Container (Requires X11 Forwarding)
```bash
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix alh477/resume-builder:latest
```

## Tips

- **Date Formats**: Use consistent formats such as "2024", "Present", or "Jan 2024"
- **Bullet Points**: Enter one achievement per line in text areas
- **Skills**: Separate individual skills with commas (e.g., "Python, JavaScript, C++")
- **Data Preservation**: Use the Save JSON feature regularly to preserve work

## File Structure

| File | Description |
|------|-------------|
| `resume_builder.py` | Main application with GTK and web interfaces |
| `web_app.py` | Flask web application module |
| `setup.py` | Python package configuration |
| `flake.nix` | Nix flake for reproducible builds |
| `Dockerfile` | Container definition for web interface |

## API Reference (Web Interface)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web UI |
| `/api/preview` | POST | Generate HTML preview |
| `/api/export` | POST | Download HTML file |
| `/api/save` | POST | Download JSON data |
| `/api/load` | POST | Upload and load JSON data |

## Customization

The HTML template is embedded in the application. To customize the output:

1. Export an HTML file
2. Modify the `<style>` section directly
3. Use the customized output as needed

The CSS uses CSS variables for easy customization of:
- Page dimensions
- Color scheme
- Spacing and padding
- Font sizes and typography

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome. Please submit pull requests through GitHub.

## Repository

- GitHub: https://github.com/ALH477/resume-builder
- Docker Hub: https://hub.docker.com/r/alh477/resume-builder
