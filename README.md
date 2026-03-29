# 🎲 German Lotto 6/49 Predictor

**Automated lottery prediction system combining statistical analysis and machine learning**

A sophisticated Python-based prediction system for German Lotto 6 aus 49 that uses historical data analysis, frequency ranking, and ensemble ML models (Neural Networks + Random Forest) to generate statistically informed number combinations.

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

---

## 📊 Features

- **🔄 Automatic Data Updates**: Automatically syncs with online lottery database and updates local CSV
- **🤖 Machine Learning Models**: 
  - Multi-Layer Perceptron (MLP) Neural Network
  - Random Forest Regressor
  - Ensemble prediction combining both models
- **📈 Frequency Analysis**: Tracks historical frequency of all numbers (1-49)
- **🎯 Rank-Based Prediction**: Predicts mean frequency rank for next draw
- **🎲 16 Special Combinations**: Generates combinations with specific patterns:
  - Isolated numbers (no consecutive)
  - Consecutive pairs (e.g., 34, 35)
  - Consecutive triplets (e.g., 9, 10, 11)
  - Even/odd balance (3/3, 4/2, 2/4)
- **💾 Google Drive Integration**: Works seamlessly with `circulation_data.csv`
- **📁 Multiple Output Formats**: JSON and CSV results

---

## 🚀 Quick Start

### Prerequisites

```bash
python >= 3.7
numpy
pandas
scikit-learn
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/lottery-predictor.git
cd lottery-predictor

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Make sure circulation_data.csv is in the same directory
python lottery_predictor.py
```

The script will:
1. ✅ Load historical data from CSV
2. ✅ Check for updates online
3. ✅ Auto-append new draws to CSV
4. ✅ Calculate frequencies and ranks
5. ✅ Train ML models
6. ✅ Predict next draw's mean rank
7. ✅ Generate 16 special combinations
8. ✅ Save results to JSON and CSV

---

## 📁 Project Structure

```
lottery-predictor/
├── lottery_predictor.py          # Main prediction script
├── circulation_data.csv           # Historical draws database
├── prediction_16_combinations.json # Prediction results (JSON)
├── prediction_16_combinations.csv  # Prediction results (CSV)
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── LICENSE                        # MIT License
├── docs/
│   ├── INSTALLATION.md           # Detailed installation guide
│   ├── USAGE.md                  # Usage examples and guide
│   ├── METHODOLOGY.md            # Technical methodology
│   └── API.md                    # Code documentation
└── examples/
    ├── example_output.json       # Sample output
    └── example_combinations.csv  # Sample combinations
```

---

## 🎯 Combination Types

The system generates **16 combinations** with specific structural patterns:

| # | Type | Consecutive | Even/Odd | Count |
|---|------|-------------|----------|-------|
| 1-4 | Isolated | None | 3/3 | 4 |
| 5-6 | Isolated | None | 4/2 | 2 |
| 7-8 | Isolated | None | 2/4 | 2 |
| 9-10 | With pair | 1 pair | 3/3 | 2 |
| 11 | With pair | 1 pair | 4/2 | 1 |
| 12 | With pair | 1 pair | 2/4 | 1 |
| 13 | With pairs | 2 pairs | 3/3 | 1 |
| 14 | With pairs | 2 pairs | 4/2 | 1 |
| 15 | With pairs | 2 pairs | 2/4 | 1 |
| 16 | With triplet | Triplet | 3/3 | 1 |

### Examples

**Isolated (no consecutive):**
```
[5, 11, 18, 23, 30, 47]  ← All numbers isolated
```

**One consecutive pair:**
```
[7, 15, 22, 34, 35, 41]  ← Pair: (34, 35)
```

**Two consecutive pairs:**
```
[9, 10, 18, 25, 34, 35]  ← Pairs: (9,10), (34,35)
```

**Consecutive triplet:**
```
[9, 10, 11, 18, 25, 42]  ← Triplet: (9,10,11)
```

---

## 📊 CSV Data Format

The `circulation_data.csv` file should follow this format:

```csv
1,09.10.1955,[3, 12, 13, 16, 23, 41]
2,16.10.1955,[5, 8, 19, 27, 33, 47]
3,23.10.1955,[7, 14, 21, 28, 35, 42]
...
```

**Format:**
- Column 1: Draw ID (integer)
- Column 2: Date (dd.mm.yyyy)
- Column 3: Numbers (Python list format)

---

## 🤖 Machine Learning Models

### Multi-Layer Perceptron (MLP)
- Architecture: 10 → 100 → 50 → 25 → 1
- Activation: ReLU
- Early stopping enabled
- Mean Absolute Error (MAE): ~4.4

### Random Forest
- 100 decision trees
- Max depth: 10
- Parallel processing
- MAE: ~4.5-5.0

### Ensemble
- Average of MLP + RF predictions
- Typically achieves best results
- MAE: ~4.4

---

## 📈 Output Format

### prediction_16_combinations.json

```json
{
  "timestamp": "2026-03-29T10:30:00",
  "last_draw": {
    "id": 4988,
    "date": "25.12.2024",
    "numbers": [3, 15, 23, 35, 42, 48]
  },
  "predicted_rank": 24.35,
  "combinations": [
    {
      "id": 1,
      "numbers": [5, 11, 18, 23, 30, 47],
      "rank": 24.12,
      "type": "Изолированные 3Ч/3Н"
    },
    ...
  ]
}
```

---

## 🔬 Methodology

### Frequency Ranking System

1. **Frequency Calculation**: Count appearances of each number (1-49) across all historical draws
2. **Rank Assignment**: Sort by frequency (Rank 1 = most frequent, Rank 49 = least frequent)
3. **Mean Rank per Draw**: Calculate average rank of 6 numbers in each draw
4. **Temporal Patterns**: Analyze mean rank evolution over time
5. **Prediction**: Use ML models to forecast next draw's mean rank
6. **Generation**: Create combinations matching predicted rank

### Why This Works (Statistically)

- **Regression to the Mean**: Extreme values tend to return to average
- **Frequency Patterns**: While each draw is random, frequencies converge over time
- **Ensemble Learning**: Combining models reduces overfitting
- **Structured Generation**: Specific patterns match historical distribution

### Important Disclaimer

⚠️ **This is a statistical analysis tool for educational purposes**

- Each lottery draw is independent and random
- Past results do not influence future outcomes
- No system can predict lottery numbers with certainty
- Mathematical expectation is always negative for players
- Use responsibly and for research only

---

## 🛠️ Configuration

### Adjust Lookback Window

```python
# In main(), change lookback parameter
X, y = predictor.prepare_sequences(lookback=15)  # Default: 10
predicted_rank = predictor.predict_next_draw(lookback=15)
```

### Modify Rank Tolerance

```python
# In generate_combination() method
if abs(actual_rank - target_rank) < 2.0:  # Default: 3.0
    return candidate, actual_rank
```

### Increase Generation Attempts

```python
# For triplets (combination #16)
max_attempts=30000  # Default: 20000
```

---

## 📚 Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions
- **[Usage Guide](docs/USAGE.md)** - Examples and tutorials
- **[Methodology](docs/METHODOLOGY.md)** - Statistical analysis details
- **[API Reference](docs/API.md)** - Code documentation

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Historical lottery data from [LottoNumberArchive](https://johannesfriedrich.github.io/LottoNumberArchive/)
- Built with [scikit-learn](https://scikit-learn.org/)
- Inspired by statistical analysis and machine learning research

---

## 📞 Contact

**Project Link**: [https://github.com/yourusername/lottery-predictor](https://github.com/yourusername/lottery-predictor)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ for data science and statistical analysis**
