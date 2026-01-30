# Contributing to Resume Builder

Thank you for your interest in contributing to Resume Builder! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/resume-builder.git`
3. Create a branch: `git checkout -b feature/your-feature-name`

## Development Environment

### Using Nix (Recommended)

```bash
nix develop
```

This will set up all necessary dependencies.

### Without Nix

Install the required dependencies:
- Python 3.8+
- GTK 3
- PyGObject

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and single-purpose

## Testing

Before submitting:
1. Test the application thoroughly
2. Ensure all dialogs work correctly
3. Verify HTML export produces valid output
4. Test save/load functionality

## Submitting Changes

1. Commit your changes with clear, descriptive messages
2. Push to your fork
3. Create a Pull Request with:
   - Clear description of changes
   - Any related issue numbers
   - Screenshots if UI changes are involved

## Bug Reports

When filing an issue, include:
- Operating system and version
- Python version
- GTK version
- Steps to reproduce
- Expected vs actual behavior
- Any error messages

## Feature Requests

Feature requests are welcome! Please:
- Check existing issues first
- Clearly describe the feature
- Explain the use case
- Consider offering to implement it

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

## Questions?

Feel free to open an issue for any questions about contributing.
