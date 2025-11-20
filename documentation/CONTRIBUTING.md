# Contributing to Network Scanner

Thank you for your interest in contributing to Network Scanner! This document provides guidelines and instructions for contributing.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Documentation](#documentation)
- [Community](#community)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Expected Behavior

- ✅ Be respectful and inclusive
- ✅ Welcome newcomers
- ✅ Focus on what is best for the community
- ✅ Show empathy towards other community members
- ✅ Provide constructive feedback

### Unacceptable Behavior

- ❌ Harassment or discrimination
- ❌ Trolling or insulting comments
- ❌ Personal or political attacks
- ❌ Publishing others' private information

---

## How Can I Contribute?

### Reporting Bugs

**Before submitting a bug report:**
1. Check existing issues to avoid duplicates
2. Verify it's reproducible on the latest version
3. Collect relevant information (OS, Python version, error messages)

**Bug Report Template:**
```markdown
### Description
Brief description of the bug

### Steps to Reproduce
1. Step one
2. Step two
3. Step three

### Expected Behavior
What you expected to happen

### Actual Behavior
What actually happened

### Environment
- OS: Windows 11 / Ubuntu 22.04 / macOS 13
- Python Version: 3.11.5
- Scanner Version: 1.0.0
- Network Configuration: Home/Office/Cloud

### Error Messages
```
Paste full error message here
```

### Additional Context
Any other relevant information
```

### Suggesting Features

**Feature Request Template:**
```markdown
### Problem Statement
What problem does this feature solve?

### Proposed Solution
How should this feature work?

### Alternatives Considered
What other approaches did you consider?

### Use Cases
Real-world scenarios where this would be helpful

### Additional Context
Mockups, examples, or references
```

### Pull Requests

We welcome pull requests! Here's the process:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Make your changes**
4. **Test thoroughly**
5. **Commit your changes** (`git commit -m 'Add AmazingFeature'`)
6. **Push to the branch** (`git push origin feature/AmazingFeature`)
7. **Open a Pull Request**

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of networking concepts
- Familiarity with Python async/await (for advanced contributions)

### Fork and Clone

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/network-scanner.git
cd network-scanner

# Add upstream remote
git remote add upstream https://github.com/original-org/network-scanner.git
```

### Stay Updated

```bash
# Fetch upstream changes
git fetch upstream

# Merge into your local main
git checkout main
git merge upstream/main
```

---

## Development Setup

### Install Development Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development tools
```

### Development Tools

**requirements-dev.txt:**
```
pytest>=7.4.0           # Testing framework
pytest-asyncio>=0.21.0  # Async test support
pytest-cov>=4.1.0       # Code coverage
black>=23.7.0           # Code formatter
pylint>=2.17.0          # Linter
mypy>=1.4.0             # Type checker
ipython>=8.14.0         # Interactive shell
```

### Project Structure

```
network-scanner/
├── scanner.py              # Main scanner script
├── multi_network_scanner.py # Multi-network scanner
├── requirements.txt        # Dependencies
├── requirements-dev.txt    # Development dependencies
├── tests/                  # Test files
│   ├── test_scanner.py
│   ├── test_port_scan.py
│   └── test_exports.py
├── docs/                   # Documentation
│   ├── README.md
│   ├── INSTALLATION.md
│   └── ...
├── examples/               # Example scripts
│   ├── monitor_network.py
│   └── compare_scans.py
└── LICENSE
```

---

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) - Python's official style guide.

**Key Points:**
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black default)
- Use meaningful variable names
- Add docstrings to functions and classes
- Use type hints where appropriate

### Code Formatting

**Use Black for automatic formatting:**
```bash
# Format all Python files
black .

# Check without modifying
black --check .
```

**Example:**
```python
# Good
def scan_network(ip_range: str, timeout: float = 2.0) -> List[Device]:
    """
    Scan a network for active devices.
    
    Args:
        ip_range: Network range in CIDR notation (e.g., '192.168.1.0/24')
        timeout: Connection timeout in seconds
    
    Returns:
        List of discovered Device objects
    """
    devices = []
    # Implementation here
    return devices
```

### Linting

**Use pylint to check code quality:**
```bash
pylint scanner.py
```

**Aim for a score of 8.0 or higher**

### Type Checking

**Use mypy for type checking:**
```bash
mypy scanner.py --strict
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=scanner --cov-report=html

# Run specific test file
pytest tests/test_scanner.py

# Run specific test
pytest tests/test_scanner.py::test_arp_discovery
```

### Writing Tests

**Test File Example:**
```python
import pytest
from scanner import NetworkScanner, Device, ScanConfig

class TestNetworkScanner:
    """Test NetworkScanner class"""
    
    def test_config_creation(self):
        """Test creating scan configuration"""
        config = ScanConfig(network="192.168.1.0/24", ports="1-100")
        assert config.network == "192.168.1.0/24"
        assert config.ports == "1-100"
    
    @pytest.mark.asyncio
    async def test_port_scan(self):
        """Test port scanning functionality"""
        config = ScanConfig(network="127.0.0.1/32", ports="80")
        scanner = NetworkScanner(config)
        
        # Test scanning localhost
        device = Device(ip="127.0.0.1")
        await scanner.scan_device_ports(device)
        
        # Should have some result
        assert device.ports is not None
```

