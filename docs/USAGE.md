# 📖 Usage Guide

Complete guide to using the German Lotto 6/49 Predictor.

---

## Quick Start

### Basic Usage

```bash
# Run prediction with default settings
python lottery_predictor.py
```

That's it! The script will:
1. Load data from `circulation_data.csv`
2. Check for online updates
3. Train models
4. Generate predictions
5. Save results

---

## Understanding the Output

### Console Output

```
================================================================================
ШАГ 1: ЗАГРУЗКА ДАННЫХ ИЗ CSV
================================================================================

✅ Загружено из CSV: 4,987 тиражей

📊 Последний тираж в CSV:
   ID: 4988
   Дата: 25.12.2024
   Числа: [3, 15, 23, 35, 42, 48]

================================================================================
ШАГ 8: ПРОГНОЗ СЛЕДУЮЩЕГО ТИРАЖА
================================================================================

🎯 ПРОГНОЗ СРЕДНЕГО РАНГА:
   MLP:      24.32
   RF:       24.41
   АНСАМБЛЬ: 24.35 ⭐

================================================================================
ШАГ 9: ГЕНЕРАЦИЯ 16 КОМБИНАЦИЙ
================================================================================

📊 Генерация комбинаций 1-4: Изолированные, 3Ч 3Н...
   #1: [5, 11, 18, 23, 30, 47] (ранг: 24.12)
   #2: [7, 13, 20, 28, 36, 43] (ранг: 24.45)
   ...
```

### Output Files

**prediction_16_combinations.json**
```json
{
  "timestamp": "2026-03-29T10:30:00",
  "last_draw": {
    "id": 4988,
    "date": "25.12.2024",
    "numbers": [3, 15, 23, 35, 42, 48]
  },
  "predicted_rank": 24.35,
  "combinations": [...]
}
```

**prediction_16_combinations.csv**
```csv
id,numbers,rank,type
1,"[5, 11, 18, 23, 30, 47]",24.12,Изолированные 3Ч/3Н
2,"[7, 13, 20, 28, 36, 43]",24.45,Изолированные 3Ч/3Н
...
```

---

## Advanced Usage

### Custom Lookback Window

Modify the main() function:

```python
# Change lookback from 10 to 15
X, y = predictor.prepare_sequences(lookback=15)
predicted_rank = predictor.predict_next_draw(lookback=15)
```

Larger lookback = more historical context  
Smaller lookback = more responsive to recent trends

### Adjust Rank Tolerance

In `generate_combination()` method:

```python
# Default: ±3.0
if abs(actual_rank - target_rank) < 3.0:
    return candidate, actual_rank

# Stricter: ±2.0
if abs(actual_rank - target_rank) < 2.0:
    return candidate, actual_rank
```

### Increase Generation Attempts

For difficult combinations (especially triplets):

```python
# In generate_16_combinations(), combination #16:
combo, rank = self.generate_combination(
    target_rank, 
    isolated=False,
    consecutive_pairs=-1,
    has_triplet_flag=True, 
    even_count=3,
    max_attempts=30000  # Increased from 20000
)
```

---

## Working with Results

### Reading JSON Results

```python
import json

# Load predictions
with open('prediction_16_combinations.json', 'r') as f:
    data = json.load(f)

# Access predictions
print(f"Predicted rank: {data['predicted_rank']}")
print(f"Last draw: {data['last_draw']['numbers']}")

# Iterate combinations
for combo in data['combinations']:
    print(f"#{combo['id']}: {combo['numbers']} ({combo['type']})")
```

### Reading CSV Results

```python
import pandas as pd

# Load as DataFrame
df = pd.read_csv('prediction_16_combinations.csv')

# Filter by type
isolated = df[df['type'].str.contains('Изолированные')]
print(isolated)

# Sort by rank
sorted_df = df.sort_values('rank')
print(sorted_df.head())
```

---

## Interpreting Results

### Predicted Rank

```
Predicted rank: 24.35

Interpretation:
- Numbers with average frequency expected
- Neither too common nor too rare
- Close to population mean (~24.4)
```

### Combination Types

**Isolated (Комбинация 1-8):**
```
[5, 11, 18, 23, 30, 47]
No consecutive numbers
Spread across number range
```

