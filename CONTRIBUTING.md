# 🤝 Contributing to Lottery Predictor

Thank you for considering contributing to this project! We welcome contributions from everyone.

---

## How to Contribute

### Reporting Bugs

**Before submitting a bug report:**
- Check existing issues to avoid duplicates
- Use the latest version of the code
- Collect relevant information (OS, Python version, error messages)

**When submitting:**
1. Use GitHub Issues
2. Provide clear title and description
3. Include steps to reproduce
4. Add expected vs actual behavior
5. Include error messages/logs
6. Specify your environment

**Example:**
```
Title: "Triplet generation fails with max_attempts=10000"

Description:
Combination #16 (triplet) often fails to generate.

Steps to reproduce:
1. Run lottery_predictor.py
2. Observe console output for combination #16

Expected: Valid triplet combination
Actual: "⚠️ #16: Не удалось сгенерировать"

Environment:
- OS: Ubuntu 20.04
- Python: 3.9.5
- Dependencies: From requirements.txt
```

---

### Suggesting Enhancements

We welcome ideas for:
- New ML models
- Additional combination patterns
- Performance improvements
- Better data visualization
- Documentation improvements

**Enhancement template:**
```
Title: "Add LSTM model for time-series prediction"

Description:
LSTM networks excel at sequence prediction. Adding this could improve accuracy.

Benefits:
- Better temporal pattern recognition
- Potentially lower MAE
- Ensemble with existing models

Considerations:
- Requires additional dependency (tensorflow/pytorch)
- Longer training time
- More complex maintenance
```

---

### Pull Requests

**Process:**

1. **Fork the repository**
   ```bash
   # On GitHub, click "Fork"
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/lottery-predictor.git
   cd lottery-predictor
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

4. **Make changes**
   - Write clean, documented code
   - Follow existing style
   - Add tests if applicable

5. **Test your changes**
   ```bash
   python lottery_predictor.py
   # Verify output
   ```

6. **Commit**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```

7. **Push**
   ```bash
   git push origin feature/amazing-feature
   ```

8. **Create Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Describe your changes
   - Link related issues

---

## Code Style

### Python Style Guide

Follow PEP 8 with these specifics:

**Indentation:**
```python
# 4 spaces (no tabs)
def function():
    if condition:
        do_something()
```

**Naming:**
```python
# Classes: PascalCase
class LotteryPredictor:
    pass

# Functions/methods: snake_case
def calculate_frequencies():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_ATTEMPTS = 10000
```

**Docstrings:**
```python
def generate_combination(self, target_rank, isolated=True):
    """
    Generate one combination with specified conditions.
    
    Args:
        target_rank (float): Target mean frequency rank
        isolated (bool): Whether numbers should be isolated
        
    Returns:
        tuple: (numbers, actual_rank) or (None, None) if failed
    """
    pass
```

**Comments:**
```python
# Good: Explain WHY
# Use -1 as special flag for triplets since count_consecutive_pairs
# would count triplet as 1 pair, causing logic conflict
if consecutive_pairs == -1:
    ...

# Bad: Explain WHAT (code already shows this)
# Check if consecutive pairs equals -1
if consecutive_pairs == -1:
    ...
```

---

## Testing

### Manual Testing

Before submitting PR:

```bash
# Test full workflow
python lottery_predictor.py

# Verify outputs
cat prediction_16_combinations.json
cat prediction_16_combinations.csv

# Check all 16 combinations generated
# Verify types match specifications
# Ensure even/odd counts correct
```

### Automated Testing (Future)

We plan to add:
- Unit tests for utility functions
- Integration tests for full workflow
- Performance benchmarks

Contributions to testing infrastructure welcome!

---

## Documentation

### Update Documentation

If your PR changes functionality:

✅ **DO update:**
- README.md (if user-facing changes)
- docs/USAGE.md (if usage changes)
- docs/API.md (if code API changes)
- Docstrings in code

### Writing Good Documentation

**Be clear:**
```markdown
❌ Bad: "Function does stuff with numbers"
✅ Good: "Generates lottery combination matching target frequency rank"
```

**Provide examples:**
```markdown
Example:
    >>> predictor.generate_combination(24.5, isolated=True)
    ([5, 11, 18, 23, 30, 47], 24.12)
```

**Explain parameters:**
```markdown
Args:
    target_rank (float): Desired mean frequency rank (1-49)
    isolated (bool): If True, no consecutive numbers allowed
```

---

## Areas for Contribution

### High Priority

- [ ] Add automated tests
- [ ] Improve triplet generation reliability
- [ ] Performance optimization for large datasets
- [ ] Multi-language support (English translation)

### Medium Priority

- [ ] Additional ML models (LSTM, XGBoost)
- [ ] Data visualization features
- [ ] Configuration file support
- [ ] Web interface

### Low Priority (But Welcome!)

- [ ] Docker containerization
- [ ] API endpoint
- [ ] Mobile app integration
- [ ] Historical accuracy tracking

---

## Community Guidelines

### Be Respectful

- Welcome newcomers
- Be patient with questions
- Provide constructive feedback
- Assume good intentions

### Be Helpful

- Answer questions when you can
- Share knowledge
- Help review PRs
- Improve documentation

### Be Professional

- Stay on topic
- Avoid personal attacks
- Respect different opinions
- Follow code of conduct

---

## Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Appreciated in commit messages

Significant contributions may result in:
- Collaborator status
- Decision-making input
- Project direction influence

---

## Getting Help

**Questions:**
- Open GitHub Discussion
- Check existing Issues
- Read documentation first

**Stuck on PR:**
- Ask in PR comments
- Tag maintainers
- Be specific about problem

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing!** 🎉

Every contribution, no matter how small, makes this project better.
