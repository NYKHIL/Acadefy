# Contributing to Acadefy

Thank you for your interest in contributing to Acadefy! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs
- Use the GitHub issue tracker
- Describe the bug clearly
- Include steps to reproduce
- Mention your environment (OS, Python version, etc.)

### Suggesting Features
- Open an issue with the "enhancement" label
- Describe the feature and its benefits
- Provide examples if possible

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed
4. **Test your changes**
   ```bash
   python backend/init_db.py
   python start_app.py
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add: your feature description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

## Development Setup

1. Clone your fork
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Initialize database: `python backend/init_db.py`
5. Start development server: `python start_app.py`

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions small and focused

## Questions?

Feel free to open an issue for any questions about contributing!