**With Pairs (Комбинация 9-15):**
```
[9, 10, 18, 25, 34, 35]
Two pairs: (9,10) and (34,35)
Rest isolated
```

**With Triplet (Комбинация 16):**
```
[9, 10, 11, 18, 25, 42]
Triplet: 9-10-11
Rest isolated
```

### Even/Odd Balance

```
3Ч/3Н → 3 even, 3 odd (balanced)
4Ч/2Н → 4 even, 2 odd (even-heavy)
2Ч/4Н → 2 even, 4 odd (odd-heavy)
```

---

## Common Workflows

### Weekly Prediction Workflow

```bash
# Monday: Update data and predict
python lottery_predictor.py

# Review results
cat prediction_16_combinations.json

# Choose combinations
# (Use your own strategy/preferences)
```

### Data Analysis Workflow

```python
# Load historical data
import pandas as pd
df = pd.read_csv('circulation_data.csv', 
                 header=None, 
                 names=['id', 'date', 'numbers'])

# Analyze frequency
from ast import literal_eval
all_numbers = []
for nums in df['numbers']:
    all_numbers.extend(literal_eval(nums))

from collections import Counter
freq = Counter(all_numbers)
print(freq.most_common(10))
```

---

## Automation

### Cron Job (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add line for weekly run (every Monday at 8 AM)
0 8 * * 1 cd /path/to/lottery-predictor && python3 lottery_predictor.py

# Check results
# (they'll be saved automatically)
```

### Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Weekly
4. Action: Start a program
5. Program: `python`
6. Arguments: `lottery_predictor.py`
7. Start in: `C:\path\to\lottery-predictor`

---

## Best Practices

### Data Management

✅ **DO:**
- Keep regular backups of `circulation_data.csv`
- Let script auto-update from online source
- Verify data format if manually editing

❌ **DON'T:**
- Edit CSV while script is running
- Delete historical data
- Use semicolons instead of commas

### Model Usage

✅ **DO:**
- Use ensemble prediction (most reliable)
- Understand that predictions are statistical
- Track prediction accuracy over time

❌ **DON'T:**
- Rely solely on predictions for betting
- Ignore the disclaimer
- Expect guaranteed wins

### Result Interpretation

✅ **DO:**
- Consider multiple combinations
- Understand combination types
- Use results as one factor among many

❌ **DON'T:**
- Bet more than you can afford to lose
- Ignore statistical reality
- Treat predictions as certainties

---

## Troubleshooting

### "No combinations generated"

**Possible causes:**
- Rank tolerance too strict
- Not enough attempts
- Data issues

**Solutions:**
```python
# Increase tolerance
if abs(actual_rank - target_rank) < 5.0:  # Was 3.0

# Increase attempts
max_attempts=50000  # Was 10000-20000
```

### "Data update failed"

**Possible causes:**
- No internet connection
- Online source unavailable

**Solution:**
```python
# Script will continue with cached data
# Or download data manually and place in directory
```

### "Model training takes too long"

**Solutions:**
```bash
# Reduce number of draws used
# (edit script to use last N draws only)

# Or increase patience
# Training 5000+ draws takes 1-2 minutes
```

---

## Performance Tips

### Speed Up Execution

1. **Use smaller lookback:**
   ```python
   lookback=5  # Instead of 10
   ```

2. **Reduce model complexity:**
   ```python
   MLPRegressor(hidden_layer_sizes=(50, 25))  # Instead of (100, 50, 25)
   ```

3. **Fewer trees in Random Forest:**
   ```python
   RandomForestRegressor(n_estimators=50)  # Instead of 100
   ```

### Improve Accuracy

1. **Increase lookback:**
   ```python
   lookback=15  # More context
   ```

2. **More training iterations:**
   ```python
   MLPRegressor(max_iter=1000)  # Instead of 500
   ```

---

## Next Steps

- 📊 Check [Methodology](METHODOLOGY.md) for technical details
- 🔧 Review [API Documentation](API.md) for code reference
- 💡 Explore example outputs in `/examples`

---

**Happy predicting! Remember: Use responsibly.** 🎲
