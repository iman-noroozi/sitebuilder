# Contributing to Site Builder

Thank you for your interest in contributing to Site Builder! We welcome contributions from the community and are grateful for your help in making this project better.

## 🤝 How to Contribute

### Reporting Bugs
- Use GitHub Issues to report bugs
- Provide detailed reproduction steps
- Include system information (OS, Python version, etc.)
- Add screenshots or error logs if applicable

### Suggesting Features
- Use GitHub Issues to suggest new features
- Describe the feature and its benefits
- Consider the impact on existing functionality
- Provide use cases and examples

### Code Contributions
- Fork the repository
- Create a feature branch
- Make your changes
- Add tests for new functionality
- Ensure all tests pass
- Submit a pull request

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git
- Docker (optional)

### Local Development
```bash
# 1. Fork and clone the repository
git clone https://github.com/your-username/sitebuilder.git
cd sitebuilder

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r backend/requirements.txt
npm install

# 4. Setup environment
cp .env.example .env
# Edit .env with your configuration

# 5. Run migrations
python backend/manage.py migrate

# 6. Start development servers
python backend/manage.py runserver &
npm run dev &
```

### Docker Development
```bash
# Build and start with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:8000
```

## 📝 Code Style

### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions small and focused
- Use meaningful variable names

### JavaScript
- Use ESLint configuration
- Follow modern ES6+ syntax
- Use meaningful variable names
- Comment complex logic
- Keep functions small and focused

### CSS/SCSS
- Use BEM methodology
- Keep selectors specific
- Use CSS custom properties
- Mobile-first approach
- Comment complex styles

## 🧪 Testing

### Running Tests
```bash
# Python tests
python -m pytest backend/tests/

# JavaScript tests
npm test

# Coverage report
python -m pytest --cov=backend backend/tests/
```

### Writing Tests
- Write tests for new features
- Test edge cases and error conditions
- Use descriptive test names
- Keep tests independent and isolated
- Mock external dependencies

## 📚 Documentation

### Code Documentation
- Write docstrings for all functions and classes
- Use type hints for better IDE support
- Comment complex algorithms
- Keep README files updated

### API Documentation
- Document all API endpoints
- Include request/response examples
- Specify authentication requirements
- Document error responses

## 🔄 Pull Request Process

### Before Submitting
1. Ensure all tests pass
2. Update documentation if needed
3. Add tests for new features
4. Follow code style guidelines
5. Rebase on latest main branch

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## 🏷️ Commit Message Format

Use conventional commit format:
```
type(scope): description

feat: add new feature
fix: resolve bug
docs: update documentation
style: formatting changes
refactor: code refactoring
test: add or update tests
chore: maintenance tasks
```

Examples:
- `feat: add AI content generation`
- `fix: resolve mobile layout issue`
- `docs: update installation guide`
- `refactor: improve error handling`

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - OS and version
   - Python version
   - Node.js version
   - Browser (if applicable)

2. **Steps to Reproduce**
   - Clear, numbered steps
   - Expected vs actual behavior
   - Screenshots or videos if helpful

3. **Error Information**
   - Full error messages
   - Stack traces
   - Log files if relevant

## 💡 Feature Requests

When suggesting features, please include:

1. **Problem Description**
   - What problem does this solve?
   - Who would benefit from this feature?

2. **Proposed Solution**
   - How should this feature work?
   - Any design considerations?

3. **Alternatives Considered**
   - Other ways to solve this problem
   - Why this approach is better

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation
- GitHub contributors page

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Discord**: For real-time chat and support
- **Email**: contact@sitebuilder.com

## 📋 Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior
- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or inflammatory comments
- Personal attacks or political discussions
- Spam or off-topic discussions

## 🎯 Areas for Contribution

### High Priority
- AI content generation improvements
- Performance optimizations
- Accessibility enhancements
- Mobile responsiveness
- Documentation improvements

### Medium Priority
- New export formats
- Additional language support
- UI/UX improvements
- Testing coverage
- Code refactoring

### Low Priority
- New templates
- Additional integrations
- Advanced features
- Experimental features

## 🔧 Development Tools

### Recommended IDEs
- **VS Code** with Python and JavaScript extensions
- **PyCharm** for Python development
- **WebStorm** for JavaScript development

### Useful Extensions
- Python
- JavaScript (ES6) code snippets
- GitLens
- Prettier
- ESLint
- Django

### Git Hooks
```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

## 📊 Project Structure

```
sitebuilder/
├── backend/                 # Django backend
│   ├── sitebuilder_app/    # Main Django app
│   ├── requirements.txt    # Python dependencies
│   └── manage.py          # Django management
├── frontend/              # Frontend assets
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript files
│   └── assets/           # Static assets
├── docs/                 # Documentation
├── tests/                # Test files
├── .github/              # GitHub workflows
└── README.md            # Project documentation
```

## 🚀 Release Process

1. **Version Bumping**
   - Update version in setup.py
   - Update CHANGELOG.md
   - Create release notes

2. **Testing**
   - Run full test suite
   - Manual testing
   - Performance testing

3. **Release**
   - Create GitHub release
   - Tag version
   - Deploy to production

## 📈 Performance Guidelines

- Keep bundle sizes small
- Optimize images and assets
- Use lazy loading where appropriate
- Minimize API calls
- Cache frequently accessed data

## 🔒 Security Guidelines

- Never commit secrets or API keys
- Use environment variables for configuration
- Validate all user inputs
- Keep dependencies updated
- Follow security best practices

---

Thank you for contributing to Site Builder! Your efforts help make this project better for everyone. 🎉