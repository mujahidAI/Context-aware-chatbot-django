# 🤝 Contributing Guide

Thank you for your interest in contributing to Nova AI Chatbot! This guide will help you get started.

---

## How to Contribute

### 1. 🐛 Report Bugs

Found a bug? [Open an issue](https://github.com/your-username/chatbot-react/issues/new) with:

- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

### 2. 💡 Suggest Features

Have an idea? Open an issue with the `enhancement` label:

- Describe the feature
- Explain the use case
- Propose implementation (optional)

### 3. 📝 Improve Documentation

Docs are in the `docs/` folder. Feel free to:

- Fix typos
- Add examples
- Clarify explanations

### 4. 🔧 Submit Code

Ready to code? Follow the process below.

---

## Development Process

### Step 1: Fork & Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR-USERNAME/chatbot-react.git
cd chatbot-react
```

### Step 2: Create Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

**Branch naming:**

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring

### Step 3: Setup Environment

See [Environment Setup](guides/environment-setup.md)

### Step 4: Make Changes

- Follow the code style
- Add tests if applicable
- Update documentation

### Step 5: Test

```bash
# Backend
cd backend
python manage.py test

# Frontend
cd frontend
npm run lint
```

### Step 6: Commit

```bash
git add .
git commit -m "feat: add model selection dropdown"
```

**Commit message format:**

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Formatting
- `refactor:` - Code restructuring
- `test:` - Tests
- `chore:` - Maintenance

### Step 7: Push & PR

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub.

---

## Code Style

### Python (Backend)

- Follow [PEP 8](https://pep8.org/)
- Use Black formatter
- Docstrings for functions
- Type hints encouraged

```python
def get_user_api_key(user: User) -> Optional[str]:
    """
    Retrieve and decrypt the user's API key.

    Args:
        user: The Django user object

    Returns:
        Decrypted API key or None if not configured
    """
    ...
```

### JavaScript (Frontend)

- ES6+ syntax
- Functional components
- Descriptive variable names
- JSDoc for complex functions

```javascript
/**
 * Fetch available AI models from the backend.
 * @param {string} token - JWT access token
 * @returns {Promise<Array>} List of model objects
 */
async function fetchModels(token) {
    ...
}
```

---

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests pass
- [ ] Documentation updated (if needed)
- [ ] Commit messages are clear

### PR Description

Include:

- What changes were made
- Why the changes were needed
- How to test
- Screenshots (for UI changes)

### Review Process

1. Maintainer reviews within 1-3 days
2. Address feedback if requested
3. PR is merged after approval

---

## Project Structure

```
chatbot-react/
├── backend/           # Django API
├── frontend/          # Next.js app
└── docs/              # Documentation
```

See [Architecture](ARCHITECTURE.md) for detailed structure.

---

## Getting Help

- 📖 Read the [documentation](DOCUMENTATION_HUB.md)
- 💬 Open a [discussion](https://github.com/your-username/chatbot-react/discussions)
- 🐛 Check [existing issues](https://github.com/your-username/chatbot-react/issues)

---

## Recognition

Contributors are recognized in:

- README.md contributors section
- Release notes

Thank you for contributing! 🙏
