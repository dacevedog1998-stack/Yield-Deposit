# Filling Optimisation Model — Static Three-Curve Version

## Final curve logic

### Expected Units

```text
Expected Units = Filling Batch / Target Filling
```

Expected Units remain fixed.

### Actual Units

```text
Actual Units = Filling Batch / Tested Filling Target
```

### Yield — blue line

```text
Yield = Actual Units / Expected Units × 100
```

Underweights are not subtracted from Yield.

### Good Units — green line

```text
Expected Seconds = Actual Units × Underweight Rate
Good Units = Actual Units - Expected Seconds
```

## Chart format

The chart is static and follows the approved preview format:

- Blue: Yield
- Red: Underweight %
- Green: Good Units
- Grey line: Target Filling
- Purple line: Input Scenario
- Orange line: Optimum Good Units

Zoom and Plotly controls have been removed.

## Inputs

### 1. Product Targets

- Target pastry
- Target filling
- Target glaze
- Filling batch
- Permitted reduction
- Maximum acceptable underweight

### 2. Scenario Adjustments

- Pastry adjustment: accepts negative and positive values
- Filling adjustment: accepts negative and positive values

### 3. Process Variation

Choose Standard Deviation in grams or Percentage CV, then enter:

- Pastry variation
- Filling variation

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```