### Test Coverage Goals

- **Minimum:** 70% code coverage
- **Target:** 85% code coverage
- **Critical paths:** 100% coverage (scanning, exports)

---

## Submitting Changes

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
# Good commits
git commit -m "feat(scanner): add IPv6 support"
git commit -m "fix(export): correct CSV encoding for unicode"
git commit -m "docs(readme): update installation instructions"

# Bad commits
git commit -m "fixed stuff"
git commit -m "updates"
git commit -m "WIP"
```

### Pull Request Process

1. **Update documentation** if you've changed functionality
2. **Add tests** for new features
3. **Ensure all tests pass** (`pytest`)
4. **Update CHANGELOG.md** under [Unreleased]
5. **Fill out PR template** completely

**PR Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature that changes existing functionality)
- [ ] Documentation update

## Testing
- [ ] All tests pass (`pytest`)
- [ ] Added tests for new functionality
- [ ] Tested on Windows/Linux/macOS
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines (`black`, `pylint`)
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No console.log or debug statements

## Related Issues
Fixes #123
```

### Review Process

1. **Automated checks** must pass (tests, linting)
2. **At least one approval** from maintainers
3. **Address review comments** promptly
4. **Squash commits** before merging (if requested)

---

## Documentation

### Documentation Standards

**All documentation should:**
- Be clear and concise
- Include examples
- Be kept up-to-date with code changes
- Use proper markdown formatting
- Include command examples with expected output

### Updating Documentation

When code changes affect documentation:

1. Update relevant .md files
2. Update inline docstrings
3. Update command help text
4. Add examples if appropriate
5. Update CHANGELOG.md

### Documentation Files

- **README.md** - Main user guide
- **INSTALLATION.md** - Setup instructions
- **TROUBLESHOOTING.md** - Problem solving
- **COMMAND_EXAMPLES.md** - Output examples
- **EXAMPLES.md** - Use cases and workflows
- **QUICK_REFERENCE.md** - Command cheat sheet
- **CHANGELOG.md** - Version history
- **CONTRIBUTING.md** - This file!

---

## Community

### Communication Channels

- **GitHub Issues** - Bug reports, feature requests
- **GitHub Discussions** - Questions, ideas, showcase
- **Pull Requests** - Code contributions

### Getting Help

**For Contributors:**
- Read existing documentation
- Search closed issues and PRs
- Ask in GitHub Discussions
- Tag maintainers for guidance

**Response Times:**
- Issues: Within 48 hours
- Pull Requests: Within 1 week
- Security Issues: Within 24 hours

---

## Development Workflow

### Typical Contribution Flow

```bash
# 1. Update your fork
git checkout main
git pull upstream main

# 2. Create feature branch
git checkout -b feature/new-feature

# 3. Make changes
# Edit files...

# 4. Test changes
pytest
black .
pylint scanner.py

# 5. Commit changes
git add .
git commit -m "feat: add new feature"

# 6. Push to your fork
git push origin feature/new-feature

# 7. Create Pull Request on GitHub
```

### Working on Issues

1. **Comment on issue** to claim it
2. **Wait for assignment** from maintainers
3. **Create branch** from main
4. **Implement solution**
5. **Submit PR** referencing issue

---

## Code Review Guidelines

### For Contributors

**Before requesting review:**
- [ ] Code is complete and tested
- [ ] All tests pass locally
- [ ] Documentation is updated
- [ ] Commit messages follow conventions
- [ ] PR description is complete

**During review:**
- Respond to feedback promptly
- Be open to suggestions
- Ask questions if unclear
- Don't take feedback personally

### For Reviewers

**Focus on:**
- Correctness and functionality
- Code quality and readability
- Test coverage
- Documentation completeness
- Security implications
- Performance considerations

**Be:**
- Constructive and respectful
- Specific with feedback
- Timely in responses
- Encouraging to contributors

---

## Security

### Reporting Security Issues

**Do NOT** open public issues for security vulnerabilities.

**Instead:**
- Email: security@network-scanner.dev (if available)
- Use GitHub Security Advisories
- Include detailed description
- Provide steps to reproduce

**Response:**
- Acknowledgment within 24 hours
- Assessment within 1 week
- Fix released as soon as possible
- Credit given in release notes

---

## Recognition

### Contributors

All contributors are recognized in:
- GitHub contributors list
- Release notes
- CHANGELOG.md (for significant contributions)

### Maintainers

Current maintainers have merge rights and guide project direction.

**To become a maintainer:**
- Consistent high-quality contributions
- Demonstrated understanding of codebase
- Active in reviews and discussions
- Nomination by existing maintainers

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Questions?

- **General Questions:** GitHub Discussions
- **Bug Reports:** GitHub Issues
- **Security Concerns:** security@network-scanner.dev
- **Feature Ideas:** GitHub Discussions

---

**Thank you for contributing to Network Scanner!** 🎉

Your contributions help make network administration easier for everyone.
