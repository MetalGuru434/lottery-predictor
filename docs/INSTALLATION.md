# 📦 Installation Guide

Complete installation instructions for German Lotto 6/49 Predictor.

---

## System Requirements

### Minimum Requirements
- **Python**: 3.7 or higher
- **RAM**: 512 MB
- **Disk Space**: 100 MB
- **Internet**: Required for initial data download

### Recommended
- **Python**: 3.9+
- **RAM**: 1 GB+
- **CPU**: Multi-core for faster model training

---

## Installation Methods

### Method 1: Clone from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/lottery-predictor.git

# Navigate to directory
cd lottery-predictor

# Install dependencies
pip install -r requirements.txt
```

### Method 2: Download ZIP

1. Download ZIP from GitHub
2. Extract to your preferred location
3. Open terminal in extracted folder
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Method 3: Manual Installation

```bash
# Create project directory
mkdir lottery-predictor
cd lottery-predictor

# Install dependencies manually
pip install numpy pandas scikit-learn

# Download lottery_predictor.py
# Place in directory
```

---

## Verify Installation

```bash
# Check Python version
python --version
# Should be 3.7+

# Check packages
python -c "import numpy, pandas, sklearn; print('All packages installed!')"
```

---

## Data Setup

### Option A: Use Provided Sample

```bash
# Sample circulation_data.csv included in repository
# Ready to use immediately
```

### Option B: Download Fresh Data

```bash
# Script will automatically download latest data
# On first run
python lottery_predictor.py
```

### Option C: Manual Data Setup

1. Create `circulation_data.csv` with format:
   ```csv
   1,09.10.1955,[3, 12, 13, 16, 23, 41]
   2,16.10.1955,[5, 8, 19, 27, 33, 47]
   ...
   ```

2. Place in same directory as script

---

## Virtual Environment (Recommended)

### Using venv

```bash
# Create virtual environment
python -m venv lottery-env

# Activate (Linux/Mac)
source lottery-env/bin/activate

# Activate (Windows)
lottery-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Using conda

```bash
# Create conda environment
conda create -n lottery python=3.9

# Activate
conda activate lottery

# Install dependencies
pip install -r requirements.txt
```

---

## Platform-Specific Notes

### Windows

```bash
# May need to use 'python' instead of 'python3'
python lottery_predictor.py

# If pip not found, try:
python -m pip install -r requirements.txt
```

### macOS

```bash
# Use python3 explicitly
python3 lottery_predictor.py

# Install pip if needed
python3 -m ensurepip --upgrade
```

### Linux

```bash
# Most distributions work out of the box
python3 lottery_predictor.py

# If scikit-learn fails, install system dependencies:
# Ubuntu/Debian:
sudo apt-get install python3-dev python3-pip

# Fedora:
sudo dnf install python3-devel python3-pip
```

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'numpy'`

**Solution:**
```bash
pip install numpy pandas scikit-learn
```

### Issue: `Permission denied` when installing

**Solution:**
```bash
# Install for user only
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
```

### Issue: `scikit-learn` installation fails

**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Then install scikit-learn
pip install scikit-learn
```

### Issue: `FileNotFoundError: circulation_data.csv`

**Solution:**
```bash
# Ensure CSV file is in same directory as script
ls circulation_data.csv

# Or let script download automatically
# (requires internet connection)
```

---

## Update Instructions

### Update from Git

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade
```

### Manual Update

1. Download latest `lottery_predictor.py`
2. Replace old file
3. Check if new dependencies needed
4. Re-run installation if necessary

---

## Uninstallation

### Remove Virtual Environment

```bash
# Deactivate first
deactivate

# Remove directory
rm -rf lottery-env/
```

### Remove Global Installation

```bash
# Uninstall packages
pip uninstall numpy pandas scikit-learn

# Remove project directory
rm -rf lottery-predictor/
```

---

## Next Steps

After installation:
1. ✅ Read [Usage Guide](USAGE.md)
2. ✅ Review [Methodology](METHODOLOGY.md)
3. ✅ Run first prediction
4. ✅ Explore example outputs

---

**Installation complete! Ready to make predictions.** 🎉
